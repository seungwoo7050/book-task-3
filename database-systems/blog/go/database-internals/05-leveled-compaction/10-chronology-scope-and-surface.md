# 10 05 Leveled Compaction를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. README를 바로 요약하기보다, 테스트 이름과 파일 배치를 먼저 훑어 이 프로젝트의 테두리를 다시 그린다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

이 구간에서 먼저 붙잡으려 한 것은 `05 Leveled Compaction`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악하는 것이었다. 처음 읽을 때는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

그런데 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. 특히 `TestKWayMergeDropsTombstonesAtDeepestLevel`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `KWayMerge` 주변의 invariant를 고정하는 일이라는 게 보였다. 이때 가장 크게 작동한 단서는 `TestKWayMergeKeepsNewerValue`는 가장 기본 표면을 보여 줬고, `TestKWayMergeDropsTombstonesAtDeepestLevel`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/database-internals/projects/05-leveled-compaction/README.md`, `database-systems/go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/leveled-compaction/main.go
internal/compaction/compaction.go
internal/sstable/sstable.go
tests/compaction_test.go
```

```bash
$ rg -n "^func Test" tests
tests/compaction_test.go:14:func TestKWayMergeKeepsNewerValue(t *testing.T) {
tests/compaction_test.go:25:func TestKWayMergeDropsTombstonesAtDeepestLevel(t *testing.T) {
tests/compaction_test.go:36:func TestCompactL0ToL1(t *testing.T) {
tests/compaction_test.go:91:func TestManifestRoundTrip(t *testing.T) {
```

검증 신호:
- `TestKWayMergeKeepsNewerValue`는 가장 기본 표면을 보여 줬고, `TestKWayMergeDropsTombstonesAtDeepestLevel`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `KWayMerge` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestKWayMergeDropsTombstonesAtDeepestLevel(t *testing.T) {
	merged := compaction.KWayMerge([][]serializer.Record{
		{{Key: "gone", Value: nil}},
		{{Key: "gone", Value: serializer.StringPtr("alive")}},
	}, true)

	if len(merged) != 0 {
		t.Fatalf("expected tombstone to be dropped, got %+v", merged)
	}
}
```

왜 여기서 판단이 바뀌었는가:

`TestKWayMergeDropsTombstonesAtDeepestLevel`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Manifest Atomicity`에서 정리한 요점처럼, Compaction은 data file 집합과 metadata를 동시에 바꾸는 작업이다. 새 SSTable만 만들고 manifest를 못 바꾸면 reader가 새 파일을 모른다. 반대로 manifest만 먼저 바꾸고 파일 교체가 실패하면 존재하지 않는 파일을 가리키게 된다.

다음으로 넘긴 질문:
- `KWayMerge`와 `NeedsL0Compaction`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

여기서 가장 먼저 확인한 것은 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다. 처음에는 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

하지만 실제로는 가장 큰 구현 파일인 `database-systems/go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 결정적으로 방향을 잡아 준 신호는 `KWayMerge` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/sstable/sstable.go`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
internal/compaction/compaction.go:14:type Result struct {
internal/compaction/compaction.go:20:type Manager struct {
internal/compaction/compaction.go:28:type manifest struct {
internal/compaction/compaction.go:33:func New(dataDir string, l0MaxFiles int) *Manager {
internal/compaction/compaction.go:46:func (manager *Manager) AddToLevel(level int, fileName string) {
internal/compaction/compaction.go:50:func (manager *Manager) NeedsL0Compaction() bool {
internal/compaction/compaction.go:54:func (manager *Manager) CompactL0ToL1() (Result, error) {
internal/compaction/compaction.go:109:func (manager *Manager) SaveManifest() error {
internal/compaction/compaction.go:121:func (manager *Manager) LoadManifest() error {
internal/compaction/compaction.go:153:func KWayMerge(sources [][]serializer.Record, dropTombstones bool) []serializer.Record {
internal/compaction/compaction.go:174:func mergeTwo(newer []serializer.Record, older []serializer.Record) []serializer.Record {
internal/compaction/compaction.go:197:func readAll(path string) ([]serializer.Record, error) {
internal/compaction/compaction.go:202:func sequenceFileName(sequence int) string {
internal/compaction/compaction.go:206:func cloneLevels(levels map[int][]string) map[int][]string {
internal/compaction/compaction.go:214:func isNotExist(err error) bool {
cmd/leveled-compaction/main.go:12:func main() {
cmd/leveled-compaction/main.go:41:func seed(manager *compaction.Manager, sequence int, records []serializer.Record) {
cmd/leveled-compaction/main.go:53:func deref(value *string) string {
internal/sstable/sstable.go:14:type IndexEntry struct {
internal/sstable/sstable.go:19:type SSTable struct {
internal/sstable/sstable.go:25:func New(filePath string) *SSTable {
internal/sstable/sstable.go:29:func (table *SSTable) Write(records []serializer.Record) error {
internal/sstable/sstable.go:90:func (table *SSTable) LoadIndex() error {
internal/sstable/sstable.go:139:func (table *SSTable) Get(key string) (*string, bool, error) {
internal/sstable/sstable.go:179:func (table *SSTable) ReadAll() ([]serializer.Record, error) {
internal/sstable/sstable.go:211:func FileName(dataDir string, sequence int) string {
internal/sstable/sstable.go:215:func validateSorted(records []serializer.Record) error {
internal/sstable/sstable.go:224:func binarySearch(index []IndexEntry, key string) int {
```

검증 신호:
- `KWayMerge` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `NeedsL0Compaction`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
func KWayMerge(sources [][]serializer.Record, dropTombstones bool) []serializer.Record {
	if len(sources) == 0 {
		return []serializer.Record{}
	}
	merged := append([]serializer.Record(nil), sources[0]...)
	for i := 1; i < len(sources); i++ {
		merged = mergeTwo(merged, sources[i])
	}
	if !dropTombstones {
		return merged
	}
```

왜 여기서 판단이 바뀌었는가:

`KWayMerge`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Merge Ordering`에서 정리한 요점처럼, Compaction에서 같은 key가 여러 source에 동시에 존재하면 최신 source의 값만 살아남아야 한다. 이 프로젝트는 `sources[0]`을 newest로 보고 pairwise merge를 왼쪽에서 오른쪽으로 진행한다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `NeedsL0Compaction`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
