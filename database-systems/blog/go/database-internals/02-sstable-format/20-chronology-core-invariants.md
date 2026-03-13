# 20 02 SSTable Format에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 기능 목록을 다시 적기보다, 규칙이 실제 코드에서 언제 강제되는지 보여 주는 데 초점을 둔다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Write에서 invariant가 잠기는 지점 보기

이번 세션의 목표는 `Write`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 초기 가설은 `Write` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

막상 다시 펼쳐 보니 `rg -n "Write|IndexEntry" internal cmd`로 핵심 함수 위치를 다시 잡고, `Write`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `Write` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`의 `Write`

CLI:

```bash
$ rg -n "Write|IndexEntry" internal cmd
internal/sstable/sstable.go:14:type IndexEntry struct {
internal/sstable/sstable.go:21:	Index            []IndexEntry
internal/sstable/sstable.go:30:func (table *SSTable) Write(records []serializer.Record) error {
internal/sstable/sstable.go:35:	indexEntries := make([]IndexEntry, 0, len(records))
internal/sstable/sstable.go:44:		indexEntries = append(indexEntries, IndexEntry{Key: record.Key, Offset: offset})
internal/sstable/sstable.go:132:	table.Index = make([]IndexEntry, 0, len(indexRecords))
internal/sstable/sstable.go:141:		table.Index = append(table.Index, IndexEntry{Key: record.Key, Offset: offset})
cmd/sstable-format/main.go:21:	err = table.Write([]serializer.Record{
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

왜 여기서 판단이 바뀌었는가:

`Write`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `SSTable Layout`에서 정리한 요점처럼, data section은 record를 연속 배치한 영역이다.

다음으로 넘긴 질문:
- `IndexEntry`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — IndexEntry로 같은 규칙 다시 확인하기

이 구간에서 먼저 붙잡으려 한 것은 `IndexEntry`가 `Write`와 어떤 짝을 이루는지 확인하는 것이었다. 처음 읽을 때는 `IndexEntry`는 단순 보조 함수일 거라고 생각했다.

그런데 두 번째 앵커를 읽고 나니, 실제로는 `Write`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `IndexEntry`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`의 `IndexEntry`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
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
cmd/sstable-format/main.go:12:func main() {
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

왜 여기서 판단이 바뀌었는가:

`IndexEntry`가 없으면 `Write`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `SSTable Layout`에서 정리한 요점처럼, data section은 record를 연속 배치한 영역이다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
