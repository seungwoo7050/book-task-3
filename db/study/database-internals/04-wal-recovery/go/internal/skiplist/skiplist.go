package skiplist

import "math/rand"

const (
	maxLevel     = 16
	probability  = 0.5
	nodeOverhead = 64
)

type ValueState int

const (
	Missing ValueState = iota
	Present
	Tombstone
)

type Entry struct {
	Key   string
	Value *string
}

type node struct {
	key     string
	value   *string
	forward []*node
}

type SkipList struct {
	rng      *rand.Rand
	level    int
	header   *node
	size     int
	byteSize int
}

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

func (list *SkipList) Put(key, value string) {
	copyValue := value
	list.put(key, &copyValue)
}

func (list *SkipList) Delete(key string) {
	list.put(key, nil)
}

func (list *SkipList) put(key string, value *string) {
	update := make([]*node, maxLevel+1)
	current := list.header
	for level := list.level; level >= 0; level-- {
		for current.forward[level] != nil && current.forward[level].key < key {
			current = current.forward[level]
		}
		update[level] = current
	}

	current = current.forward[0]
	if current != nil && current.key == key {
		list.byteSize += valueLen(value) - valueLen(current.value)
		current.value = value
		return
	}

	newLevel := list.randomLevel()
	if newLevel > list.level {
		for level := list.level + 1; level <= newLevel; level++ {
			update[level] = list.header
		}
		list.level = newLevel
	}

	inserted := newNode(key, value, newLevel)
	for level := 0; level <= newLevel; level++ {
		inserted.forward[level] = update[level].forward[level]
		update[level].forward[level] = inserted
	}

	list.size++
	list.byteSize += len(key) + valueLen(value) + nodeOverhead
}

func (list *SkipList) Get(key string) (*string, ValueState) {
	current := list.header
	for level := list.level; level >= 0; level-- {
		for current.forward[level] != nil && current.forward[level].key < key {
			current = current.forward[level]
		}
	}
	current = current.forward[0]
	if current == nil || current.key != key {
		return nil, Missing
	}
	if current.value == nil {
		return nil, Tombstone
	}
	return current.value, Present
}

func (list *SkipList) Entries() []Entry {
	result := make([]Entry, 0, list.size)
	current := list.header.forward[0]
	for current != nil {
		result = append(result, Entry{Key: current.key, Value: current.value})
		current = current.forward[0]
	}
	return result
}

func (list *SkipList) Size() int {
	return list.size
}

func (list *SkipList) ByteSize() int {
	return list.byteSize
}

func (list *SkipList) Clear() {
	list.level = 0
	list.header = newNode("", nil, maxLevel)
	list.size = 0
	list.byteSize = 0
}

func (list *SkipList) randomLevel() int {
	level := 0
	for level < maxLevel && list.rng.Float64() < probability {
		level++
	}
	return level
}

func valueLen(value *string) int {
	if value == nil {
		return 0
	}
	return len(*value)
}
