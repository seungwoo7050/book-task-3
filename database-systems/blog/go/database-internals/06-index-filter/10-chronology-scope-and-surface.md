# 10 06 Index Filter를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 설명문을 믿고 곧장 구현으로 들어가기보다, 테스트와 파일 구조를 다시 읽으면서 어디서부터 이야기를 시작해야 하는지 정리한다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

여기서 가장 먼저 확인한 것은 `06 Index Filter`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다. 처음에는 README의 한 줄 설명만으로는 실제 핵심 invariant가 무엇인지 아직 흐릿했다.

하지만 실제로는 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestSSTableBloomRejectAndBoundedScan`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Filter` 주변의 invariant를 고정하는 일이라는 게 보였다. 결정적으로 방향을 잡아 준 신호는 `TestBloomFilterHasNoFalseNegatives`는 가장 기본 표면을 보여 줬고, `TestSSTableBloomRejectAndBoundedScan`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/database-internals/projects/06-index-filter/README.md`, `database-systems/go/database-internals/projects/06-index-filter/tests/index_filter_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/index-filter/main.go
internal/bloomfilter/bloom_filter.go
internal/sparseindex/sparse_index.go
internal/sstable/sstable.go
tests/index_filter_test.go
```

```bash
$ rg -n "^func Test" tests
tests/index_filter_test.go:13:func TestBloomFilterHasNoFalseNegatives(t *testing.T) {
tests/index_filter_test.go:28:func TestBloomFilterFalsePositiveRateIsBounded(t *testing.T) {
tests/index_filter_test.go:47:func TestSparseIndexFindsExpectedBlock(t *testing.T) {
tests/index_filter_test.go:64:func TestSSTableBloomRejectAndBoundedScan(t *testing.T) {
```

검증 신호:
- `TestBloomFilterHasNoFalseNegatives`는 가장 기본 표면을 보여 줬고, `TestSSTableBloomRejectAndBoundedScan`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Filter` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestSSTableBloomRejectAndBoundedScan(t *testing.T) {
	tempDir := t.TempDir()
	table := sstable.New(filepath.Join(tempDir, "index.sst"), 8)
	records := make([]serializer.Record, 0, 64)
	for i := 0; i < 64; i++ {
		records = append(records, serializer.Record{
			Key:   fmtKey(i),
			Value: serializer.StringPtr("value-" + fmtKey(i)),
		})
	}
	if err := table.Write(records); err != nil {
		t.Fatalf("write table: %v", err)
	}
```

왜 여기서 판단이 바뀌었는가:

`TestSSTableBloomRejectAndBoundedScan`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Bloom Filter Sizing`에서 정리한 요점처럼, Bloom filter는 false negative가 없어야 하고, false positive는 허용 가능한 수준으로만 남아야 한다. 이 프로젝트는 레거시와 같은 식을 사용한다.

다음으로 넘긴 질문:
- `Filter`와 `Serialize`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이번 세션의 목표는 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 초기 가설은 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

막상 다시 펼쳐 보니 가장 큰 구현 파일인 `database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `Filter` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/index-filter/main.go:11:func main() {
internal/sparseindex/sparse_index.go:9:type Entry struct {
internal/sparseindex/sparse_index.go:14:type Range struct {
internal/sparseindex/sparse_index.go:19:type Index struct {
internal/sparseindex/sparse_index.go:24:func New(blockSize int) *Index {
internal/sparseindex/sparse_index.go:31:func (index *Index) Build(entries []Entry) {
internal/sparseindex/sparse_index.go:40:func (index *Index) FindBlock(key string, dataSize int64) (Range, bool) {
internal/sparseindex/sparse_index.go:69:func (index *Index) Serialize() ([]byte, error) {
internal/sparseindex/sparse_index.go:78:func Deserialize(buffer []byte, blockSize int) (*Index, error) {
internal/sstable/sstable.go:16:type LookupStats struct {
internal/sstable/sstable.go:22:type Table struct {
internal/sstable/sstable.go:34:func New(filePath string, blockSize int) *Table {
internal/sstable/sstable.go:41:func (table *Table) Write(records []serializer.Record) error {
internal/sstable/sstable.go:107:func (table *Table) Load() error {
internal/sstable/sstable.go:154:func (table *Table) Get(key string) (*string, bool, error) {
internal/sstable/sstable.go:159:func (table *Table) GetWithStats(key string) (*string, bool, LookupStats, error) {
internal/sstable/sstable.go:205:func validateSorted(records []serializer.Record) error {
internal/bloomfilter/bloom_filter.go:11:type Filter struct {
internal/bloomfilter/bloom_filter.go:17:func New(expectedItems int, falsePositiveRate float64) *Filter {
internal/bloomfilter/bloom_filter.go:38:func (filter *Filter) Add(key string) {
internal/bloomfilter/bloom_filter.go:44:func (filter *Filter) MightContain(key string) bool {
internal/bloomfilter/bloom_filter.go:53:func (filter *Filter) Serialize() []byte {
internal/bloomfilter/bloom_filter.go:61:func Deserialize(buffer []byte) (*Filter, error) {
internal/bloomfilter/bloom_filter.go:76:func (filter *Filter) positions(key string) []uint32 {
internal/bloomfilter/bloom_filter.go:86:func (filter *Filter) setBit(position uint32) {
internal/bloomfilter/bloom_filter.go:92:func (filter *Filter) getBit(position uint32) bool {
```

검증 신호:
- `Filter` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Serialize`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
type Filter struct {
	BitCount      uint32
	HashFunctions uint32
	bits          []byte
}

func New(expectedItems int, falsePositiveRate float64) *Filter {
	if expectedItems <= 0 {
		expectedItems = 1
	}
	if falsePositiveRate <= 0 || falsePositiveRate >= 1 {
		falsePositiveRate = 0.01
	}
```

왜 여기서 판단이 바뀌었는가:

`Filter`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Sparse Index Scan`에서 정리한 요점처럼, sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `Serialize`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
