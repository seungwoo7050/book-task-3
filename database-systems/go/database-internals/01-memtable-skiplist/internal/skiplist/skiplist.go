package skiplist

import (
	"math/rand"
)

const (
	maxLevel     = 16
	probability  = 0.5
	nodeOverhead = 64
)

// ValueState distinguishes a live value, a tombstone, and a missing key.
type ValueState int

const (
	Missing ValueState = iota
	Present
	Tombstone
)

// Entry is one logical MemTable record.
type Entry struct {
	Key   string
	Value *string
}

type node struct {
	key     string
	value   *string
	forward []*node
}

// SkipList stores ordered key-value records for the MemTable phase.
type SkipList struct {
	rng      *rand.Rand
	level    int
	header   *node
	size     int
	byteSize int
}

// New returns an empty SkipList with deterministic level generation.
func New() *SkipList {
	return &SkipList{
		rng:    rand.New(rand.NewSource(7)),
		header: newNode("", nil, maxLevel),
	}
}

func newNode(key string, value *string, level int) *node {
	return &node{
		key:     key,
		value:   value,
		forward: make([]*node, level+1),
	}
}

func (s *SkipList) randomLevel() int {
	level := 0
	for level < maxLevel && s.rng.Float64() < probability {
		level++
	}
	return level
}

// Put inserts or updates a live value.
func (s *SkipList) Put(key, value string) {
	copyValue := value
	s.put(key, &copyValue)
}

// Delete replaces the key with a tombstone.
func (s *SkipList) Delete(key string) {
	s.put(key, nil)
}

func (s *SkipList) put(key string, value *string) {
	update := make([]*node, maxLevel+1)
	current := s.header

	for level := s.level; level >= 0; level-- {
		for current.forward[level] != nil && current.forward[level].key < key {
			current = current.forward[level]
		}
		update[level] = current
	}

	current = current.forward[0]
	if current != nil && current.key == key {
		s.byteSize += valueLen(value) - valueLen(current.value)
		current.value = value
		return
	}

	newLevel := s.randomLevel()
	if newLevel > s.level {
		for level := s.level + 1; level <= newLevel; level++ {
			update[level] = s.header
		}
		s.level = newLevel
	}

	inserted := newNode(key, value, newLevel)
	for level := 0; level <= newLevel; level++ {
		inserted.forward[level] = update[level].forward[level]
		update[level].forward[level] = inserted
	}

	s.size++
	s.byteSize += len(key) + valueLen(value) + nodeOverhead
}

// Get returns the stored value and a state marker.
func (s *SkipList) Get(key string) (string, ValueState) {
	current := s.header

	for level := s.level; level >= 0; level-- {
		for current.forward[level] != nil && current.forward[level].key < key {
			current = current.forward[level]
		}
	}

	current = current.forward[0]
	if current == nil || current.key != key {
		return "", Missing
	}
	if current.value == nil {
		return "", Tombstone
	}
	return *current.value, Present
}

// Entries returns a materialized ordered view of the list.
func (s *SkipList) Entries() []Entry {
	entries := make([]Entry, 0, s.size)
	current := s.header.forward[0]
	for current != nil {
		entries = append(entries, Entry{Key: current.key, Value: current.value})
		current = current.forward[0]
	}
	return entries
}

// Size returns the number of logical records, including tombstones.
func (s *SkipList) Size() int {
	return s.size
}

// ByteSize returns approximate in-memory usage for flush threshold checks.
func (s *SkipList) ByteSize() int {
	return s.byteSize
}

// Clear resets the SkipList to an empty state.
func (s *SkipList) Clear() {
	s.level = 0
	s.header = newNode("", nil, maxLevel)
	s.size = 0
	s.byteSize = 0
}

func valueLen(value *string) int {
	if value == nil {
		return 0
	}
	return len(*value)
}
