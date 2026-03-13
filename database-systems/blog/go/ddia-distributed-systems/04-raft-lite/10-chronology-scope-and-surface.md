# 10 04 Raft Lite를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. README를 바로 요약하기보다, 테스트 이름과 파일 배치를 먼저 훑어 이 프로젝트의 테두리를 다시 그린다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

이 구간에서 먼저 붙잡으려 한 것은 `04 Raft Lite`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악하는 것이었다. 처음 읽을 때는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

그런데 `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. 특히 `TestLogReplicationAndCommit`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Tick` 주변의 invariant를 고정하는 일이라는 게 보였다. 이때 가장 크게 작동한 단서는 `TestLeaderElection`는 가장 기본 표면을 보여 줬고, `TestLogReplicationAndCommit`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/README.md`, `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/tests/raft_test.go`

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/raft-lite/main.go
internal/raft/raft.go
tests/raft_test.go
```

```bash
$ rg -n "^func Test" tests
tests/raft_test.go:19:func TestLeaderElection(t *testing.T) {
tests/raft_test.go:37:func TestLeaderFailover(t *testing.T) {
tests/raft_test.go:50:func TestLogReplicationAndCommit(t *testing.T) {
tests/raft_test.go:77:func TestHigherTermForcesStepDown(t *testing.T) {
```

검증 신호:
- `TestLeaderElection`는 가장 기본 표면을 보여 줬고, `TestLogReplicationAndCommit`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Tick` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestLogReplicationAndCommit(t *testing.T) {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := electLeader(cluster, 20)
	if leader == nil {
		t.Fatalf("expected leader")
	}

	cluster.ClientRequest("SET x 1")
	cluster.ClientRequest("SET y 2")
	for i := 0; i < 20; i++ {
		cluster.Tick()
	}
```

왜 여기서 판단이 바뀌었는가:

`TestLogReplicationAndCommit`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Commit Rule`에서 정리한 요점처럼, leader는 단순히 local append 했다고 commit하지 않는다. 현재 term의 entry가 과반수 노드에 replicate 되었을 때만 `commitIndex`를 올린다.

다음으로 넘긴 질문:
- `Tick`와 `startElection`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

여기서 가장 먼저 확인한 것은 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다. 처음에는 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

하지만 실제로는 가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 결정적으로 방향을 잡아 준 신호는 `Tick` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/raft-lite/main.go:9:func main() {
cmd/raft-lite/main.go:19:func waitLeader(cluster *raft.Cluster) *raft.Node {
internal/raft/raft.go:9:type LogEntry struct {
internal/raft/raft.go:15:type voteRequest struct {
internal/raft/raft.go:22:type voteResponse struct {
internal/raft/raft.go:27:type appendRequest struct {
internal/raft/raft.go:36:type appendResponse struct {
internal/raft/raft.go:41:type Node struct {
internal/raft/raft.go:60:func NewNode(id string, peers []string, electionTTL int, sendRPC func(string, string, any) any) *Node {
internal/raft/raft.go:75:func (node *Node) Tick() {
internal/raft/raft.go:91:func (node *Node) startElection() {
internal/raft/raft.go:124:func (node *Node) becomeLeader() {
internal/raft/raft.go:135:func (node *Node) stepDown(term int) {
internal/raft/raft.go:143:func (node *Node) HandleRequestVote(req voteRequest) voteResponse {
internal/raft/raft.go:162:func (node *Node) HandleAppendEntries(req appendRequest) appendResponse {
internal/raft/raft.go:199:func (node *Node) ClientRequest(command string) *LogEntry {
internal/raft/raft.go:208:func (node *Node) sendHeartbeats() {
internal/raft/raft.go:215:func (node *Node) replicateTo(peer string) {
internal/raft/raft.go:249:func (node *Node) advanceCommitIndex() {
internal/raft/raft.go:267:func (node *Node) lastLogInfo() (int, int) {
internal/raft/raft.go:275:type Cluster struct {
internal/raft/raft.go:281:func NewCluster(nodeIDs []string) *Cluster {
internal/raft/raft.go:302:func (cluster *Cluster) Tick() {
internal/raft/raft.go:311:func (cluster *Cluster) Leader() *Node {
internal/raft/raft.go:323:func (cluster *Cluster) Nodes() []*Node {
internal/raft/raft.go:331:func (cluster *Cluster) DownNode(id string) {
internal/raft/raft.go:335:func (cluster *Cluster) UpNode(id string) {
internal/raft/raft.go:340:func (cluster *Cluster) ClientRequest(command string) *LogEntry {
internal/raft/raft.go:348:func (cluster *Cluster) deliverRPC(target string, rpc string, payload any) any {
internal/raft/raft.go:363:func majority(size int) int {
internal/raft/raft.go:367:func min(a int, b int) int {
```

검증 신호:
- `Tick` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `startElection`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
func (node *Node) Tick() {
	if node.State == Leader {
		node.heartAge++
		if node.heartAge >= node.heartbeat {
			node.heartAge = 0
			node.sendHeartbeats()
		}
		return
	}
```

왜 여기서 판단이 바뀌었는가:

`Tick`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Election Cycle`에서 정리한 요점처럼, follower는 heartbeat를 받지 못하면 candidate가 되고 term을 올린 뒤 RequestVote를 보낸다. 과반을 얻으면 leader가 되고, 그렇지 못하면 다시 follower/candidate 사이를 오간다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `startElection`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
