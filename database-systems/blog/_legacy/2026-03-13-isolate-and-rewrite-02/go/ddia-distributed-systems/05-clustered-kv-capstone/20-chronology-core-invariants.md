# 20 05 Clustered KV Capstone의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `RouteShard`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone/capstone.go`의 `RouteShard`
- 처음 가설:
  `RouteShard` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "RouteShard|shardRing" internal cmd`로 핵심 함수 위치를 다시 잡고, `RouteShard`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "RouteShard|shardRing" internal cmd
internal/capstone/capstone.go:132:type shardRing struct {
internal/capstone/capstone.go:137:func newShardRing(virtualNodes int) *shardRing {
internal/capstone/capstone.go:141:	return &shardRing{virtualNodes: virtualNodes}
internal/capstone/capstone.go:144:func (ring *shardRing) AddShard(shardID string) {
internal/capstone/capstone.go:161:func (ring *shardRing) ShardForKey(key string) string {
internal/capstone/capstone.go:174:	router        *shardRing
internal/capstone/capstone.go:212:func (cluster *Cluster) RouteShard(key string) string {
internal/capstone/capstone.go:221:	shardID := cluster.RouteShard(key)
internal/capstone/capstone.go:238:	shardID := cluster.RouteShard(key)
internal/capstone/capstone.go:270:	shardID := cluster.RouteShard(key)
internal/capstone/capstone.go:277:	shardID := cluster.RouteShard(key)
```

검증 신호:

- `RouteShard` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `router, leader, follower, local store가 한 write pipeline 안에서 어떻게 연결되는지 익힙니다.`

핵심 코드:

```go
func (cluster *Cluster) RouteShard(key string) string {
	return cluster.router.ShardForKey(key)
}

func (cluster *Cluster) Group(shardID string) ReplicaGroup {
	return cluster.groups[shardID]
}

func (cluster *Cluster) Put(key string, value string) (string, error) {
	shardID := cluster.RouteShard(key)
	group := cluster.groups[shardID]
	store := cluster.nodes[group.Leader].stores[shardID]
	if _, err := store.AppendPut(key, value); err != nil {
		return shardID, err
```

왜 이 코드가 중요했는가:

`RouteShard`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Static Topology`에서 정리한 요점처럼, 이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

다음:

- `shardRing`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `shardRing`가 `RouteShard`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone/capstone.go`의 `shardRing`
- 처음 가설:
  `shardRing`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `RouteShard`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/clustered-kv/main.go:10:func main() {
internal/capstone/capstone.go:14:type Operation struct {
internal/capstone/capstone.go:21:type Store struct {
internal/capstone/capstone.go:27:func LoadStore(path string) (*Store, error) {
internal/capstone/capstone.go:50:func (store *Store) AppendPut(key string, value string) (Operation, error) {
internal/capstone/capstone.go:55:func (store *Store) AppendDelete(key string) (Operation, error) {
internal/capstone/capstone.go:60:func (store *Store) Apply(op Operation) error {
internal/capstone/capstone.go:86:func (store *Store) EntriesFrom(offset int) []Operation {
internal/capstone/capstone.go:96:func (store *Store) Watermark() int {
internal/capstone/capstone.go:100:func (store *Store) Get(key string) (string, bool) {
internal/capstone/capstone.go:105:func (store *Store) applyInMemory(op Operation) {
internal/capstone/capstone.go:116:type ReplicaGroup struct {
internal/capstone/capstone.go:122:type Node struct {
internal/capstone/capstone.go:127:type ringEntry struct {
internal/capstone/capstone.go:132:type shardRing struct {
internal/capstone/capstone.go:137:func newShardRing(virtualNodes int) *shardRing {
internal/capstone/capstone.go:144:func (ring *shardRing) AddShard(shardID string) {
internal/capstone/capstone.go:161:func (ring *shardRing) ShardForKey(key string) string {
internal/capstone/capstone.go:172:type Cluster struct {
internal/capstone/capstone.go:180:func NewCluster(dataDir string, groups []ReplicaGroup, virtualNodes int) (*Cluster, error) {
internal/capstone/capstone.go:208:func (cluster *Cluster) SetAutoReplicate(enabled bool) {
internal/capstone/capstone.go:212:func (cluster *Cluster) RouteShard(key string) string {
internal/capstone/capstone.go:216:func (cluster *Cluster) Group(shardID string) ReplicaGroup {
internal/capstone/capstone.go:220:func (cluster *Cluster) Put(key string, value string) (string, error) {
internal/capstone/capstone.go:237:func (cluster *Cluster) Delete(key string) (string, error) {
internal/capstone/capstone.go:254:func (cluster *Cluster) SyncFollower(shardID string, followerID string) (int, error) {
internal/capstone/capstone.go:269:func (cluster *Cluster) Read(key string) (string, bool, string, error) {
internal/capstone/capstone.go:276:func (cluster *Cluster) ReadFromNode(nodeID string, key string) (string, bool, error) {
internal/capstone/capstone.go:286:func (cluster *Cluster) RestartNode(nodeID string) error {
internal/capstone/capstone.go:301:func stringPtr(value string) *string {
internal/capstone/capstone.go:306:func itoa(value int) string {
```

검증 신호:

- `shardRing`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestRestartNodeLoadsFromDisk` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
type shardRing struct {
	virtualNodes int
	ring         []ringEntry
}

func newShardRing(virtualNodes int) *shardRing {
	if virtualNodes <= 0 {
		virtualNodes = 64
	}
	return &shardRing{virtualNodes: virtualNodes}
}
```

왜 이 코드가 중요했는가:

`shardRing`가 없으면 `RouteShard`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Static Topology`에서 정리한 요점처럼, 이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
