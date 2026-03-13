# 20 06 Quorum and Consistency에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 기능 목록을 다시 적기보다, 규칙이 실제 코드에서 언제 강제되는지 보여 주는 데 초점을 둔다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — LatestVersion에서 invariant가 잠기는 지점 보기

이번 세션의 목표는 `LatestVersion`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 초기 가설은 `LatestVersion` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

막상 다시 펼쳐 보니 `rg -n "LatestVersion|ReadResult" internal cmd`로 핵심 함수 위치를 다시 잡고, `LatestVersion`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `LatestVersion` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`의 `LatestVersion`

CLI:

```bash
$ rg -n "LatestVersion|ReadResult" internal cmd
cmd/quorum-demo/main.go:51:func formatValue(result quorum.ReadResult) string {
cmd/quorum-demo/main.go:58:func formatResponders(result quorum.ReadResult) string {
internal/quorum/quorum.go:44:type ReadResult struct {
internal/quorum/quorum.go:121:func (cluster *Cluster) Read(key string) (ReadResult, error) {
internal/quorum/quorum.go:124:		return ReadResult{}, fmt.Errorf("read quorum unavailable: need %d replicas, have %d", cluster.policy.R, len(available))
internal/quorum/quorum.go:127:	result := ReadResult{
internal/quorum/quorum.go:158:func (cluster *Cluster) LatestVersion(key string) int {
```

검증 신호:
- `LatestVersion` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `replica 일부가 뒤처져도 quorum read가 최신 버전을 고르는 조건을 익힙니다.`

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

`LatestVersion`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Versioned Register`에서 정리한 요점처럼, 이 프로젝트의 value는 `(version, data)` 두 값으로만 구성됩니다. vector clock처럼 여러 branch를 추적하지 않고, 가장 큰 version 하나만 최신으로 취급합니다.

다음으로 넘긴 질문:
- `ReadResult`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — ReadResult로 같은 규칙 다시 확인하기

이 구간에서 먼저 붙잡으려 한 것은 `ReadResult`가 `LatestVersion`와 어떤 짝을 이루는지 확인하는 것이었다. 처음 읽을 때는 `ReadResult`는 단순 보조 함수일 거라고 생각했다.

그런데 두 번째 앵커를 읽고 나니, 실제로는 `LatestVersion`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `ReadResult`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`의 `ReadResult`

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
- `ReadResult`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestReplicaFailuresReduceAvailability` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
type ReadResult struct {
	Value      Value
	Found      bool
	Responders []Observation
}

type WriteResult struct {
	Version    int
	Replicated []string
}
```

왜 여기서 판단이 바뀌었는가:

`ReadResult`가 없으면 `LatestVersion`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Versioned Register`에서 정리한 요점처럼, 이 프로젝트의 value는 `(version, data)` 두 값으로만 구성됩니다. vector clock처럼 여러 branch를 추적하지 않고, 가장 큰 version 하나만 최신으로 취급합니다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
