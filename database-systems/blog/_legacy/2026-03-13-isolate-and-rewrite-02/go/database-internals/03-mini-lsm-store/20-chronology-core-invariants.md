# 20 03 Mini LSM Store의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `Put`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore/store.go`의 `Put`
- 처음 가설:
  `Put` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "Put|Get" internal cmd`로 핵심 함수 위치를 다시 잡고, `Put`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "Put|Get" internal cmd
internal/skiplist/skiplist.go:53:func (list *SkipList) Put(key, value string) {
internal/skiplist/skiplist.go:98:func (list *SkipList) Get(key string) (*string, ValueState) {
cmd/mini-lsm-store/main.go:22:	must(store.Put("apple", "green"))
cmd/mini-lsm-store/main.go:23:	must(store.Put("banana", "yellow"))
cmd/mini-lsm-store/main.go:25:	must(store.Put("banana", "ripe"))
cmd/mini-lsm-store/main.go:34:	value, found, err := store.Get(key)
internal/lsmstore/store.go:66:func (store *LSMStore) Put(key, value string) error {
internal/lsmstore/store.go:67:	store.Memtable.Put(key, value)
internal/lsmstore/store.go:76:func (store *LSMStore) Get(key string) (*string, bool, error) {
internal/lsmstore/store.go:77:	if value, state := store.Memtable.Get(key); state != skiplist.Missing {
internal/lsmstore/store.go:82:		if value, state := store.ImmutableMemtable.Get(key); state != skiplist.Missing {
internal/sstable/sstable.go:55:	binary.BigEndian.PutUint32(footer[0:4], uint32(len(dataSection)))
internal/sstable/sstable.go:56:	binary.BigEndian.PutUint32(footer[4:8], uint32(len(indexSection)))
```

검증 신호:

- `Put` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `active memtable이 threshold를 넘을 때 immutable swap과 flush가 어떻게 이어지는지 익힙니다.`

핵심 코드:

```go
func (store *LSMStore) Put(key, value string) error {
	store.Memtable.Put(key, value)
	return store.maybeFlush()
}

func (store *LSMStore) Delete(key string) error {
	store.Memtable.Delete(key)
	return store.maybeFlush()
}
```

왜 이 코드가 중요했는가:

`Put`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Read Path`에서 정리한 요점처럼, 먼저 active MemTable을 본다.

다음:

- `Get`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `Get`가 `Put`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore/store.go`의 `Get`
- 처음 가설:
  `Get`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `Put`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/mini-lsm-store/main.go:10:func main() {
cmd/mini-lsm-store/main.go:33:func printLookup(store *lsmstore.LSMStore, key string) {
cmd/mini-lsm-store/main.go:48:func must(err error) {
internal/skiplist/skiplist.go:11:type ValueState int
internal/skiplist/skiplist.go:19:type Entry struct {
internal/skiplist/skiplist.go:24:type node struct {
internal/skiplist/skiplist.go:30:type SkipList struct {
internal/skiplist/skiplist.go:38:func New() *SkipList {
internal/skiplist/skiplist.go:45:func newNode(key string, value *string, level int) *node {
internal/skiplist/skiplist.go:53:func (list *SkipList) Put(key, value string) {
internal/skiplist/skiplist.go:58:func (list *SkipList) Delete(key string) {
internal/skiplist/skiplist.go:62:func (list *SkipList) put(key string, value *string) {
internal/skiplist/skiplist.go:98:func (list *SkipList) Get(key string) (*string, ValueState) {
internal/skiplist/skiplist.go:116:func (list *SkipList) Entries() []Entry {
internal/skiplist/skiplist.go:126:func (list *SkipList) Size() int {
internal/skiplist/skiplist.go:130:func (list *SkipList) ByteSize() int {
internal/skiplist/skiplist.go:134:func (list *SkipList) Clear() {
internal/skiplist/skiplist.go:141:func (list *SkipList) randomLevel() int {
internal/skiplist/skiplist.go:149:func valueLen(value *string) int {
internal/sstable/sstable.go:14:type IndexEntry struct {
internal/sstable/sstable.go:19:type SSTable struct {
internal/sstable/sstable.go:24:func New(filePath string) *SSTable {
internal/sstable/sstable.go:28:func (table *SSTable) Write(records []serializer.Record) error {
internal/sstable/sstable.go:81:func (table *SSTable) LoadIndex() error {
internal/sstable/sstable.go:126:func (table *SSTable) Lookup(key string) (*string, bool, error) {
internal/sstable/sstable.go:159:func (table *SSTable) ReadAll() ([]serializer.Record, error) {
internal/sstable/sstable.go:186:func FileName(dataDir string, sequence int) string {
internal/sstable/sstable.go:190:func (table *SSTable) binarySearch(key string) int {
internal/lsmstore/store.go:16:type LSMStore struct {
internal/lsmstore/store.go:25:func New(dataDir string, memtableSizeThreshold int) *LSMStore {
internal/lsmstore/store.go:37:func (store *LSMStore) Open() error {
internal/lsmstore/store.go:66:func (store *LSMStore) Put(key, value string) error {
internal/lsmstore/store.go:71:func (store *LSMStore) Delete(key string) error {
internal/lsmstore/store.go:76:func (store *LSMStore) Get(key string) (*string, bool, error) {
internal/lsmstore/store.go:100:func (store *LSMStore) ForceFlush() error {
internal/lsmstore/store.go:107:func (store *LSMStore) Close() error {
internal/lsmstore/store.go:111:func (store *LSMStore) maybeFlush() error {
internal/lsmstore/store.go:118:func (store *LSMStore) flush() error {
internal/lsmstore/store.go:139:func reverseTables(tables []*sstable.SSTable) {
```

검증 신호:

- `Get`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestPersistenceAfterReopen` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (store *LSMStore) Get(key string) (*string, bool, error) {
	if value, state := store.Memtable.Get(key); state != skiplist.Missing {
		return value, true, nil
	}

	if store.ImmutableMemtable != nil {
		if value, state := store.ImmutableMemtable.Get(key); state != skiplist.Missing {
			return value, true, nil
		}
	}
```

왜 이 코드가 중요했는가:

`Get`가 없으면 `Put`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Read Path`에서 정리한 요점처럼, 먼저 active MemTable을 본다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
