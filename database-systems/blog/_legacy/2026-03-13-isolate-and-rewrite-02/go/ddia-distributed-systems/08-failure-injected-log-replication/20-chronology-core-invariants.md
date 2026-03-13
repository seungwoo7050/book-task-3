# 20 08 Failure-Injected Log Replication의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `AppendPut`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go`의 `AppendPut`
- 처음 가설:
  `AppendPut` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "AppendPut|Follower" internal cmd`로 핵심 함수 위치를 다시 잡고, `AppendPut`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "AppendPut|Follower" internal cmd
cmd/failure-replication/main.go:15:	node2 := mustFollower(cluster, "node-2")
cmd/failure-replication/main.go:16:	node3 := mustFollower(cluster, "node-3")
cmd/failure-replication/main.go:37:func mustFollower(cluster *replication.Cluster, id string) *replication.Follower {
cmd/failure-replication/main.go:38:	follower, err := cluster.Follower(id)
internal/replication/replication.go:49:func (leader *Leader) AppendPut(key string, value string) LogEntry {
internal/replication/replication.go:116:type Follower struct {
internal/replication/replication.go:123:func NewFollower(id string) *Follower {
internal/replication/replication.go:124:	return &Follower{
internal/replication/replication.go:130:func (follower *Follower) HandleAppend(entry LogEntry) int {
internal/replication/replication.go:148:func (follower *Follower) Watermark() int {
internal/replication/replication.go:152:func (follower *Follower) Read(key string) (string, bool) {
internal/replication/replication.go:157:func (follower *Follower) LogLength() int {
internal/replication/replication.go:161:func (follower *Follower) AppliedCount() int {
internal/replication/replication.go:165:func (follower *Follower) apply(entry LogEntry) {
internal/replication/replication.go:175:func (follower *Follower) rebuildStore() {
internal/replication/replication.go:242:	followers map[string]*Follower
internal/replication/replication.go:250:		followers: map[string]*Follower{},
internal/replication/replication.go:255:		cluster.followers[followerID] = NewFollower(followerID)
internal/replication/replication.go:261:	return cluster.Leader.AppendPut(key, value)
internal/replication/replication.go:268:func (cluster *Cluster) Follower(id string) (*Follower, error) {
```

검증 신호:

- `AppendPut` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `dropped append가 retry로 수렴하는 흐름을 익힙니다.`

핵심 코드:

```go
func (leader *Leader) AppendPut(key string, value string) LogEntry {
	entry := LogEntry{
		Index:     len(leader.log),
		Operation: "put",
		Key:       key,
		Value:     stringPtr(value),
	}
	leader.log = append(leader.log, entry)
	leader.store[key] = value
	return entry
}
```

왜 이 코드가 중요했는가:

`AppendPut`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Quorum Commit and Retry`에서 정리한 요점처럼, leader는 모든 follower가 다 따라올 때까지 기다리지 않고, quorum ack가 모이면 commit index를 올립니다. 하지만 뒤처진 follower는 retry를 통해 결국 따라잡아야 합니다.

다음:

- `Follower`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `Follower`가 `AppendPut`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go`의 `Follower`
- 처음 가설:
  `Follower`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `AppendPut`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/failure-replication/main.go:9:func main() {
cmd/failure-replication/main.go:37:func mustFollower(cluster *replication.Cluster, id string) *replication.Follower {
internal/replication/replication.go:10:type LogEntry struct {
internal/replication/replication.go:17:type Message struct {
internal/replication/replication.go:25:type Leader struct {
internal/replication/replication.go:34:func NewLeader(id string, followerIDs []string) *Leader {
internal/replication/replication.go:49:func (leader *Leader) AppendPut(key string, value string) LogEntry {
internal/replication/replication.go:61:func (leader *Leader) CommitIndex() int {
internal/replication/replication.go:65:func (leader *Leader) Read(key string) (string, bool) {
internal/replication/replication.go:70:func (leader *Leader) LogLength() int {
internal/replication/replication.go:74:func (leader *Leader) outgoingAppends() []Message {
internal/replication/replication.go:93:func (leader *Leader) handleAck(followerID string, index int) {
internal/replication/replication.go:101:func (leader *Leader) advanceCommit() {
internal/replication/replication.go:116:type Follower struct {
internal/replication/replication.go:123:func NewFollower(id string) *Follower {
internal/replication/replication.go:130:func (follower *Follower) HandleAppend(entry LogEntry) int {
internal/replication/replication.go:148:func (follower *Follower) Watermark() int {
internal/replication/replication.go:152:func (follower *Follower) Read(key string) (string, bool) {
internal/replication/replication.go:157:func (follower *Follower) LogLength() int {
internal/replication/replication.go:161:func (follower *Follower) AppliedCount() int {
internal/replication/replication.go:165:func (follower *Follower) apply(entry LogEntry) {
internal/replication/replication.go:175:func (follower *Follower) rebuildStore() {
internal/replication/replication.go:183:type NetworkHarness struct {
internal/replication/replication.go:189:func NewNetworkHarness() *NetworkHarness {
internal/replication/replication.go:197:func (network *NetworkHarness) PauseNode(id string) {
internal/replication/replication.go:201:func (network *NetworkHarness) ResumeNode(id string) {
internal/replication/replication.go:205:func (network *NetworkHarness) DropNext(kind string, to string, index int, count int) {
internal/replication/replication.go:209:func (network *NetworkHarness) DuplicateNext(kind string, to string, index int, count int) {
internal/replication/replication.go:213:func (network *NetworkHarness) Route(messages []Message, handler func(Message) []Message) {
internal/replication/replication.go:240:type Cluster struct {
internal/replication/replication.go:247:func NewCluster(leaderID string, followerIDs []string) *Cluster {
internal/replication/replication.go:260:func (cluster *Cluster) Put(key string, value string) LogEntry {
internal/replication/replication.go:264:func (cluster *Cluster) Tick() {
internal/replication/replication.go:268:func (cluster *Cluster) Follower(id string) (*Follower, error) {
internal/replication/replication.go:276:func (cluster *Cluster) PauseNode(id string) {
internal/replication/replication.go:280:func (cluster *Cluster) ResumeNode(id string) {
internal/replication/replication.go:284:func (cluster *Cluster) DropNext(kind string, to string, index int, count int) {
internal/replication/replication.go:288:func (cluster *Cluster) DuplicateNext(kind string, to string, index int, count int) {
internal/replication/replication.go:292:func (cluster *Cluster) handleMessage(message Message) []Message {
internal/replication/replication.go:313:func majority(size int) int {
internal/replication/replication.go:317:func ruleKey(kind string, to string, index int) string {
internal/replication/replication.go:321:func equalEntry(left LogEntry, right LogEntry) bool {
internal/replication/replication.go:335:func stringPtr(value string) *string {
```

검증 신호:

- `Follower`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestPausedFollowerLagsButRecoversAfterResume` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
type Follower struct {
	ID           string
	log          []LogEntry
	store        map[string]string
	appliedCount int
}

func NewFollower(id string) *Follower {
	return &Follower{
		ID:    id,
		store: map[string]string{},
	}
}
```

왜 이 코드가 중요했는가:

`Follower`가 없으면 `AppendPut`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Quorum Commit and Retry`에서 정리한 요점처럼, leader는 모든 follower가 다 따라올 때까지 기다리지 않고, quorum ack가 모이면 commit index를 올립니다. 하지만 뒤처진 follower는 retry를 통해 결국 따라잡아야 합니다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
