# 10 06 Quorum and Consistency를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 설명문을 믿고 곧장 구현으로 들어가기보다, 테스트와 파일 구조를 다시 읽으면서 어디서부터 이야기를 시작해야 하는지 정리한다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

여기서 가장 먼저 확인한 것은 `06 Quorum and Consistency`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다. 처음에는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

하지만 실제로는 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestReplicaFailuresReduceAvailability`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `LatestVersion` 주변의 invariant를 고정하는 일이라는 게 보였다. 결정적으로 방향을 잡아 준 신호는 `TestReadReturnsLatestWhenQuorumsOverlap`는 가장 기본 표면을 보여 줬고, `TestReplicaFailuresReduceAvailability`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/README.md`, `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/tests/quorum_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/quorum-demo/main.go
internal/quorum/quorum.go
tests/quorum_test.go
```

```bash
$ rg -n "^func Test" tests
tests/quorum_test.go:9:func TestReadReturnsLatestWhenQuorumsOverlap(t *testing.T) {
tests/quorum_test.go:42:func TestStaleReadAppearsWhenQuorumsDoNotOverlap(t *testing.T) {
tests/quorum_test.go:75:func TestWriteFailureDoesNotAdvanceVersion(t *testing.T) {
tests/quorum_test.go:95:func TestReplicaFailuresReduceAvailability(t *testing.T) {
```

검증 신호:
- `TestReadReturnsLatestWhenQuorumsOverlap`는 가장 기본 표면을 보여 줬고, `TestReplicaFailuresReduceAvailability`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `LatestVersion` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestReplicaFailuresReduceAvailability(t *testing.T) {
	cluster := newCluster(t, quorum.Policy{N: 3, W: 2, R: 2})
	if _, err := cluster.Write("order", "v1"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-2"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-3"); err != nil {
		t.Fatal(err)
	}
```

왜 여기서 판단이 바뀌었는가:

`TestReplicaFailuresReduceAvailability`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Quorum Read/Write`에서 정리한 요점처럼, quorum의 핵심은 “모든 replica가 최신이어야 한다”가 아니라, read quorum과 write quorum이 반드시 한 번은 겹치게 만드는 것입니다.

다음으로 넘긴 질문:
- `LatestVersion`와 `ReadResult`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이번 세션의 목표는 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 초기 가설은 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

막상 다시 펼쳐 보니 가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `LatestVersion` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
internal/quorum/quorum.go:5:type Value struct {
internal/quorum/quorum.go:10:type Policy struct {
internal/quorum/quorum.go:16:func (policy Policy) Validate(replicaCount int) error {
internal/quorum/quorum.go:29:type Replica struct {
internal/quorum/quorum.go:35:func (replica *Replica) IsUp() bool {
internal/quorum/quorum.go:39:type Observation struct {
internal/quorum/quorum.go:44:type ReadResult struct {
internal/quorum/quorum.go:50:type WriteResult struct {
internal/quorum/quorum.go:55:type Cluster struct {
internal/quorum/quorum.go:62:func NewCluster(ids []string, policy Policy) (*Cluster, error) {
internal/quorum/quorum.go:82:func (cluster *Cluster) Policy() Policy {
internal/quorum/quorum.go:86:func (cluster *Cluster) DownReplica(id string) error {
internal/quorum/quorum.go:95:func (cluster *Cluster) UpReplica(id string) error {
internal/quorum/quorum.go:104:func (cluster *Cluster) Write(key string, value string) (WriteResult, error) {
internal/quorum/quorum.go:121:func (cluster *Cluster) Read(key string) (ReadResult, error) {
internal/quorum/quorum.go:149:func (cluster *Cluster) ReplicaValue(id string, key string) (Value, bool, error) {
internal/quorum/quorum.go:158:func (cluster *Cluster) LatestVersion(key string) int {
internal/quorum/quorum.go:162:func (cluster *Cluster) availableReplicas() []*Replica {
internal/quorum/quorum.go:173:func (cluster *Cluster) replica(id string) (*Replica, error) {
cmd/quorum-demo/main.go:10:func main() {
cmd/quorum-demo/main.go:34:func mustCluster(policy quorum.Policy) *quorum.Cluster {
cmd/quorum-demo/main.go:40:func mustWrite(cluster *quorum.Cluster, key string, value string) {
cmd/quorum-demo/main.go:45:func must(err error) {
cmd/quorum-demo/main.go:51:func formatValue(result quorum.ReadResult) string {
cmd/quorum-demo/main.go:58:func formatResponders(result quorum.ReadResult) string {
```

검증 신호:
- `LatestVersion` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `ReadResult`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
func (cluster *Cluster) LatestVersion(key string) int {
	return cluster.versions[key]
}

func (cluster *Cluster) availableReplicas() []*Replica {
	available := make([]*Replica, 0, len(cluster.order))
	for _, id := range cluster.order {
		replica := cluster.replicas[id]
		if replica != nil && replica.up {
			available = append(available, replica)
		}
	}
	return available
}
```

왜 여기서 판단이 바뀌었는가:

`LatestVersion`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Versioned Register`에서 정리한 요점처럼, 이 프로젝트의 value는 `(version, data)` 두 값으로만 구성됩니다. vector clock처럼 여러 branch를 추적하지 않고, 가장 큰 version 하나만 최신으로 취급합니다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `ReadResult`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
