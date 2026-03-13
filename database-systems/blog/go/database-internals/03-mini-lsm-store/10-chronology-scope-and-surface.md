# 10 03 Mini LSM Store를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 여기서는 구현 세부사항을 서둘러 설명하지 않고, 무엇을 먼저 고정해야 하는지 범위부터 다시 좁힌다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

이번 세션의 목표는 `03 Mini LSM Store`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악하는 것이었다. 초기 가설은 README의 한 줄 설명만으로는 실제 핵심 invariant가 무엇인지 아직 흐릿했다.

막상 다시 펼쳐 보니 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. 특히 `TestPersistenceAfterReopen`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Put` 주변의 invariant를 고정하는 일이라는 게 보였다. 여기서 해석을 바꾼 단서는 `TestPutAndGet`는 가장 기본 표면을 보여 줬고, `TestPersistenceAfterReopen`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/database-internals/projects/03-mini-lsm-store/README.md`, `database-systems/go/database-internals/projects/03-mini-lsm-store/tests/lsm_store_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/mini-lsm-store/main.go
internal/lsmstore/store.go
internal/skiplist/skiplist.go
internal/sstable/sstable.go
tests/lsm_store_test.go
```

```bash
$ rg -n "^func Test" tests
tests/lsm_store_test.go:9:func TestPutAndGet(t *testing.T) {
tests/lsm_store_test.go:24:func TestMissingKey(t *testing.T) {
tests/lsm_store_test.go:35:func TestUpdate(t *testing.T) {
tests/lsm_store_test.go:52:func TestDelete(t *testing.T) {
tests/lsm_store_test.go:69:func TestFlushCreatesSSTable(t *testing.T) {
tests/lsm_store_test.go:81:func TestReadAfterForceFlush(t *testing.T) {
tests/lsm_store_test.go:101:func TestMemtableWinsOverSSTable(t *testing.T) {
tests/lsm_store_test.go:122:func TestTombstoneAcrossLevels(t *testing.T) {
tests/lsm_store_test.go:143:func TestPersistenceAfterReopen(t *testing.T) {
```

검증 신호:
- `TestPutAndGet`는 가장 기본 표면을 보여 줬고, `TestPersistenceAfterReopen`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Put` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestPersistenceAfterReopen(t *testing.T) {
	tempDir := t.TempDir()
	store := lsmstore.New(tempDir, 1024)
	if err := store.Open(); err != nil {
		t.Fatal(err)
	}
	if err := store.Put("persist", "me"); err != nil {
		t.Fatal(err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
```

왜 여기서 판단이 바뀌었는가:

`TestPersistenceAfterReopen`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Flush Lifecycle`에서 정리한 요점처럼, active MemTable은 write를 받는 유일한 구조다.

다음으로 넘긴 질문:
- `Put`와 `Get`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이 구간에서 먼저 붙잡으려 한 것은 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 처음 읽을 때는 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

그런데 가장 큰 구현 파일인 `database-systems/go/database-internals/projects/03-mini-lsm-store/internal/sstable/sstable.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `Put` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/database-internals/projects/03-mini-lsm-store/internal/sstable/sstable.go`

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
- `Put` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Get`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

왜 여기서 판단이 바뀌었는가:

`Put`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Read Path`에서 정리한 요점처럼, 먼저 active MemTable을 본다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `Get`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
