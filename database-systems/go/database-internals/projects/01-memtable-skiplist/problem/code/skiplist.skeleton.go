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
	// TODO: 정렬 순서를 유지하면서 삽입하거나 갱신한다.
}

func (s *SkipList) Delete(key string) {
	// TODO: key를 제거하지 말고 tombstone으로 표시한다.
}

func (s *SkipList) Get(key string) (string, ValueState) {
	// TODO: present, tombstone, missing을 구분한다.
	return "", Missing
}

func (s *SkipList) Entries() []Entry {
	// TODO: 정렬된 순서로 entry를 반환한다.
	return nil
}

func (s *SkipList) Size() int {
	return 0
}

func (s *SkipList) ByteSize() int {
	return 0
}

func (s *SkipList) Clear() {}
