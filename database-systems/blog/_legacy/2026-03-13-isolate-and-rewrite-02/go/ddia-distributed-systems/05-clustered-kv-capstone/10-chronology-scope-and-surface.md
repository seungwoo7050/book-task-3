# 10 05 Clustered KV Capstone의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `05 Clustered KV Capstone`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/README.md`, `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/tests/capstone_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestRestartNodeLoadsFromDisk`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `RouteShard` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/clustered-kv/main.go
internal/capstone/capstone.go
tests/capstone_test.go
```

```bash
$ rg -n "^func Test" tests
tests/capstone_test.go:9:func TestWriteRoutesToLeaderAndReplicates(t *testing.T) {
tests/capstone_test.go:25:func TestFollowerCatchUpAndDelete(t *testing.T) {
tests/capstone_test.go:55:func TestRestartNodeLoadsFromDisk(t *testing.T) {
```

검증 신호:

- `TestWriteRoutesToLeaderAndReplicates`는 가장 기본 표면을 보여 줬고, `TestRestartNodeLoadsFromDisk`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `RouteShard` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestRestartNodeLoadsFromDisk(t *testing.T) {
	cluster := newCluster(t)
	shardID, err := cluster.Put("gamma", "3")
	if err != nil {
		t.Fatal(err)
	}
	group := cluster.Group(shardID)
	follower := group.Followers[0]

	if err := cluster.RestartNode(follower); err != nil {
		t.Fatal(err)
	}
	if value, ok, err := cluster.ReadFromNode(follower, "gamma"); err != nil || !ok || value != "3" {
		t.Fatalf("expected restarted node to recover value, got value=%q ok=%v err=%v", value, ok, err)
```

왜 이 코드가 중요했는가:

`TestRestartNodeLoadsFromDisk`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Replicated Write Pipeline`에서 정리한 요점처럼, write pipeline은 다음 순서를 따른다.

다음:

- `RouteShard`와 `shardRing`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone/capstone.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone/capstone.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `RouteShard` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `shardRing`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`RouteShard`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Static Topology`에서 정리한 요점처럼, 이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `shardRing`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
