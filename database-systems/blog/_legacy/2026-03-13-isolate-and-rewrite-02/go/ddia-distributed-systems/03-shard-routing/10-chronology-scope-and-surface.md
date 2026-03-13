# 10 03 Shard Routing의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `03 Shard Routing`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/README.md`, `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/tests/routing_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestBatchRouting`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Router` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/shard-routing/main.go
internal/routing/routing.go
tests/routing_test.go
```

```bash
$ rg -n "^func Test" tests
tests/routing_test.go:9:func TestEmptyAndSingleNodeRouting(t *testing.T) {
tests/routing_test.go:21:func TestDistributionAndRebalance(t *testing.T) {
tests/routing_test.go:59:func TestBatchRouting(t *testing.T) {
```

검증 신호:

- `TestEmptyAndSingleNodeRouting`는 가장 기본 표면을 보여 줬고, `TestBatchRouting`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Router` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestBatchRouting(t *testing.T) {
	ring := routing.NewRing(100)
	ring.AddNode("node-a")
	ring.AddNode("node-b")
	router := routing.NewRouter(ring)

	grouped := router.RouteBatch([]string{"k1", "k2", "k3", "k4", "k5"})
	total := 0
	for _, keys := range grouped {
		total += len(keys)
	}
	if total != 5 {
		t.Fatalf("expected 5 routed keys, got %d", total)
	}
```

왜 이 코드가 중요했는가:

`TestBatchRouting`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Rebalance Accounting`에서 정리한 요점처럼, consistent hashing의 핵심 가치는 membership 변화가 있을 때 전체 key를 거의 다 움직이지 않는다는 점이다. 그래서 구현을 검증할 때는 "새 ring이 얼마나 적은 key를 옮겼는가"를 함께 본다.

다음:

- `Router`와 `ringEntry`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `Router` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `ringEntry`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

왜 이 코드가 중요했는가:

`Router`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Virtual Nodes`에서 정리한 요점처럼, 물리 node마다 ring에 하나의 점만 두면 hash 편차 때문에 분산이 쉽게 치우친다. virtual node는 물리 node 하나를 ring 위의 여러 점으로 쪼개서 더 고르게 분산되도록 만든다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `ringEntry`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
