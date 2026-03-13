# 20 04 WAL Recovery의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `AppendPut`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/04-wal-recovery/internal/wal/wal.go`의 `AppendPut`
- 처음 가설:
  `AppendPut` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "AppendPut|Recover" internal cmd`로 핵심 함수 위치를 다시 잡고, `AppendPut`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "AppendPut|Recover" internal cmd
internal/store/store.go:65:	records, err := wal.New(store.WALPath, false).Recover()
internal/store/store.go:81:	if err := store.writeAheadLog.AppendPut(key, value); err != nil {
internal/wal/wal.go:42:func (log *WriteAheadLog) AppendPut(key, value string) error {
internal/wal/wal.go:51:func (log *WriteAheadLog) Recover() ([]Record, error) {
```

검증 신호:

- `AppendPut` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `acknowledged write를 잃지 않기 위한 append-before-apply 순서를 익힙니다.`

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

`AppendPut`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `WAL Record Format`에서 정리한 요점처럼, record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.

다음:

- `Recover`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `Recover`가 `AppendPut`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/04-wal-recovery/internal/wal/wal.go`의 `Recover`
- 처음 가설:
  `Recover`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `AppendPut`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

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

- `Recover`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestForceFlushRotatesWAL` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (log *WriteAheadLog) Recover() ([]Record, error) {
	handle := fileio.NewHandle(log.FilePath)
	if err := handle.Open("r"); err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return []Record{}, nil
		}
		return nil, err
	}
	defer handle.Close()
```

왜 이 코드가 중요했는가:

`Recover`가 없으면 `AppendPut`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `WAL Record Format`에서 정리한 요점처럼, record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
