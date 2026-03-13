# 20 02 Leader-Follower Replication에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 이제부터는 README 요약보다 코드가 더 많은 말을 한다. 핵심 함수 두 곳을 골라 상태 전이가 어떻게 고정되는지 확인한다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Append에서 invariant가 잠기는 지점 보기

여기서 가장 먼저 확인한 것은 `Append`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다. 처음에는 `Append` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

하지만 실제로는 `rg -n "Append|ReplicateOnce" internal cmd`로 핵심 함수 위치를 다시 잡고, `Append`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 결정적으로 방향을 잡아 준 신호는 `Append` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go`의 `Append`

CLI:

```bash
$ rg -n "Append|ReplicateOnce" internal cmd
internal/replication/replication.go:14:func (log *ReplicationLog) Append(operation string, key string, value *string) int {
internal/replication/replication.go:53:	return leader.log.Append("put", key, stringPtr(value))
internal/replication/replication.go:58:	return leader.log.Append("delete", key, nil)
internal/replication/replication.go:115:func ReplicateOnce(leader *Leader, follower *Follower) int {
cmd/replication/main.go:15:	replication.ReplicateOnce(leader, follower)
cmd/replication/main.go:18:	replication.ReplicateOnce(leader, follower)
```

검증 신호:
- `Append` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `leader가 local state와 append-only log를 어떻게 함께 유지하는지 익힙니다.`

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

왜 여기서 판단이 바뀌었는가:

`Append`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Log Shipping`에서 정리한 요점처럼, leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

다음으로 넘긴 질문:
- `ReplicateOnce`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — ReplicateOnce로 같은 규칙 다시 확인하기

이번 세션의 목표는 `ReplicateOnce`가 `Append`와 어떤 짝을 이루는지 확인하는 것이었다. 초기 가설은 `ReplicateOnce`는 단순 보조 함수일 거라고 생각했다.

막상 다시 펼쳐 보니 두 번째 앵커를 읽고 나니, 실제로는 `Append`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `ReplicateOnce`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go`의 `ReplicateOnce`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
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
cmd/replication/main.go:9:func main() {
```

검증 신호:
- `ReplicateOnce`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestReplicateOnceIncrementalAndDeletes` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
func ReplicateOnce(leader *Leader, follower *Follower) int {
	entries := leader.LogFrom(follower.Watermark() + 1)
	return follower.Apply(entries)
}

func stringPtr(value string) *string {
	copyValue := value
	return &copyValue
}
```

왜 여기서 판단이 바뀌었는가:

`ReplicateOnce`가 없으면 `Append`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Log Shipping`에서 정리한 요점처럼, leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
