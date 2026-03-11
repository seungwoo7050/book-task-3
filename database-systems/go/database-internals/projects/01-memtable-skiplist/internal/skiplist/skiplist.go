package skiplist

import (
	"math/rand"
)

const (
	maxLevel     = 16
	probability  = 0.5
	nodeOverhead = 64
)

// ValueState는 live value, tombstone, missing key를 구분한다.
type ValueState int

const (
	Missing ValueState = iota
	Present
	Tombstone
)

// Entry는 하나의 논리적 MemTable record를 표현한다.
type Entry struct {
	Key   string
	Value *string
}

type node struct {
	key     string
	value   *string
	forward []*node
}

// SkipList는 MemTable 단계에서 정렬된 key-value record를 저장한다.
type SkipList struct {
	rng      *rand.Rand
	level    int
	header   *node
	size     int
	byteSize int
}

// New는 deterministic level generation을 쓰는 빈 SkipList를 반환한다.
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

// Put은 live value를 삽입하거나 갱신한다.
func (s *SkipList) Put(key, value string) {
	copyValue := value
	s.put(key, &copyValue)
}

// Delete는 key를 제거하지 않고 tombstone으로 바꾼다.
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

// Get은 저장된 값과 상태 marker를 함께 반환한다.
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

// Entries는 list를 materialized ordered view로 반환한다.
func (s *SkipList) Entries() []Entry {
	entries := make([]Entry, 0, s.size)
	current := s.header.forward[0]
	for current != nil {
		entries = append(entries, Entry{Key: current.key, Value: current.value})
		current = current.forward[0]
	}
	return entries
}

// Size는 tombstone을 포함한 논리 record 수를 반환한다.
func (s *SkipList) Size() int {
	return s.size
}

// ByteSize는 flush threshold 확인에 쓰는 대략적인 in-memory usage를 반환한다.
func (s *SkipList) ByteSize() int {
	return s.byteSize
}

// Clear는 SkipList를 빈 상태로 되돌린다.
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
