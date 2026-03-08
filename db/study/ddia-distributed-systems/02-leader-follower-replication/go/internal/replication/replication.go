package replication

type LogEntry struct {
	Offset    int
	Operation string
	Key       string
	Value     *string
}

type ReplicationLog struct {
	entries []LogEntry
}

func (log *ReplicationLog) Append(operation string, key string, value *string) int {
	offset := len(log.entries)
	log.entries = append(log.entries, LogEntry{
		Offset:    offset,
		Operation: operation,
		Key:       key,
		Value:     value,
	})
	return offset
}

func (log *ReplicationLog) From(offset int) []LogEntry {
	if offset < 0 {
		offset = 0
	}
	if offset >= len(log.entries) {
		return []LogEntry{}
	}
	return append([]LogEntry(nil), log.entries[offset:]...)
}

func (log *ReplicationLog) LatestOffset() int {
	return len(log.entries) - 1
}

type Leader struct {
	store map[string]string
	log   *ReplicationLog
}

func NewLeader() *Leader {
	return &Leader{
		store: map[string]string{},
		log:   &ReplicationLog{},
	}
}

func (leader *Leader) Put(key string, value string) int {
	leader.store[key] = value
	return leader.log.Append("put", key, stringPtr(value))
}

func (leader *Leader) Delete(key string) int {
	delete(leader.store, key)
	return leader.log.Append("delete", key, nil)
}

func (leader *Leader) Get(key string) (string, bool) {
	value, ok := leader.store[key]
	return value, ok
}

func (leader *Leader) LogFrom(offset int) []LogEntry {
	return leader.log.From(offset)
}

func (leader *Leader) LatestOffset() int {
	return leader.log.LatestOffset()
}

type Follower struct {
	store             map[string]string
	lastAppliedOffset int
}

func NewFollower() *Follower {
	return &Follower{
		store:             map[string]string{},
		lastAppliedOffset: -1,
	}
}

func (follower *Follower) Apply(entries []LogEntry) int {
	applied := 0
	for _, entry := range entries {
		if entry.Offset <= follower.lastAppliedOffset {
			continue
		}
		switch entry.Operation {
		case "put":
			if entry.Value != nil {
				follower.store[entry.Key] = *entry.Value
			}
		case "delete":
			delete(follower.store, entry.Key)
		}
		follower.lastAppliedOffset = entry.Offset
		applied++
	}
	return applied
}

func (follower *Follower) Get(key string) (string, bool) {
	value, ok := follower.store[key]
	return value, ok
}

func (follower *Follower) Watermark() int {
	return follower.lastAppliedOffset
}

func ReplicateOnce(leader *Leader, follower *Follower) int {
	entries := leader.LogFrom(follower.Watermark() + 1)
	return follower.Apply(entries)
}

func stringPtr(value string) *string {
	copyValue := value
	return &copyValue
}
