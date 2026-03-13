# 20 04 Raft Lite에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 이제부터는 README 요약보다 코드가 더 많은 말을 한다. 핵심 함수 두 곳을 골라 상태 전이가 어떻게 고정되는지 확인한다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Tick에서 invariant가 잠기는 지점 보기

여기서 가장 먼저 확인한 것은 `Tick`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다. 처음에는 `Tick` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

하지만 실제로는 `rg -n "Tick|startElection" internal cmd`로 핵심 함수 위치를 다시 잡고, `Tick`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 결정적으로 방향을 잡아 준 신호는 `Tick` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go`의 `Tick`

CLI:

```bash
$ rg -n "Tick|startElection" internal cmd
cmd/raft-lite/main.go:14:		cluster.Tick()
cmd/raft-lite/main.go:21:		cluster.Tick()
internal/raft/raft.go:75:func (node *Node) Tick() {
internal/raft/raft.go:87:		node.startElection()
internal/raft/raft.go:91:func (node *Node) startElection() {
internal/raft/raft.go:302:func (cluster *Cluster) Tick() {
internal/raft/raft.go:307:		cluster.nodes[id].Tick()
```

검증 신호:
- `Tick` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `term과 election cycle이 leader 교체를 어떻게 제어하는지 익힙니다.`

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

`Tick`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Election Cycle`에서 정리한 요점처럼, follower는 heartbeat를 받지 못하면 candidate가 되고 term을 올린 뒤 RequestVote를 보낸다. 과반을 얻으면 leader가 되고, 그렇지 못하면 다시 follower/candidate 사이를 오간다.

다음으로 넘긴 질문:
- `startElection`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — startElection로 같은 규칙 다시 확인하기

이번 세션의 목표는 `startElection`가 `Tick`와 어떤 짝을 이루는지 확인하는 것이었다. 초기 가설은 `startElection`는 단순 보조 함수일 거라고 생각했다.

막상 다시 펼쳐 보니 두 번째 앵커를 읽고 나니, 실제로는 `Tick`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `startElection`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go`의 `startElection`

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
- `startElection`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestLogReplicationAndCommit` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func (node *Node) startElection() {
	node.State = Candidate
	node.Term++
	node.VotedFor = node.ID
	node.votes = map[string]struct{}{node.ID: {}}
	node.electionAge = 0

	lastIndex, lastTerm := node.lastLogInfo()
	for _, peer := range node.Peers {
		raw := node.sendRPC(peer, "requestVote", voteRequest{
			Term:         node.Term,
			CandidateID:  node.ID,
			LastLogIndex: lastIndex,
			LastLogTerm:  lastTerm,
```

왜 여기서 판단이 바뀌었는가:

`startElection`가 없으면 `Tick`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Election Cycle`에서 정리한 요점처럼, follower는 heartbeat를 받지 못하면 candidate가 되고 term을 올린 뒤 RequestVote를 보낸다. 과반을 얻으면 leader가 되고, 그렇지 못하면 다시 follower/candidate 사이를 오간다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
