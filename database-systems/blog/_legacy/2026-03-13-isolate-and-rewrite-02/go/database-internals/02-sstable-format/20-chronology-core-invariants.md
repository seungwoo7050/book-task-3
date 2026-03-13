# 20 02 SSTable Format의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `Write`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`의 `Write`
- 처음 가설:
  `Write` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "Write|IndexEntry" internal cmd`로 핵심 함수 위치를 다시 잡고, `Write`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "Write|IndexEntry" internal cmd
cmd/sstable-format/main.go:21:	err = table.Write([]serializer.Record{
internal/sstable/sstable.go:14:type IndexEntry struct {
internal/sstable/sstable.go:21:	Index            []IndexEntry
internal/sstable/sstable.go:30:func (table *SSTable) Write(records []serializer.Record) error {
internal/sstable/sstable.go:35:	indexEntries := make([]IndexEntry, 0, len(records))
internal/sstable/sstable.go:44:		indexEntries = append(indexEntries, IndexEntry{Key: record.Key, Offset: offset})
internal/sstable/sstable.go:132:	table.Index = make([]IndexEntry, 0, len(indexRecords))
internal/sstable/sstable.go:141:		table.Index = append(table.Index, IndexEntry{Key: record.Key, Offset: offset})
```

검증 신호:

- `Write` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `정렬된 record stream을 immutable file format으로 저장하는 방법을 익힙니다.`

핵심 코드:

```go
func (table *SSTable) Write(records []serializer.Record) error {
	if err := validateSorted(records); err != nil {
		return err
	}

	indexEntries := make([]IndexEntry, 0, len(records))
	dataSection := make([]byte, 0)
	var offset int64

	for _, record := range records {
		encoded, err := serializer.EncodeRecord(record)
		if err != nil {
			return err
		}
```

왜 이 코드가 중요했는가:

`Write`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `SSTable Layout`에서 정리한 요점처럼, data section은 record를 연속 배치한 영역이다.

다음:

- `IndexEntry`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `IndexEntry`가 `Write`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`의 `IndexEntry`
- 처음 가설:
  `IndexEntry`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `Write`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/sstable-format/main.go:12:func main() {
internal/sstable/sstable.go:14:type IndexEntry struct {
internal/sstable/sstable.go:19:type SSTable struct {
internal/sstable/sstable.go:26:func New(filePath string) *SSTable {
internal/sstable/sstable.go:30:func (table *SSTable) Write(records []serializer.Record) error {
internal/sstable/sstable.go:94:func (table *SSTable) LoadIndex() error {
internal/sstable/sstable.go:148:func (table *SSTable) Lookup(key string) (*string, bool, error) {
internal/sstable/sstable.go:187:func (table *SSTable) ReadAll() ([]serializer.Record, error) {
internal/sstable/sstable.go:219:func (table *SSTable) binarySearch(key string) int {
internal/sstable/sstable.go:237:func validateSorted(records []serializer.Record) error {
internal/sstable/sstable.go:246:func FileName(dataDir string, sequence int) string {
```

검증 신호:

- `IndexEntry`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestTombstones` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
type IndexEntry struct {
	Key    string
	Offset int64
}

type SSTable struct {
	FilePath         string
	Index            []IndexEntry
	dataSectionSize  int64
	indexSectionSize int64
}
```

왜 이 코드가 중요했는가:

`IndexEntry`가 없으면 `Write`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `SSTable Layout`에서 정리한 요점처럼, data section은 record를 연속 배치한 영역이다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
