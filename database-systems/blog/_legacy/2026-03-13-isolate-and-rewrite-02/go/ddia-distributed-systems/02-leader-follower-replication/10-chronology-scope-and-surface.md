# 10 02 Leader-Follower Replication의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `02 Leader-Follower Replication`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/README.md`, `database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/tests/replication_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestReplicateOnceIncrementalAndDeletes`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Append` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/replication/main.go
internal/replication/replication.go
tests/replication_test.go
```

```bash
$ rg -n "^func Test" tests
tests/replication_test.go:9:func TestReplicationLogAssignsSequentialOffsets(t *testing.T) {
tests/replication_test.go:19:func TestFollowerApplyIsIdempotent(t *testing.T) {
tests/replication_test.go:36:func TestReplicateOnceIncrementalAndDeletes(t *testing.T) {
```

검증 신호:

- `TestReplicationLogAssignsSequentialOffsets`는 가장 기본 표면을 보여 줬고, `TestReplicateOnceIncrementalAndDeletes`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Append` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestReplicateOnceIncrementalAndDeletes(t *testing.T) {
	leader := replication.NewLeader()
	follower := replication.NewFollower()

	leader.Put("a", "1")
	if applied := replication.ReplicateOnce(leader, follower); applied != 1 {
		t.Fatalf("expected 1 applied, got %d", applied)
	}
	if follower.Watermark() != 0 {
		t.Fatalf("expected watermark 0, got %d", follower.Watermark())
	}
```

왜 이 코드가 중요했는가:

`TestReplicateOnceIncrementalAndDeletes`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Idempotent Follower`에서 정리한 요점처럼, 실제 복제에서는 같은 entry batch가 재전송될 수 있다. follower가 `offset <= current_watermark`인 entry를 다시 적용하지 않도록 만들면 replay가 안전해진다.

다음:

- `Append`와 `ReplicateOnce`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/replication/main.go:9:func main() {
internal/replication/replication.go:3:type LogEntry struct {
internal/replication/replication.go:10:type ReplicationLog struct {
internal/replication/replication.go:14:func (log *ReplicationLog) Append(operation string, key string, value *string) int {
internal/replication/replication.go:25:func (log *ReplicationLog) From(offset int) []LogEntry {
internal/replication/replication.go:35:func (log *ReplicationLog) LatestOffset() int {
internal/replication/replication.go:39:type Leader struct {
internal/replication/replication.go:44:func NewLeader() *Leader {
internal/replication/replication.go:51:func (leader *Leader) Put(key string, value string) int {
internal/replication/replication.go:56:func (leader *Leader) Delete(key string) int {
internal/replication/replication.go:61:func (leader *Leader) Get(key string) (string, bool) {
internal/replication/replication.go:66:func (leader *Leader) LogFrom(offset int) []LogEntry {
internal/replication/replication.go:70:func (leader *Leader) LatestOffset() int {
internal/replication/replication.go:74:type Follower struct {
internal/replication/replication.go:79:func NewFollower() *Follower {
internal/replication/replication.go:86:func (follower *Follower) Apply(entries []LogEntry) int {
internal/replication/replication.go:106:func (follower *Follower) Get(key string) (string, bool) {
internal/replication/replication.go:111:func (follower *Follower) Watermark() int {
internal/replication/replication.go:115:func ReplicateOnce(leader *Leader, follower *Follower) int {
internal/replication/replication.go:120:func stringPtr(value string) *string {
```

검증 신호:

- `Append` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `ReplicateOnce`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
func (log *ReplicationLog) Append(operation string, key string, value *string) int {
	offset := len(log.entries)
	log.entries = append(log.entries, LogEntry{
		Offset:    offset,
		Operation: operation,
		Key:       key,
		Value:     value,
	})
	return offset
}
```

왜 이 코드가 중요했는가:

`Append`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Log Shipping`에서 정리한 요점처럼, leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `ReplicateOnce`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
