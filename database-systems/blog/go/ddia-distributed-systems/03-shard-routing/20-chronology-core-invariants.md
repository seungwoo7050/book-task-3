# 20 03 Shard Routing에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 여기서는 추상 설명을 줄이고, 실제 구현에서 invariant가 어디서 잠기는지 핵심 코드만 붙잡아 따라간다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Router에서 invariant가 잠기는 지점 보기

이 구간에서 먼저 붙잡으려 한 것은 `Router`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 처음 읽을 때는 `Router` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

그런데 `rg -n "Router|ringEntry" internal cmd`로 핵심 함수 위치를 다시 잡고, `Router`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `Router` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go`의 `Router`

CLI:

```bash
$ rg -n "Router|ringEntry" internal cmd
cmd/shard-routing/main.go:15:	router := routing.NewRouter(ring)
internal/routing/routing.go:9:type ringEntry struct {
internal/routing/routing.go:16:	ring         []ringEntry
internal/routing/routing.go:36:		entry := ringEntry{
internal/routing/routing.go:40:		index := slices.IndexFunc(ring.ring, func(candidate ringEntry) bool {
internal/routing/routing.go:46:			ring.ring = append(ring.ring[:index], append([]ringEntry{entry}, ring.ring[index:]...)...)
internal/routing/routing.go:53:	filtered := make([]ringEntry, 0, len(ring.ring))
internal/routing/routing.go:76:	index := slices.IndexFunc(ring.ring, func(entry ringEntry) bool {
internal/routing/routing.go:107:type Router struct {
internal/routing/routing.go:111:func NewRouter(ring *Ring) *Router {
internal/routing/routing.go:112:	return &Router{Ring: ring}
internal/routing/routing.go:115:func (router *Router) Route(key string) (string, bool) {
internal/routing/routing.go:119:func (router *Router) RouteBatch(keys []string) map[string][]string {
```

검증 신호:
- `Router` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `consistent hash ring이 key를 물리 node에 매핑하는 방식을 익힙니다.`

핵심 코드:

```go
type Router struct {
	Ring *Ring
}

func NewRouter(ring *Ring) *Router {
	return &Router{Ring: ring}
}

func (router *Router) Route(key string) (string, bool) {
	return router.Ring.NodeForKey(key)
}
```

왜 여기서 판단이 바뀌었는가:

`Router`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Virtual Nodes`에서 정리한 요점처럼, 물리 node마다 ring에 하나의 점만 두면 hash 편차 때문에 분산이 쉽게 치우친다. virtual node는 물리 node 하나를 ring 위의 여러 점으로 쪼개서 더 고르게 분산되도록 만든다.

다음으로 넘긴 질문:
- `ringEntry`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — ringEntry로 같은 규칙 다시 확인하기

여기서 가장 먼저 확인한 것은 `ringEntry`가 `Router`와 어떤 짝을 이루는지 확인한다. 처음에는 `ringEntry`는 단순 보조 함수일 거라고 생각했다.

하지만 실제로는 두 번째 앵커를 읽고 나니, 실제로는 `Router`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 결정적으로 방향을 잡아 준 신호는 `ringEntry`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go`의 `ringEntry`

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/shard-routing/main.go:9:func main() {
internal/routing/routing.go:9:type ringEntry struct {
internal/routing/routing.go:14:type Ring struct {
internal/routing/routing.go:20:func NewRing(virtualNodes int) *Ring {
internal/routing/routing.go:30:func (ring *Ring) AddNode(nodeID string) {
internal/routing/routing.go:51:func (ring *Ring) RemoveNode(nodeID string) {
internal/routing/routing.go:62:func (ring *Ring) Nodes() []string {
internal/routing/routing.go:71:func (ring *Ring) NodeForKey(key string) (string, bool) {
internal/routing/routing.go:85:func (ring *Ring) Assignments(keys []string) map[string]string {
internal/routing/routing.go:96:func (ring *Ring) MovedKeys(keys []string, previous map[string]string) int {
internal/routing/routing.go:107:type Router struct {
internal/routing/routing.go:111:func NewRouter(ring *Ring) *Router {
internal/routing/routing.go:115:func (router *Router) Route(key string) (string, bool) {
internal/routing/routing.go:119:func (router *Router) RouteBatch(keys []string) map[string][]string {
internal/routing/routing.go:131:func itoa(value int) string {
```

검증 신호:
- `ringEntry`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestBatchRouting` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
type ringEntry struct {
	Hash   uint32
	NodeID string
}

type Ring struct {
	VirtualNodes int
	ring         []ringEntry
	nodes        map[string]struct{}
}
```

왜 여기서 판단이 바뀌었는가:

`ringEntry`가 없으면 `Router`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Virtual Nodes`에서 정리한 요점처럼, 물리 node마다 ring에 하나의 점만 두면 hash 편차 때문에 분산이 쉽게 치우친다. virtual node는 물리 node 하나를 ring 위의 여러 점으로 쪼개서 더 고르게 분산되도록 만든다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
