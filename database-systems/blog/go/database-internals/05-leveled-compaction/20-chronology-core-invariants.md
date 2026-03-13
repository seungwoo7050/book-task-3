# 20 05 Leveled Compaction에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 이제부터는 README 요약보다 코드가 더 많은 말을 한다. 핵심 함수 두 곳을 골라 상태 전이가 어떻게 고정되는지 확인한다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — KWayMerge에서 invariant가 잠기는 지점 보기

여기서 가장 먼저 확인한 것은 `KWayMerge`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다. 처음에는 `KWayMerge` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

하지만 실제로는 `rg -n "KWayMerge|NeedsL0Compaction" internal cmd`로 핵심 함수 위치를 다시 잡고, `KWayMerge`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 결정적으로 방향을 잡아 준 신호는 `KWayMerge` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`의 `KWayMerge`

CLI:

```bash
$ rg -n "KWayMerge|NeedsL0Compaction" internal cmd
internal/compaction/compaction.go:50:func (manager *Manager) NeedsL0Compaction() bool {
internal/compaction/compaction.go:80:	merged := KWayMerge(sources, dropTombstones)
internal/compaction/compaction.go:153:func KWayMerge(sources [][]serializer.Record, dropTombstones bool) []serializer.Record {
```

검증 신호:
- `KWayMerge` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `newest-first 우선순위를 유지한 k-way merge를 구현합니다.`

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

`KWayMerge`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Merge Ordering`에서 정리한 요점처럼, Compaction에서 같은 key가 여러 source에 동시에 존재하면 최신 source의 값만 살아남아야 한다. 이 프로젝트는 `sources[0]`을 newest로 보고 pairwise merge를 왼쪽에서 오른쪽으로 진행한다.

다음으로 넘긴 질문:
- `NeedsL0Compaction`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — NeedsL0Compaction로 같은 규칙 다시 확인하기

이번 세션의 목표는 `NeedsL0Compaction`가 `KWayMerge`와 어떤 짝을 이루는지 확인하는 것이었다. 초기 가설은 `NeedsL0Compaction`는 단순 보조 함수일 거라고 생각했다.

막상 다시 펼쳐 보니 두 번째 앵커를 읽고 나니, 실제로는 `KWayMerge`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `NeedsL0Compaction`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go`의 `NeedsL0Compaction`

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
- `NeedsL0Compaction`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestKWayMergeDropsTombstonesAtDeepestLevel` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (manager *Manager) NeedsL0Compaction() bool {
	return len(manager.Levels[0]) >= manager.L0MaxFiles
}

func (manager *Manager) CompactL0ToL1() (Result, error) {
	l0Files := append([]string(nil), manager.Levels[0]...)
	if len(l0Files) == 0 {
		return Result{}, nil
	}
```

왜 여기서 판단이 바뀌었는가:

`NeedsL0Compaction`가 없으면 `KWayMerge`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Merge Ordering`에서 정리한 요점처럼, Compaction에서 같은 key가 여러 source에 동시에 존재하면 최신 source의 값만 살아남아야 한다. 이 프로젝트는 `sources[0]`을 newest로 보고 pairwise merge를 왼쪽에서 오른쪽으로 진행한다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
