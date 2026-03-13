# 10 08 Failure-Injected Log Replication의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `08 Failure-Injected Log Replication`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/README.md`, `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/tests/replication_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestPausedFollowerLagsButRecoversAfterResume`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `AppendPut` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/failure-replication/main.go
internal/replication/replication.go
tests/replication_test.go
```

```bash
$ rg -n "^func Test" tests
tests/replication_test.go:9:func TestDroppedAppendRetriesUntilFollowerConverges(t *testing.T) {
tests/replication_test.go:34:func TestDuplicateAppendIsIdempotent(t *testing.T) {
tests/replication_test.go:50:func TestPausedFollowerLagsButRecoversAfterResume(t *testing.T) {
```

검증 신호:

- `TestDroppedAppendRetriesUntilFollowerConverges`는 가장 기본 표면을 보여 줬고, `TestPausedFollowerLagsButRecoversAfterResume`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `AppendPut` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestPausedFollowerLagsButRecoversAfterResume(t *testing.T) {
	cluster := replication.NewCluster("leader-1", []string{"node-2", "node-3"})
	cluster.PauseNode("node-2")

	cluster.Put("alpha", "1")
	cluster.Tick()
	cluster.Put("beta", "2")
	cluster.Tick()

	node2 := follower(t, cluster, "node-2")
	if cluster.Leader.CommitIndex() != 1 {
		t.Fatalf("expected quorum commit to advance to 1, got %d", cluster.Leader.CommitIndex())
	}
	if node2.Watermark() != -1 {
```

왜 이 코드가 중요했는가:

`TestPausedFollowerLagsButRecoversAfterResume`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Failure Injection Harness`에서 정리한 요점처럼, 이 프로젝트의 하네스는 실제 네트워크를 흉내 내는 게 아니라, replication 코드가 어떤 실패에 반응해야 하는지 관찰 가능한 장면으로 압축하는 장치입니다.

다음:

- `AppendPut`와 `Follower`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `AppendPut` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Follower`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`AppendPut`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Quorum Commit and Retry`에서 정리한 요점처럼, leader는 모든 follower가 다 따라올 때까지 기다리지 않고, quorum ack가 모이면 commit index를 올립니다. 하지만 뒤처진 follower는 retry를 통해 결국 따라잡아야 합니다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `Follower`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
