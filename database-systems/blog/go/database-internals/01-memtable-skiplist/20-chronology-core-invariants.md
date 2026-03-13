# 20 01 MemTable SkipList에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 여기서는 추상 설명을 줄이고, 실제 구현에서 invariant가 어디서 잠기는지 핵심 코드만 붙잡아 따라간다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Put에서 invariant가 잠기는 지점 보기

이 구간에서 먼저 붙잡으려 한 것은 `Put`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 처음 읽을 때는 `Put` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

그런데 `rg -n "Put|Delete" internal cmd`로 핵심 함수 위치를 다시 잡고, `Put`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `Put` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`의 `Put`

CLI:

```bash
$ rg -n "Put|Delete" internal cmd
internal/skiplist/skiplist.go:67:// Put은 live value를 삽입하거나 갱신한다.
internal/skiplist/skiplist.go:68:func (s *SkipList) Put(key, value string) {
internal/skiplist/skiplist.go:73:// Delete는 key를 제거하지 않고 tombstone으로 바꾼다.
internal/skiplist/skiplist.go:74:func (s *SkipList) Delete(key string) {
cmd/skiplist-demo/main.go:11:	list.Put("banana", "yellow")
cmd/skiplist-demo/main.go:12:	list.Put("apple", "green")
cmd/skiplist-demo/main.go:13:	list.Put("carrot", "orange")
cmd/skiplist-demo/main.go:14:	list.Delete("banana")
```

검증 신호:
- `Put` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `정렬된 문자열 키-값 엔트리를 유지하는 in-memory write structure를 설계합니다.`

핵심 코드:

```go
func (s *SkipList) Put(key, value string) {
	copyValue := value
	s.put(key, &copyValue)
}

// Delete는 key를 제거하지 않고 tombstone으로 바꾼다.
func (s *SkipList) Delete(key string) {
	s.put(key, nil)
}
```

왜 여기서 판단이 바뀌었는가:

`Put`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `SkipList Invariants`에서 정리한 요점처럼, level 0 연결 리스트는 전체 키 집합을 오름차순으로 포함한다.

다음으로 넘긴 질문:
- `Delete`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — Delete로 같은 규칙 다시 확인하기

여기서 가장 먼저 확인한 것은 `Delete`가 `Put`와 어떤 짝을 이루는지 확인한다. 처음에는 `Delete`는 단순 보조 함수일 거라고 생각했다.

하지만 실제로는 두 번째 앵커를 읽고 나니, 실제로는 `Put`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 결정적으로 방향을 잡아 준 신호는 `Delete`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`의 `Delete`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
internal/skiplist/skiplist.go:14:type ValueState int
internal/skiplist/skiplist.go:23:type Entry struct {
internal/skiplist/skiplist.go:28:type node struct {
internal/skiplist/skiplist.go:35:type SkipList struct {
internal/skiplist/skiplist.go:44:func New() *SkipList {
internal/skiplist/skiplist.go:51:func newNode(key string, value *string, level int) *node {
internal/skiplist/skiplist.go:59:func (s *SkipList) randomLevel() int {
internal/skiplist/skiplist.go:68:func (s *SkipList) Put(key, value string) {
internal/skiplist/skiplist.go:74:func (s *SkipList) Delete(key string) {
internal/skiplist/skiplist.go:78:func (s *SkipList) put(key string, value *string) {
internal/skiplist/skiplist.go:115:func (s *SkipList) Get(key string) (string, ValueState) {
internal/skiplist/skiplist.go:135:func (s *SkipList) Entries() []Entry {
internal/skiplist/skiplist.go:146:func (s *SkipList) Size() int {
internal/skiplist/skiplist.go:151:func (s *SkipList) ByteSize() int {
internal/skiplist/skiplist.go:156:func (s *SkipList) Clear() {
internal/skiplist/skiplist.go:163:func valueLen(value *string) int {
cmd/skiplist-demo/main.go:9:func main() {
```

검증 신호:
- `Delete`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestEntriesIncludeTombstones` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
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
```

왜 여기서 판단이 바뀌었는가:

`Delete`가 없으면 `Put`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `SkipList Invariants`에서 정리한 요점처럼, level 0 연결 리스트는 전체 키 집합을 오름차순으로 포함한다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
