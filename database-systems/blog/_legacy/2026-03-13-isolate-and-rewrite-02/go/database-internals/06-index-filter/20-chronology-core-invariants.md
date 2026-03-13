# 20 06 Index Filter의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `Filter`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go`의 `Filter`
- 처음 가설:
  `Filter` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "Filter|Serialize" internal cmd`로 핵심 함수 위치를 다시 잡고, `Filter`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "Filter|Serialize" internal cmd
internal/sparseindex/sparse_index.go:69:func (index *Index) Serialize() ([]byte, error) {
internal/bloomfilter/bloom_filter.go:11:type Filter struct {
internal/bloomfilter/bloom_filter.go:17:func New(expectedItems int, falsePositiveRate float64) *Filter {
internal/bloomfilter/bloom_filter.go:31:	return &Filter{
internal/bloomfilter/bloom_filter.go:38:func (filter *Filter) Add(key string) {
internal/bloomfilter/bloom_filter.go:44:func (filter *Filter) MightContain(key string) bool {
internal/bloomfilter/bloom_filter.go:53:func (filter *Filter) Serialize() []byte {
internal/bloomfilter/bloom_filter.go:61:func Deserialize(buffer []byte) (*Filter, error) {
internal/bloomfilter/bloom_filter.go:65:	filter := &Filter{
internal/bloomfilter/bloom_filter.go:76:func (filter *Filter) positions(key string) []uint32 {
internal/bloomfilter/bloom_filter.go:86:func (filter *Filter) setBit(position uint32) {
internal/bloomfilter/bloom_filter.go:92:func (filter *Filter) getBit(position uint32) bool {
internal/sstable/sstable.go:30:	Filter      *bloomfilter.Filter
internal/sstable/sstable.go:64:	indexBytes, err := index.Serialize()
internal/sstable/sstable.go:68:	filterBytes := filter.Serialize()
internal/sstable/sstable.go:75:	table.Filter = filter
internal/sstable/sstable.go:141:	table.Filter, err = bloomfilter.Deserialize(filterBytes)
internal/sstable/sstable.go:160:	if table.Filter == nil || table.Index == nil {
internal/sstable/sstable.go:166:	if !table.Filter.MightContain(key) {
```

검증 신호:

- `Filter` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `Bloom filter가 negative lookup 비용을 어떻게 줄이는지 이해합니다.`

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

왜 이 코드가 중요했는가:

`Filter`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Sparse Index Scan`에서 정리한 요점처럼, sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

다음:

- `Serialize`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `Serialize`가 `Filter`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go`의 `Serialize`
- 처음 가설:
  `Serialize`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `Filter`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

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
internal/bloomfilter/bloom_filter.go:11:type Filter struct {
internal/bloomfilter/bloom_filter.go:17:func New(expectedItems int, falsePositiveRate float64) *Filter {
internal/bloomfilter/bloom_filter.go:38:func (filter *Filter) Add(key string) {
internal/bloomfilter/bloom_filter.go:44:func (filter *Filter) MightContain(key string) bool {
internal/bloomfilter/bloom_filter.go:53:func (filter *Filter) Serialize() []byte {
internal/bloomfilter/bloom_filter.go:61:func Deserialize(buffer []byte) (*Filter, error) {
internal/bloomfilter/bloom_filter.go:76:func (filter *Filter) positions(key string) []uint32 {
internal/bloomfilter/bloom_filter.go:86:func (filter *Filter) setBit(position uint32) {
internal/bloomfilter/bloom_filter.go:92:func (filter *Filter) getBit(position uint32) bool {
internal/sstable/sstable.go:16:type LookupStats struct {
internal/sstable/sstable.go:22:type Table struct {
internal/sstable/sstable.go:34:func New(filePath string, blockSize int) *Table {
internal/sstable/sstable.go:41:func (table *Table) Write(records []serializer.Record) error {
internal/sstable/sstable.go:107:func (table *Table) Load() error {
internal/sstable/sstable.go:154:func (table *Table) Get(key string) (*string, bool, error) {
internal/sstable/sstable.go:159:func (table *Table) GetWithStats(key string) (*string, bool, LookupStats, error) {
internal/sstable/sstable.go:205:func validateSorted(records []serializer.Record) error {
```

검증 신호:

- `Serialize`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestSSTableBloomRejectAndBoundedScan` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (filter *Filter) Serialize() []byte {
	buffer := make([]byte, 8+len(filter.bits))
	binary.BigEndian.PutUint32(buffer[0:4], filter.BitCount)
	binary.BigEndian.PutUint32(buffer[4:8], filter.HashFunctions)
	copy(buffer[8:], filter.bits)
	return buffer
}

func Deserialize(buffer []byte) (*Filter, error) {
	if len(buffer) < 8 {
		return nil, errors.New("bloomfilter: buffer too small")
	}
	filter := &Filter{
		BitCount:      binary.BigEndian.Uint32(buffer[0:4]),
```

왜 이 코드가 중요했는가:

`Serialize`가 없으면 `Filter`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Sparse Index Scan`에서 정리한 요점처럼, sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
