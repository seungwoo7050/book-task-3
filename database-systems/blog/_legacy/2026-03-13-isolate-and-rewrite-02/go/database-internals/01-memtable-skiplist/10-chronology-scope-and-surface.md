# 10 01 MemTable SkipList의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `01 MemTable SkipList`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/01-memtable-skiplist/README.md`, `database-systems/go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestEntriesIncludeTombstones`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Put` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/skiplist-demo/main.go
internal/skiplist/skiplist.go
tests/skiplist_test.go
```

```bash
$ rg -n "^func Test" tests
tests/skiplist_test.go:9:func TestPutAndGet(t *testing.T) {
tests/skiplist_test.go:22:func TestMissingKey(t *testing.T) {
tests/skiplist_test.go:31:func TestUpdateKeepsLogicalSize(t *testing.T) {
tests/skiplist_test.go:45:func TestManyInserts(t *testing.T) {
tests/skiplist_test.go:59:func TestDeleteProducesTombstone(t *testing.T) {
tests/skiplist_test.go:73:func TestEntriesStaySorted(t *testing.T) {
tests/skiplist_test.go:88:func TestEntriesIncludeTombstones(t *testing.T) {
tests/skiplist_test.go:103:func TestByteSizeTracking(t *testing.T) {
tests/skiplist_test.go:115:func TestClear(t *testing.T) {
```

검증 신호:

- `TestPutAndGet`는 가장 기본 표면을 보여 줬고, `TestEntriesIncludeTombstones`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Put` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestEntriesIncludeTombstones(t *testing.T) {
	list := skiplist.New()
	list.Put("x", "1")
	list.Put("y", "2")
	list.Delete("x")

	entries := list.Entries()
	if len(entries) != 2 {
		t.Fatalf("expected 2 entries, got %d", len(entries))
	}
	if entries[0].Value != nil {
		t.Fatalf("expected first entry to be a tombstone")
	}
}
```

왜 이 코드가 중요했는가:

`TestEntriesIncludeTombstones`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `SkipList Invariants`에서 정리한 요점처럼, level 0 연결 리스트는 전체 키 집합을 오름차순으로 포함한다.

다음:

- `Put`와 `Delete`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/skiplist-demo/main.go:9:func main() {
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
```

검증 신호:

- `Put` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Delete`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

왜 이 코드가 중요했는가:

`Put`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `SkipList Invariants`에서 정리한 요점처럼, level 0 연결 리스트는 전체 키 집합을 오름차순으로 포함한다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `Delete`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
