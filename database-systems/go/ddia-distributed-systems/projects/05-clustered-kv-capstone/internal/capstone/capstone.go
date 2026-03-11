package capstone

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"slices"

	"study.local/go/shared/hash"
)

type Operation struct {
	Offset int     `json:"offset"`
	Type   string  `json:"type"`
	Key    string  `json:"key"`
	Value  *string `json:"value,omitempty"`
}

type Store struct {
	path string
	data map[string]string
	log  []Operation
}

func LoadStore(path string) (*Store, error) {
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return nil, err
	}
	file, err := os.OpenFile(path, os.O_CREATE|os.O_RDONLY, 0o644)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	store := &Store{path: path, data: map[string]string{}}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var op Operation
		if err := json.Unmarshal(scanner.Bytes(), &op); err != nil {
			return nil, err
		}
		store.applyInMemory(op)
		store.log = append(store.log, op)
	}
	return store, scanner.Err()
}

func (store *Store) AppendPut(key string, value string) (Operation, error) {
	op := Operation{Offset: len(store.log), Type: "put", Key: key, Value: stringPtr(value)}
	return op, store.Apply(op)
}

func (store *Store) AppendDelete(key string) (Operation, error) {
	op := Operation{Offset: len(store.log), Type: "delete", Key: key}
	return op, store.Apply(op)
}

func (store *Store) Apply(op Operation) error {
	if op.Offset < len(store.log) {
		return nil
	}
	if op.Offset != len(store.log) {
		return fmt.Errorf("store: non-sequential offset %d", op.Offset)
	}

	file, err := os.OpenFile(store.path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o644)
	if err != nil {
		return err
	}
	defer file.Close()

	buffer, err := json.Marshal(op)
	if err != nil {
		return err
	}
	if _, err := file.Write(append(buffer, '\n')); err != nil {
		return err
	}
	store.applyInMemory(op)
	store.log = append(store.log, op)
	return nil
}

func (store *Store) EntriesFrom(offset int) []Operation {
	if offset < 0 {
		offset = 0
	}
	if offset >= len(store.log) {
		return []Operation{}
	}
	return append([]Operation(nil), store.log[offset:]...)
}

func (store *Store) Watermark() int {
	return len(store.log) - 1
}

func (store *Store) Get(key string) (string, bool) {
	value, ok := store.data[key]
	return value, ok
}

func (store *Store) applyInMemory(op Operation) {
	switch op.Type {
	case "put":
		if op.Value != nil {
			store.data[op.Key] = *op.Value
		}
	case "delete":
		delete(store.data, op.Key)
	}
}

type ReplicaGroup struct {
	ShardID   string
	Leader    string
	Followers []string
}

type Node struct {
	ID     string
	stores map[string]*Store
}

type ringEntry struct {
	Hash    uint32
	ShardID string
}

type shardRing struct {
	virtualNodes int
	ring         []ringEntry
}

func newShardRing(virtualNodes int) *shardRing {
	if virtualNodes <= 0 {
		virtualNodes = 64
	}
	return &shardRing{virtualNodes: virtualNodes}
}

func (ring *shardRing) AddShard(shardID string) {
	for i := 0; i < ring.virtualNodes; i++ {
		entry := ringEntry{
			Hash:    hash.MurmurHash3([]byte(shardID+"#v"+itoa(i)), 0),
			ShardID: shardID,
		}
		index := slices.IndexFunc(ring.ring, func(candidate ringEntry) bool {
			return candidate.Hash >= entry.Hash
		})
		if index == -1 {
			ring.ring = append(ring.ring, entry)
		} else {
			ring.ring = append(ring.ring[:index], append([]ringEntry{entry}, ring.ring[index:]...)...)
		}
	}
}

func (ring *shardRing) ShardForKey(key string) string {
	target := hash.MurmurHash3([]byte(key), 0)
	index := slices.IndexFunc(ring.ring, func(entry ringEntry) bool {
		return entry.Hash >= target
	})
	if index == -1 {
		index = 0
	}
	return ring.ring[index].ShardID
}

type Cluster struct {
	dataDir       string
	router        *shardRing
	groups        map[string]ReplicaGroup
	nodes         map[string]*Node
	autoReplicate bool
}

func NewCluster(dataDir string, groups []ReplicaGroup, virtualNodes int) (*Cluster, error) {
	cluster := &Cluster{
		dataDir:       dataDir,
		router:        newShardRing(virtualNodes),
		groups:        map[string]ReplicaGroup{},
		nodes:         map[string]*Node{},
		autoReplicate: true,
	}
	for _, group := range groups {
		cluster.groups[group.ShardID] = group
		cluster.router.AddShard(group.ShardID)
		members := append([]string{group.Leader}, group.Followers...)
		for _, nodeID := range members {
			node := cluster.nodes[nodeID]
			if node == nil {
				node = &Node{ID: nodeID, stores: map[string]*Store{}}
				cluster.nodes[nodeID] = node
			}
			store, err := LoadStore(filepath.Join(dataDir, nodeID, group.ShardID+".log"))
			if err != nil {
				return nil, err
			}
			node.stores[group.ShardID] = store
		}
	}
	return cluster, nil
}

func (cluster *Cluster) SetAutoReplicate(enabled bool) {
	cluster.autoReplicate = enabled
}

func (cluster *Cluster) RouteShard(key string) string {
	return cluster.router.ShardForKey(key)
}

func (cluster *Cluster) Group(shardID string) ReplicaGroup {
	return cluster.groups[shardID]
}

func (cluster *Cluster) Put(key string, value string) (string, error) {
	shardID := cluster.RouteShard(key)
	group := cluster.groups[shardID]
	store := cluster.nodes[group.Leader].stores[shardID]
	if _, err := store.AppendPut(key, value); err != nil {
		return shardID, err
	}
	if cluster.autoReplicate {
		for _, followerID := range group.Followers {
			if _, err := cluster.SyncFollower(shardID, followerID); err != nil {
				return shardID, err
			}
		}
	}
	return shardID, nil
}

func (cluster *Cluster) Delete(key string) (string, error) {
	shardID := cluster.RouteShard(key)
	group := cluster.groups[shardID]
	store := cluster.nodes[group.Leader].stores[shardID]
	if _, err := store.AppendDelete(key); err != nil {
		return shardID, err
	}
	if cluster.autoReplicate {
		for _, followerID := range group.Followers {
			if _, err := cluster.SyncFollower(shardID, followerID); err != nil {
				return shardID, err
			}
		}
	}
	return shardID, nil
}

func (cluster *Cluster) SyncFollower(shardID string, followerID string) (int, error) {
	group := cluster.groups[shardID]
	leaderStore := cluster.nodes[group.Leader].stores[shardID]
	followerStore := cluster.nodes[followerID].stores[shardID]
	entries := leaderStore.EntriesFrom(followerStore.Watermark() + 1)
	applied := 0
	for _, entry := range entries {
		if err := followerStore.Apply(entry); err != nil {
			return applied, err
		}
		applied++
	}
	return applied, nil
}

func (cluster *Cluster) Read(key string) (string, bool, string, error) {
	shardID := cluster.RouteShard(key)
	group := cluster.groups[shardID]
	value, ok := cluster.nodes[group.Leader].stores[shardID].Get(key)
	return value, ok, shardID, nil
}

func (cluster *Cluster) ReadFromNode(nodeID string, key string) (string, bool, error) {
	shardID := cluster.RouteShard(key)
	node := cluster.nodes[nodeID]
	if node == nil || node.stores[shardID] == nil {
		return "", false, fmt.Errorf("node %s is not replica for shard %s", nodeID, shardID)
	}
	value, ok := node.stores[shardID].Get(key)
	return value, ok, nil
}

func (cluster *Cluster) RestartNode(nodeID string) error {
	node := cluster.nodes[nodeID]
	if node == nil {
		return fmt.Errorf("unknown node %s", nodeID)
	}
	for shardID := range node.stores {
		store, err := LoadStore(filepath.Join(cluster.dataDir, nodeID, shardID+".log"))
		if err != nil {
			return err
		}
		node.stores[shardID] = store
	}
	return nil
}

func stringPtr(value string) *string {
	copyValue := value
	return &copyValue
}

func itoa(value int) string {
	if value == 0 {
		return "0"
	}
	buffer := make([]byte, 0, 4)
	for value > 0 {
		buffer = append([]byte{byte('0' + value%10)}, buffer...)
		value /= 10
	}
	return string(buffer)
}
