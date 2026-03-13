# 20 06 Quorum and Consistency의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `LatestVersion`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`의 `LatestVersion`
- 처음 가설:
  `LatestVersion` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "LatestVersion|ReadResult" internal cmd`로 핵심 함수 위치를 다시 잡고, `LatestVersion`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

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

왜 이 코드가 중요했는가:

`LatestVersion`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Versioned Register`에서 정리한 요점처럼, 이 프로젝트의 value는 `(version, data)` 두 값으로만 구성됩니다. vector clock처럼 여러 branch를 추적하지 않고, 가장 큰 version 하나만 최신으로 취급합니다.

다음:

- `ReadResult`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `ReadResult`가 `LatestVersion`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`의 `ReadResult`
- 처음 가설:
  `ReadResult`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `LatestVersion`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/quorum-demo/main.go:10:func main() {
cmd/quorum-demo/main.go:34:func mustCluster(policy quorum.Policy) *quorum.Cluster {
cmd/quorum-demo/main.go:40:func mustWrite(cluster *quorum.Cluster, key string, value string) {
cmd/quorum-demo/main.go:45:func must(err error) {
cmd/quorum-demo/main.go:51:func formatValue(result quorum.ReadResult) string {
cmd/quorum-demo/main.go:58:func formatResponders(result quorum.ReadResult) string {
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

왜 이 코드가 중요했는가:

`ReadResult`가 없으면 `LatestVersion`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Versioned Register`에서 정리한 요점처럼, 이 프로젝트의 value는 `(version, data)` 두 값으로만 구성됩니다. vector clock처럼 여러 branch를 추적하지 않고, 가장 큰 version 하나만 최신으로 취급합니다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
