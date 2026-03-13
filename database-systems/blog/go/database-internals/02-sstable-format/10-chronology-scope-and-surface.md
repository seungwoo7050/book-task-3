# 10 02 SSTable Format를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 설명문을 믿고 곧장 구현으로 들어가기보다, 테스트와 파일 구조를 다시 읽으면서 어디서부터 이야기를 시작해야 하는지 정리한다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

여기서 가장 먼저 확인한 것은 `02 SSTable Format`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다. 처음에는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

하지만 실제로는 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestTombstones`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Write` 주변의 invariant를 고정하는 일이라는 게 보였다. 결정적으로 방향을 잡아 준 신호는 `TestReadAll`는 가장 기본 표면을 보여 줬고, `TestTombstones`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/database-internals/projects/02-sstable-format/README.md`, `database-systems/go/database-internals/projects/02-sstable-format/tests/sstable_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/sstable-format/main.go
internal/sstable/sstable.go
tests/sstable_test.go
```

```bash
$ rg -n "^func Test" tests
tests/sstable_test.go:12:func TestRoundTripSortedEntries(t *testing.T) {
tests/sstable_test.go:40:func TestMissingKey(t *testing.T) {
tests/sstable_test.go:63:func TestTombstones(t *testing.T) {
tests/sstable_test.go:89:func TestReadAll(t *testing.T) {
tests/sstable_test.go:112:func TestLargeDataset(t *testing.T) {
tests/sstable_test.go:143:func TestMalformedFooter(t *testing.T) {
```

검증 신호:
- `TestReadAll`는 가장 기본 표면을 보여 줬고, `TestTombstones`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Write` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestTombstones(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	table := sstable.New(filePath)
	if err := table.Write([]serializer.Record{
		{Key: "alive", Value: serializer.StringPtr("yes")},
		{Key: "dead", Value: nil},
	}); err != nil {
		t.Fatalf("write failed: %v", err)
	}
```

왜 여기서 판단이 바뀌었는가:

`TestTombstones`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Lookup Path`에서 정리한 요점처럼, reopen 시점에는 footer를 읽어 index section 위치를 계산한다.

다음으로 넘긴 질문:
- `Write`와 `IndexEntry`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이번 세션의 목표는 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 초기 가설은 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

막상 다시 펼쳐 보니 가장 큰 구현 파일인 `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `Write` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go`

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
- `Write` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `IndexEntry`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`Write`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `SSTable Layout`에서 정리한 요점처럼, data section은 record를 연속 배치한 영역이다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `IndexEntry`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
