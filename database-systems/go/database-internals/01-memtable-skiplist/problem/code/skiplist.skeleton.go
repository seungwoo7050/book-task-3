package skiplist

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

type SkipList struct{}

func New() *SkipList {
	return &SkipList{}
}

func (s *SkipList) Put(key, value string) {
	// TODO: insert or update while preserving sort order.
}

func (s *SkipList) Delete(key string) {
	// TODO: mark a key as a tombstone rather than removing it.
}

func (s *SkipList) Get(key string) (string, ValueState) {
	// TODO: distinguish present, tombstone, and missing.
	return "", Missing
}

func (s *SkipList) Entries() []Entry {
	// TODO: return entries in sorted order.
	return nil
}

func (s *SkipList) Size() int {
	return 0
}

func (s *SkipList) ByteSize() int {
	return 0
}

func (s *SkipList) Clear() {}
