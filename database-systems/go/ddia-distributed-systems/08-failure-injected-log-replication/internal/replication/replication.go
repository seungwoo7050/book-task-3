package replication

import "fmt"

const (
	MessageAppend = "append"
	MessageAck    = "ack"
)

type LogEntry struct {
	Index     int
	Operation string
	Key       string
	Value     *string
}

type Message struct {
	Kind  string
	From  string
	To    string
	Index int
	Entry *LogEntry
}

type Leader struct {
	ID          string
	log         []LogEntry
	store       map[string]string
	nextIndex   map[string]int
	matchIndex  map[string]int
	commitIndex int
}

func NewLeader(id string, followerIDs []string) *Leader {
	leader := &Leader{
		ID:          id,
		store:       map[string]string{},
		nextIndex:   map[string]int{},
		matchIndex:  map[string]int{},
		commitIndex: -1,
	}
	for _, followerID := range followerIDs {
		leader.nextIndex[followerID] = 0
		leader.matchIndex[followerID] = -1
	}
	return leader
}

func (leader *Leader) AppendPut(key string, value string) LogEntry {
	entry := LogEntry{
		Index:     len(leader.log),
		Operation: "put",
		Key:       key,
		Value:     stringPtr(value),
	}
	leader.log = append(leader.log, entry)
	leader.store[key] = value
	return entry
}

func (leader *Leader) CommitIndex() int {
	return leader.commitIndex
}

func (leader *Leader) Read(key string) (string, bool) {
	value, ok := leader.store[key]
	return value, ok
}

func (leader *Leader) LogLength() int {
	return len(leader.log)
}

func (leader *Leader) outgoingAppends() []Message {
	messages := make([]Message, 0, len(leader.nextIndex))
	for followerID, nextIndex := range leader.nextIndex {
		if nextIndex >= len(leader.log) {
			continue
		}
		entry := leader.log[nextIndex]
		copyEntry := entry
		messages = append(messages, Message{
			Kind:  MessageAppend,
			From:  leader.ID,
			To:    followerID,
			Index: entry.Index,
			Entry: &copyEntry,
		})
	}
	return messages
}

func (leader *Leader) handleAck(followerID string, index int) {
	if index > leader.matchIndex[followerID] {
		leader.matchIndex[followerID] = index
		leader.nextIndex[followerID] = index + 1
	}
	leader.advanceCommit()
}

func (leader *Leader) advanceCommit() {
	for index := len(leader.log) - 1; index > leader.commitIndex; index-- {
		replicated := 1
		for _, matchIndex := range leader.matchIndex {
			if matchIndex >= index {
				replicated++
			}
		}
		if replicated >= majority(len(leader.matchIndex)+1) {
			leader.commitIndex = index
			return
		}
	}
}

type Follower struct {
	ID           string
	log          []LogEntry
	store        map[string]string
	appliedCount int
}

func NewFollower(id string) *Follower {
	return &Follower{
		ID:    id,
		store: map[string]string{},
	}
}

func (follower *Follower) HandleAppend(entry LogEntry) int {
	if entry.Index < len(follower.log) {
		if equalEntry(follower.log[entry.Index], entry) {
			return follower.Watermark()
		}
		follower.log = append([]LogEntry(nil), follower.log[:entry.Index]...)
		follower.rebuildStore()
	}
	if entry.Index > len(follower.log) {
		return follower.Watermark()
	}
	if entry.Index == len(follower.log) {
		follower.log = append(follower.log, entry)
		follower.apply(entry)
	}
	return follower.Watermark()
}

func (follower *Follower) Watermark() int {
	return len(follower.log) - 1
}

func (follower *Follower) Read(key string) (string, bool) {
	value, ok := follower.store[key]
	return value, ok
}

func (follower *Follower) LogLength() int {
	return len(follower.log)
}

func (follower *Follower) AppliedCount() int {
	return follower.appliedCount
}

func (follower *Follower) apply(entry LogEntry) {
	switch entry.Operation {
	case "put":
		if entry.Value != nil {
			follower.store[entry.Key] = *entry.Value
		}
	}
	follower.appliedCount++
}

func (follower *Follower) rebuildStore() {
	follower.store = map[string]string{}
	follower.appliedCount = 0
	for _, entry := range follower.log {
		follower.apply(entry)
	}
}

type NetworkHarness struct {
	paused         map[string]bool
	dropRules      map[string]int
	duplicateRules map[string]int
}

func NewNetworkHarness() *NetworkHarness {
	return &NetworkHarness{
		paused:         map[string]bool{},
		dropRules:      map[string]int{},
		duplicateRules: map[string]int{},
	}
}

func (network *NetworkHarness) PauseNode(id string) {
	network.paused[id] = true
}

func (network *NetworkHarness) ResumeNode(id string) {
	delete(network.paused, id)
}

func (network *NetworkHarness) DropNext(kind string, to string, index int, count int) {
	network.dropRules[ruleKey(kind, to, index)] += count
}

func (network *NetworkHarness) DuplicateNext(kind string, to string, index int, count int) {
	network.duplicateRules[ruleKey(kind, to, index)] += count
}

func (network *NetworkHarness) Route(messages []Message, handler func(Message) []Message) {
	queue := append([]Message(nil), messages...)
	for len(queue) > 0 {
		message := queue[0]
		queue = queue[1:]

		if network.paused[message.To] {
			continue
		}
		key := ruleKey(message.Kind, message.To, message.Index)
		if network.dropRules[key] > 0 {
			network.dropRules[key]--
			continue
		}

		deliveries := 1
		if network.duplicateRules[key] > 0 {
			network.duplicateRules[key]--
			deliveries = 2
		}
		for range deliveries {
			replies := handler(message)
			queue = append(queue, replies...)
		}
	}
}

type Cluster struct {
	Leader    *Leader
	followers map[string]*Follower
	order     []string
	Network   *NetworkHarness
}

func NewCluster(leaderID string, followerIDs []string) *Cluster {
	cluster := &Cluster{
		Leader:    NewLeader(leaderID, followerIDs),
		followers: map[string]*Follower{},
		order:     append([]string(nil), followerIDs...),
		Network:   NewNetworkHarness(),
	}
	for _, followerID := range followerIDs {
		cluster.followers[followerID] = NewFollower(followerID)
	}
	return cluster
}

func (cluster *Cluster) Put(key string, value string) LogEntry {
	return cluster.Leader.AppendPut(key, value)
}

func (cluster *Cluster) Tick() {
	cluster.Network.Route(cluster.Leader.outgoingAppends(), cluster.handleMessage)
}

func (cluster *Cluster) Follower(id string) (*Follower, error) {
	follower := cluster.followers[id]
	if follower == nil {
		return nil, fmt.Errorf("unknown follower %s", id)
	}
	return follower, nil
}

func (cluster *Cluster) PauseNode(id string) {
	cluster.Network.PauseNode(id)
}

func (cluster *Cluster) ResumeNode(id string) {
	cluster.Network.ResumeNode(id)
}

func (cluster *Cluster) DropNext(kind string, to string, index int, count int) {
	cluster.Network.DropNext(kind, to, index, count)
}

func (cluster *Cluster) DuplicateNext(kind string, to string, index int, count int) {
	cluster.Network.DuplicateNext(kind, to, index, count)
}

func (cluster *Cluster) handleMessage(message Message) []Message {
	if message.To == cluster.Leader.ID && message.Kind == MessageAck {
		cluster.Leader.handleAck(message.From, message.Index)
		return nil
	}
	if message.Kind != MessageAppend || message.Entry == nil {
		return nil
	}
	follower := cluster.followers[message.To]
	if follower == nil {
		return nil
	}
	ackIndex := follower.HandleAppend(*message.Entry)
	return []Message{{
		Kind:  MessageAck,
		From:  follower.ID,
		To:    cluster.Leader.ID,
		Index: ackIndex,
	}}
}

func majority(size int) int {
	return size/2 + 1
}

func ruleKey(kind string, to string, index int) string {
	return fmt.Sprintf("%s|%s|%d", kind, to, index)
}

func equalEntry(left LogEntry, right LogEntry) bool {
	if left.Index != right.Index || left.Operation != right.Operation || left.Key != right.Key {
		return false
	}
	switch {
	case left.Value == nil && right.Value == nil:
		return true
	case left.Value != nil && right.Value != nil:
		return *left.Value == *right.Value
	default:
		return false
	}
}

func stringPtr(value string) *string {
	copyValue := value
	return &copyValue
}
