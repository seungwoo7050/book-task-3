# 20 07 Heartbeat and Leader Election의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `heartbeatRequest`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`의 `heartbeatRequest`
- 처음 가설:
  `heartbeatRequest` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "heartbeatRequest|startElection" internal cmd`로 핵심 함수 위치를 다시 잡고, `heartbeatRequest`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "heartbeatRequest|startElection" internal cmd
internal/election/election.go:19:type heartbeatRequest struct {
internal/election/election.go:72:		node.startElection()
internal/election/election.go:94:func (node *Node) HandleHeartbeat(req heartbeatRequest) heartbeatResponse {
internal/election/election.go:106:func (node *Node) startElection() {
internal/election/election.go:156:		raw := node.sendRPC(peer, "heartbeat", heartbeatRequest{
internal/election/election.go:254:		return node.HandleHeartbeat(payload.(heartbeatRequest))
```

검증 신호:

- `heartbeatRequest` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `heartbeat silence가 suspicion으로 바뀌고, 그 다음 election으로 이어지는 흐름을 익힙니다.`

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

왜 이 코드가 중요했는가:

`heartbeatRequest`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Majority Election`에서 정리한 요점처럼, leader election의 핵심은 단순히 “가장 먼저 손든 node”가 아니라, 과반이 인정한 node만 authority를 가진다는 점입니다.

다음:

- `startElection`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `startElection`가 `heartbeatRequest`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`의 `startElection`
- 처음 가설:
  `startElection`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `heartbeatRequest`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

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

- `startElection`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestLeaderFailureTriggersSingleReelection` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (node *Node) startElection() {
	node.State = Candidate
	node.Term++
	node.VotedFor = node.ID
	node.Suspected = false
	node.silenceAge = 0
	node.votes = map[string]struct{}{node.ID: {}}

	for _, peer := range node.Peers {
		raw := node.sendRPC(peer, "vote", voteRequest{
			Term:        node.Term,
			CandidateID: node.ID,
		})
		resp, ok := raw.(voteResponse)
```

왜 이 코드가 중요했는가:

`startElection`가 없으면 `heartbeatRequest`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Majority Election`에서 정리한 요점처럼, leader election의 핵심은 단순히 “가장 먼저 손든 node”가 아니라, 과반이 인정한 node만 authority를 가진다는 점입니다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
