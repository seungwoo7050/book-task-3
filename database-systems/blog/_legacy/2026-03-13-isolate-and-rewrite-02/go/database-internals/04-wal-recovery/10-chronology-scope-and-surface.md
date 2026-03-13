# 10 04 WAL Recovery의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `04 WAL Recovery`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/04-wal-recovery/README.md`, `database-systems/go/database-internals/projects/04-wal-recovery/tests/wal_test.go`
- 처음 가설:
  README의 한 줄 설명만으로는 실제 핵심 invariant가 무엇인지 아직 흐릿했다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestForceFlushRotatesWAL`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `AppendPut` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/wal-recovery/main.go
internal/skiplist/skiplist.go
internal/sstable/sstable.go
internal/store/store.go
internal/wal/wal.go
tests/wal_test.go
```

```bash
$ rg -n "^func Test" tests
tests/wal_test.go:12:func TestRecoverPutRecords(t *testing.T) {
tests/wal_test.go:27:func TestRecoverDeleteRecords(t *testing.T) {
tests/wal_test.go:42:func TestRecoverManyRecords(t *testing.T) {
tests/wal_test.go:58:func TestStopAtCorruptedRecord(t *testing.T) {
tests/wal_test.go:79:func TestRecoverNonexistentAndTruncated(t *testing.T) {
tests/wal_test.go:95:func TestStoreRecoversFromWALAfterReopen(t *testing.T) {
tests/wal_test.go:111:func TestForceFlushRotatesWAL(t *testing.T) {
```

검증 신호:

- `TestRecoverPutRecords`는 가장 기본 표면을 보여 줬고, `TestForceFlushRotatesWAL`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `AppendPut` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestForceFlushRotatesWAL(t *testing.T) {
	tempDir := t.TempDir()
	durable := store.New(tempDir, 4096, false)
	mustNoErr(t, durable.Open())
	mustNoErr(t, durable.Put("alpha", "1"))
	mustNoErr(t, durable.ForceFlush())

	info, err := os.Stat(filepath.Join(tempDir, "active.wal"))
	mustNoErr(t, err)
	if info.Size() != 0 {
		t.Fatalf("expected fresh empty wal after rotation, got %d bytes", info.Size())
	}
```

왜 이 코드가 중요했는가:

`TestForceFlushRotatesWAL`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Recovery Policy`에서 정리한 요점처럼, header가 13바이트보다 짧으면 truncated header로 보고 중단한다.

다음:

- `AppendPut`와 `Recover`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/04-wal-recovery/internal/sstable/sstable.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/database-internals/projects/04-wal-recovery/internal/sstable/sstable.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/wal-recovery/main.go:10:func main() {
cmd/wal-recovery/main.go:39:func must(err error) {
internal/store/store.go:17:type DurableStore struct {
internal/store/store.go:27:func New(dataDir string, memtableSizeThreshold int, fsyncEnabled bool) *DurableStore {
internal/store/store.go:42:func (store *DurableStore) Open() error {
internal/store/store.go:80:func (store *DurableStore) Put(key, value string) error {
internal/store/store.go:88:func (store *DurableStore) Delete(key string) error {
internal/store/store.go:96:func (store *DurableStore) Get(key string) (*string, bool, error) {
internal/store/store.go:112:func (store *DurableStore) ForceFlush() error {
internal/store/store.go:140:func (store *DurableStore) Close() error {
internal/store/store.go:144:func (store *DurableStore) maybeFlush() error {
internal/store/store.go:151:func reverseTables(tables []*sstable.SSTable) {
internal/wal/wal.go:18:type Record struct {
internal/wal/wal.go:24:type WriteAheadLog struct {
internal/wal/wal.go:30:func New(filePath string, fsyncEnabled bool) *WriteAheadLog {
internal/wal/wal.go:37:func (log *WriteAheadLog) Open() error {
internal/wal/wal.go:42:func (log *WriteAheadLog) AppendPut(key, value string) error {
internal/wal/wal.go:47:func (log *WriteAheadLog) AppendDelete(key string) error {
internal/wal/wal.go:51:func (log *WriteAheadLog) Recover() ([]Record, error) {
internal/wal/wal.go:112:func (log *WriteAheadLog) Close() error {
internal/wal/wal.go:121:func (log *WriteAheadLog) appendRecord(recordType byte, key string, value *string) error {
internal/skiplist/skiplist.go:11:type ValueState int
internal/skiplist/skiplist.go:19:type Entry struct {
internal/skiplist/skiplist.go:24:type node struct {
internal/skiplist/skiplist.go:30:type SkipList struct {
internal/skiplist/skiplist.go:38:func New() *SkipList {
internal/skiplist/skiplist.go:45:func newNode(key string, value *string, level int) *node {
internal/skiplist/skiplist.go:53:func (list *SkipList) Put(key, value string) {
internal/skiplist/skiplist.go:58:func (list *SkipList) Delete(key string) {
internal/skiplist/skiplist.go:62:func (list *SkipList) put(key string, value *string) {
internal/skiplist/skiplist.go:97:func (list *SkipList) Get(key string) (*string, ValueState) {
internal/skiplist/skiplist.go:114:func (list *SkipList) Entries() []Entry {
internal/skiplist/skiplist.go:124:func (list *SkipList) Size() int {
internal/skiplist/skiplist.go:128:func (list *SkipList) ByteSize() int {
internal/skiplist/skiplist.go:132:func (list *SkipList) Clear() {
internal/skiplist/skiplist.go:139:func (list *SkipList) randomLevel() int {
internal/skiplist/skiplist.go:147:func valueLen(value *string) int {
internal/sstable/sstable.go:14:type IndexEntry struct {
internal/sstable/sstable.go:19:type SSTable struct {
internal/sstable/sstable.go:24:func New(filePath string) *SSTable {
internal/sstable/sstable.go:28:func (table *SSTable) Write(records []serializer.Record) error {
internal/sstable/sstable.go:80:func (table *SSTable) LoadIndex() error {
internal/sstable/sstable.go:124:func (table *SSTable) Lookup(key string) (*string, bool, error) {
internal/sstable/sstable.go:157:func FileName(dataDir string, sequence int) string {
internal/sstable/sstable.go:161:func (table *SSTable) binarySearch(key string) int {
```

검증 신호:

- `AppendPut` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Recover`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
func (log *WriteAheadLog) AppendPut(key, value string) error {
	copyValue := value
	return log.appendRecord(OpPut, key, &copyValue)
}

func (log *WriteAheadLog) AppendDelete(key string) error {
	return log.appendRecord(OpDelete, key, nil)
}

func (log *WriteAheadLog) Recover() ([]Record, error) {
	handle := fileio.NewHandle(log.FilePath)
	if err := handle.Open("r"); err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return []Record{}, nil
```

왜 이 코드가 중요했는가:

`AppendPut`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `WAL Record Format`에서 정리한 요점처럼, record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `Recover`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
