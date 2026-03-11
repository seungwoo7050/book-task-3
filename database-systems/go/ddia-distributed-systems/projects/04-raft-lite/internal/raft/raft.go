package raft

const (
	Follower  = "follower"
	Candidate = "candidate"
	Leader    = "leader"
)

type LogEntry struct {
	Index   int
	Term    int
	Command string
}

type voteRequest struct {
	Term         int
	CandidateID  string
	LastLogIndex int
	LastLogTerm  int
}

type voteResponse struct {
	Term        int
	VoteGranted bool
}

type appendRequest struct {
	Term         int
	LeaderID     string
	PrevLogIndex int
	PrevLogTerm  int
	Entries      []LogEntry
	LeaderCommit int
}

type appendResponse struct {
	Term    int
	Success bool
}

type Node struct {
	ID        string
	Peers     []string
	sendRPC   func(target string, rpc string, payload any) any
	State     string
	Term      int
	VotedFor  string
	Log       []LogEntry
	CommitIdx int

	nextIndex   map[string]int
	matchIndex  map[string]int
	electionTTL int
	electionAge int
	heartbeat   int
	heartAge    int
	votes       map[string]struct{}
}

func NewNode(id string, peers []string, electionTTL int, sendRPC func(string, string, any) any) *Node {
	return &Node{
		ID:          id,
		Peers:       peers,
		sendRPC:     sendRPC,
		State:       Follower,
		CommitIdx:   -1,
		nextIndex:   map[string]int{},
		matchIndex:  map[string]int{},
		electionTTL: electionTTL,
		heartbeat:   2,
		votes:       map[string]struct{}{},
	}
}

func (node *Node) Tick() {
	if node.State == Leader {
		node.heartAge++
		if node.heartAge >= node.heartbeat {
			node.heartAge = 0
			node.sendHeartbeats()
		}
		return
	}

	node.electionAge++
	if node.electionAge >= node.electionTTL {
		node.startElection()
	}
}

func (node *Node) startElection() {
	node.State = Candidate
	node.Term++
	node.VotedFor = node.ID
	node.votes = map[string]struct{}{node.ID: {}}
	node.electionAge = 0

	lastIndex, lastTerm := node.lastLogInfo()
	for _, peer := range node.Peers {
		raw := node.sendRPC(peer, "requestVote", voteRequest{
			Term:         node.Term,
			CandidateID:  node.ID,
			LastLogIndex: lastIndex,
			LastLogTerm:  lastTerm,
		})
		resp, ok := raw.(voteResponse)
		if !ok {
			continue
		}
		if resp.Term > node.Term {
			node.stepDown(resp.Term)
			return
		}
		if resp.VoteGranted {
			node.votes[peer] = struct{}{}
		}
	}

	if len(node.votes) >= majority(len(node.Peers)+1) {
		node.becomeLeader()
	}
}

func (node *Node) becomeLeader() {
	node.State = Leader
	node.heartAge = 0
	next := len(node.Log)
	for _, peer := range node.Peers {
		node.nextIndex[peer] = next
		node.matchIndex[peer] = -1
	}
	node.sendHeartbeats()
}

func (node *Node) stepDown(term int) {
	node.State = Follower
	node.Term = term
	node.VotedFor = ""
	node.electionAge = 0
	node.votes = map[string]struct{}{}
}

func (node *Node) HandleRequestVote(req voteRequest) voteResponse {
	if req.Term > node.Term {
		node.stepDown(req.Term)
	}
	if req.Term < node.Term {
		return voteResponse{Term: node.Term, VoteGranted: false}
	}

	lastIndex, lastTerm := node.lastLogInfo()
	upToDate := req.LastLogTerm > lastTerm || (req.LastLogTerm == lastTerm && req.LastLogIndex >= lastIndex)
	canVote := node.VotedFor == "" || node.VotedFor == req.CandidateID
	if canVote && upToDate {
		node.VotedFor = req.CandidateID
		node.electionAge = 0
		return voteResponse{Term: node.Term, VoteGranted: true}
	}
	return voteResponse{Term: node.Term, VoteGranted: false}
}

func (node *Node) HandleAppendEntries(req appendRequest) appendResponse {
	if req.Term < node.Term {
		return appendResponse{Term: node.Term, Success: false}
	}
	if req.Term >= node.Term && (node.State != Follower || req.Term > node.Term) {
		node.stepDown(req.Term)
	}
	node.electionAge = 0

	if req.PrevLogIndex >= 0 {
		if req.PrevLogIndex >= len(node.Log) {
			return appendResponse{Term: node.Term, Success: false}
		}
		if node.Log[req.PrevLogIndex].Term != req.PrevLogTerm {
			node.Log = node.Log[:req.PrevLogIndex]
			return appendResponse{Term: node.Term, Success: false}
		}
	}

	for i, entry := range req.Entries {
		index := req.PrevLogIndex + 1 + i
		if index < len(node.Log) {
			if node.Log[index].Term != entry.Term {
				node.Log = node.Log[:index]
				node.Log = append(node.Log, entry)
			}
		} else {
			node.Log = append(node.Log, entry)
		}
	}

	if req.LeaderCommit > node.CommitIdx {
		node.CommitIdx = min(req.LeaderCommit, len(node.Log)-1)
	}
	return appendResponse{Term: node.Term, Success: true}
}

func (node *Node) ClientRequest(command string) *LogEntry {
	if node.State != Leader {
		return nil
	}
	entry := LogEntry{Index: len(node.Log), Term: node.Term, Command: command}
	node.Log = append(node.Log, entry)
	return &entry
}

func (node *Node) sendHeartbeats() {
	for _, peer := range node.Peers {
		node.replicateTo(peer)
	}
	node.advanceCommitIndex()
}

func (node *Node) replicateTo(peer string) {
	next := node.nextIndex[peer]
	prevIndex := next - 1
	prevTerm := 0
	if prevIndex >= 0 && prevIndex < len(node.Log) {
		prevTerm = node.Log[prevIndex].Term
	}
	entries := append([]LogEntry(nil), node.Log[next:]...)
	raw := node.sendRPC(peer, "appendEntries", appendRequest{
		Term:         node.Term,
		LeaderID:     node.ID,
		PrevLogIndex: prevIndex,
		PrevLogTerm:  prevTerm,
		Entries:      entries,
		LeaderCommit: node.CommitIdx,
	})
	resp, ok := raw.(appendResponse)
	if !ok {
		return
	}
	if resp.Term > node.Term {
		node.stepDown(resp.Term)
		return
	}
	if resp.Success {
		node.nextIndex[peer] = next + len(entries)
		node.matchIndex[peer] = node.nextIndex[peer] - 1
		return
	}
	if node.nextIndex[peer] > 0 {
		node.nextIndex[peer]--
	}
}

func (node *Node) advanceCommitIndex() {
	for index := len(node.Log) - 1; index > node.CommitIdx; index-- {
		if node.Log[index].Term != node.Term {
			continue
		}
		replicated := 1
		for _, peer := range node.Peers {
			if node.matchIndex[peer] >= index {
				replicated++
			}
		}
		if replicated >= majority(len(node.Peers)+1) {
			node.CommitIdx = index
			break
		}
	}
}

func (node *Node) lastLogInfo() (int, int) {
	if len(node.Log) == 0 {
		return -1, 0
	}
	last := node.Log[len(node.Log)-1]
	return last.Index, last.Term
}

type Cluster struct {
	nodes  map[string]*Node
	downed map[string]struct{}
	order  []string
}

func NewCluster(nodeIDs []string) *Cluster {
	cluster := &Cluster{
		nodes:  map[string]*Node{},
		downed: map[string]struct{}{},
		order:  append([]string(nil), nodeIDs...),
	}
	for i, id := range nodeIDs {
		peers := make([]string, 0, len(nodeIDs)-1)
		for _, peer := range nodeIDs {
			if peer != id {
				peers = append(peers, peer)
			}
		}
		node := NewNode(id, peers, 5+i*2, func(target string, rpc string, payload any) any {
			return cluster.deliverRPC(target, rpc, payload)
		})
		cluster.nodes[id] = node
	}
	return cluster
}

func (cluster *Cluster) Tick() {
	for _, id := range cluster.order {
		if _, down := cluster.downed[id]; down {
			continue
		}
		cluster.nodes[id].Tick()
	}
}

func (cluster *Cluster) Leader() *Node {
	for _, id := range cluster.order {
		if _, down := cluster.downed[id]; down {
			continue
		}
		if cluster.nodes[id].State == Leader {
			return cluster.nodes[id]
		}
	}
	return nil
}

func (cluster *Cluster) Nodes() []*Node {
	nodes := make([]*Node, 0, len(cluster.order))
	for _, id := range cluster.order {
		nodes = append(nodes, cluster.nodes[id])
	}
	return nodes
}

func (cluster *Cluster) DownNode(id string) {
	cluster.downed[id] = struct{}{}
}

func (cluster *Cluster) UpNode(id string) {
	delete(cluster.downed, id)
	cluster.nodes[id].electionAge = 0
}

func (cluster *Cluster) ClientRequest(command string) *LogEntry {
	leader := cluster.Leader()
	if leader == nil {
		return nil
	}
	return leader.ClientRequest(command)
}

func (cluster *Cluster) deliverRPC(target string, rpc string, payload any) any {
	if _, down := cluster.downed[target]; down {
		return nil
	}
	node := cluster.nodes[target]
	switch rpc {
	case "requestVote":
		return node.HandleRequestVote(payload.(voteRequest))
	case "appendEntries":
		return node.HandleAppendEntries(payload.(appendRequest))
	default:
		return nil
	}
}

func majority(size int) int {
	return size/2 + 1
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}
