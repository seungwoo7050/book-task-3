# 10 07 Heartbeat and Leader Election를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 설명문을 믿고 곧장 구현으로 들어가기보다, 테스트와 파일 구조를 다시 읽으면서 어디서부터 이야기를 시작해야 하는지 정리한다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

여기서 가장 먼저 확인한 것은 `07 Heartbeat and Leader Election`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다. 처음에는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

하지만 실제로는 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestLeaderFailureTriggersSingleReelection`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `heartbeatRequest` 주변의 invariant를 고정하는 일이라는 게 보였다. 결정적으로 방향을 잡아 준 신호는 `TestHealthyLeaderKeepsSendingHeartbeats`는 가장 기본 표면을 보여 줬고, `TestLeaderFailureTriggersSingleReelection`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/README.md`, `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/tests/election_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/leader-election/main.go
internal/election/election.go
tests/election_test.go
```

```bash
$ rg -n "^func Test" tests
tests/election_test.go:9:func TestHealthyLeaderKeepsSendingHeartbeats(t *testing.T) {
tests/election_test.go:30:func TestLeaderFailureTriggersSingleReelection(t *testing.T) {
tests/election_test.go:44:func TestIsolatedNodeCannotPromoteItself(t *testing.T) {
tests/election_test.go:61:func TestHigherTermHeartbeatForcesOldLeaderToStepDown(t *testing.T) {
```

검증 신호:
- `TestHealthyLeaderKeepsSendingHeartbeats`는 가장 기본 표면을 보여 줬고, `TestLeaderFailureTriggersSingleReelection`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `heartbeatRequest` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestLeaderFailureTriggersSingleReelection(t *testing.T) {
	cluster := election.NewCluster([]string{"node-1", "node-2", "node-3"})
	leader := tickUntilLeader(t, cluster, 12)
	cluster.DownNode(leader.ID)

	next := tickUntilLeader(t, cluster, 12)
	if next.ID == leader.ID {
		t.Fatalf("expected a new leader after failover")
	}
	if next.Term <= leader.Term {
		t.Fatalf("expected term to increase after failover, old=%d new=%d", leader.Term, next.Term)
	}
}
```

왜 여기서 판단이 바뀌었는가:

`TestLeaderFailureTriggersSingleReelection`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Heartbeat Failure Detector`에서 정리한 요점처럼, 이 프로젝트의 failure detector는 아주 단순합니다. leader heartbeat를 일정 tick 동안 못 보면 follower가 “leader가 죽었을 수 있다”고 suspect합니다.

다음으로 넘긴 질문:
- `heartbeatRequest`와 `startElection`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이번 세션의 목표는 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 초기 가설은 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

막상 다시 펼쳐 보니 가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `heartbeatRequest` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/leader-election/main.go:9:func main() {
internal/election/election.go:9:type voteRequest struct {
internal/election/election.go:14:type voteResponse struct {
internal/election/election.go:19:type heartbeatRequest struct {
internal/election/election.go:24:type heartbeatResponse struct {
internal/election/election.go:28:type Node struct {
internal/election/election.go:44:func NewNode(id string, peers []string, suspicionTTL int, electionTTL int, sendRPC func(string, string, any) any) *Node {
internal/election/election.go:57:func (node *Node) Tick() {
internal/election/election.go:76:func (node *Node) HandleVoteRequest(req voteRequest) voteResponse {
internal/election/election.go:94:func (node *Node) HandleHeartbeat(req heartbeatRequest) heartbeatResponse {
internal/election/election.go:106:func (node *Node) startElection() {
internal/election/election.go:137:func (node *Node) becomeLeader() {
internal/election/election.go:144:func (node *Node) stepDown(term int) {
internal/election/election.go:154:func (node *Node) sendHeartbeats() {
internal/election/election.go:171:type Cluster struct {
internal/election/election.go:177:func NewCluster(nodeIDs []string) *Cluster {
internal/election/election.go:198:func (cluster *Cluster) Tick() {
internal/election/election.go:207:func (cluster *Cluster) Leader() *Node {
internal/election/election.go:220:func (cluster *Cluster) Node(id string) *Node {
internal/election/election.go:224:func (cluster *Cluster) Nodes() []*Node {
internal/election/election.go:232:func (cluster *Cluster) DownNode(id string) {
internal/election/election.go:236:func (cluster *Cluster) UpNode(id string) {
internal/election/election.go:245:func (cluster *Cluster) deliverRPC(target string, rpc string, payload any) any {
internal/election/election.go:260:func majority(size int) int {
```

검증 신호:
- `heartbeatRequest` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `startElection`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
type heartbeatRequest struct {
	Term     int
	LeaderID string
}

type heartbeatResponse struct {
	Term int
}

type Node struct {
	ID             string
	Peers          []string
	sendRPC        func(target string, rpc string, payload any) any
	State          string
```

왜 여기서 판단이 바뀌었는가:

`heartbeatRequest`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Majority Election`에서 정리한 요점처럼, leader election의 핵심은 단순히 “가장 먼저 손든 node”가 아니라, 과반이 인정한 node만 authority를 가진다는 점입니다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `startElection`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
