package election

const (
	Follower  = "follower"
	Candidate = "candidate"
	Leader    = "leader"
)

type voteRequest struct {
	Term        int
	CandidateID string
}

type voteResponse struct {
	Term        int
	VoteGranted bool
}

type heartbeatRequest struct {
	Term     int
	LeaderID string
}

type heartbeatResponse struct {
	Term int
}

type Node struct {
	ID             string
	Peers          []string
	sendRPC        func(target string, rpc string, payload any) any
	State          string
	Term           int
	VotedFor       string
	Suspected      bool
	silenceAge     int
	suspicionTTL   int
	electionTTL    int
	heartbeatEvery int
	heartbeatAge   int
	votes          map[string]struct{}
}

func NewNode(id string, peers []string, suspicionTTL int, electionTTL int, sendRPC func(string, string, any) any) *Node {
	return &Node{
		ID:             id,
		Peers:          peers,
		sendRPC:        sendRPC,
		State:          Follower,
		suspicionTTL:   suspicionTTL,
		electionTTL:    electionTTL,
		heartbeatEvery: 2,
		votes:          map[string]struct{}{},
	}
}

func (node *Node) Tick() {
	if node.State == Leader {
		node.heartbeatAge++
		if node.heartbeatAge >= node.heartbeatEvery {
			node.heartbeatAge = 0
			node.sendHeartbeats()
		}
		return
	}

	node.silenceAge++
	if node.silenceAge >= node.suspicionTTL {
		node.Suspected = true
	}
	if node.silenceAge >= node.electionTTL {
		node.startElection()
	}
}

func (node *Node) HandleVoteRequest(req voteRequest) voteResponse {
	if req.Term > node.Term {
		node.stepDown(req.Term)
	}
	if req.Term < node.Term {
		return voteResponse{Term: node.Term, VoteGranted: false}
	}

	canVote := node.VotedFor == "" || node.VotedFor == req.CandidateID
	if canVote {
		node.VotedFor = req.CandidateID
		node.silenceAge = 0
		node.Suspected = false
		return voteResponse{Term: node.Term, VoteGranted: true}
	}
	return voteResponse{Term: node.Term, VoteGranted: false}
}

func (node *Node) HandleHeartbeat(req heartbeatRequest) heartbeatResponse {
	if req.Term < node.Term {
		return heartbeatResponse{Term: node.Term}
	}
	if req.Term > node.Term || node.State != Follower {
		node.stepDown(req.Term)
	}
	node.silenceAge = 0
	node.Suspected = false
	return heartbeatResponse{Term: node.Term}
}

func (node *Node) startElection() {
	node.State = Candidate
	node.Term++
	node.VotedFor = node.ID
	node.Suspected = false
	node.silenceAge = 0
	node.votes = map[string]struct{}{node.ID: {}}

	for _, peer := range node.Peers {
		raw := node.sendRPC(peer, "vote", voteRequest{
			Term:        node.Term,
			CandidateID: node.ID,
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
	node.Suspected = false
	node.heartbeatAge = 0
	node.sendHeartbeats()
}

func (node *Node) stepDown(term int) {
	node.State = Follower
	node.Term = term
	node.VotedFor = ""
	node.Suspected = false
	node.silenceAge = 0
	node.heartbeatAge = 0
	node.votes = map[string]struct{}{}
}

func (node *Node) sendHeartbeats() {
	for _, peer := range node.Peers {
		raw := node.sendRPC(peer, "heartbeat", heartbeatRequest{
			Term:     node.Term,
			LeaderID: node.ID,
		})
		resp, ok := raw.(heartbeatResponse)
		if !ok {
			continue
		}
		if resp.Term > node.Term {
			node.stepDown(resp.Term)
			return
		}
	}
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
	for index, id := range nodeIDs {
		peers := make([]string, 0, len(nodeIDs)-1)
		for _, peer := range nodeIDs {
			if peer != id {
				peers = append(peers, peer)
			}
		}
		node := NewNode(id, peers, 3+index*2, 4+index*2, func(target string, rpc string, payload any) any {
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
		node := cluster.nodes[id]
		if node.State == Leader {
			return node
		}
	}
	return nil
}

func (cluster *Cluster) Node(id string) *Node {
	return cluster.nodes[id]
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
	node := cluster.nodes[id]
	if node != nil {
		node.silenceAge = 0
		node.Suspected = false
	}
}

func (cluster *Cluster) deliverRPC(target string, rpc string, payload any) any {
	if _, down := cluster.downed[target]; down {
		return nil
	}
	node := cluster.nodes[target]
	switch rpc {
	case "vote":
		return node.HandleVoteRequest(payload.(voteRequest))
	case "heartbeat":
		return node.HandleHeartbeat(payload.(heartbeatRequest))
	default:
		return nil
	}
}

func majority(size int) int {
	return size/2 + 1
}
