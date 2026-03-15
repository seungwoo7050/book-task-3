# 10 범위를 다시 좁히기: 이 capstone이 합치는 것은 무엇인가

이 프로젝트를 처음 다시 읽을 때 가장 먼저 걸린 부분은 이름이었다. `Clustered KV Capstone`이라는 이름만 보면 합의, failover, membership change까지 들어 있을 것처럼 느껴진다. 그런데 문제 문서와 구현을 같이 읽으면 실제 범위는 훨씬 더 선명하다. 이 project는 앞 단원에서 따로 배웠던 routing, replication, local persistence를 "한 write pipeline" 안에서 만나는 지점까지 연결하는 capstone이다.

## Session 1 — problem 문서가 먼저 빼는 것부터 확인하기

이번 Todo에서 제일 먼저 다시 본 문서는 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/problem/README.md)였다. 여기에는 해야 할 일보다 하지 않는 일이 더 중요하게 적혀 있다.

- key를 shard로 라우팅한다.
- shard별 leader/follower group을 선택한다.
- leader write를 disk-backed store에 남긴다.
- follower는 watermark 이후 entry만 catch-up한다.
- node restart 뒤 disk에서 상태를 복원한다.

반대로 문서가 명시적으로 빼는 것은 다음이다.

- dynamic membership
- automatic failover
- consensus 기반 leader election
- production deployment

이 순서가 중요한 이유는, 뒤에서 보게 될 `Cluster` 구현이 의외로 많은 책임을 한 파일에 담고 있지만 그 책임이 "작은 클러스터 전체"를 의미하지는 않기 때문이다. 범위를 먼저 고정하지 않으면 capstone을 실제보다 더 큰 시스템처럼 과대해석하게 된다.

## Session 2 — `NewCluster`가 topology를 어떻게 굳히는지 보기

핵심 구현은 [`internal/capstone/capstone.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone/capstone.go)에 거의 다 들어 있다. 그중에서도 `NewCluster`는 이 프로젝트가 어디서부터 정적이라고 가정하는지를 가장 직접적으로 보여 준다.

```go
func NewCluster(dataDir string, groups []ReplicaGroup, virtualNodes int) (*Cluster, error) {
	cluster := &Cluster{
		dataDir:       dataDir,
		router:        newShardRing(virtualNodes),
		groups:        map[string]ReplicaGroup{},
		nodes:         map[string]*Node{},
		autoReplicate: true,
	}
	for _, group := range groups {
		cluster.groups[group.ShardID] = group
		cluster.router.AddShard(group.ShardID)
		members := append([]string{group.Leader}, group.Followers...)
```

여기서 topology는 런타임에 학습되지 않는다. `groups` 배열이 곧 shard 집합, leader, follower, 그리고 node별 local store layout을 전부 결정한다. docs의 [`static-topology.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/docs/concepts/static-topology.md)가 말하는 "초기화 시점에 고정"이 실제 코드에서 어디에 박혀 있는지 바로 보인다.

## Session 3 — public surface는 놀랄 만큼 얇다

테스트와 demo가 바깥으로 보여 주는 표면도 의도적으로 작다.

- test: `TestWriteRoutesToLeaderAndReplicates`
- test: `TestFollowerCatchUpAndDelete`
- test: `TestRestartNodeLoadsFromDisk`
- demo: `key=alpha shard=shard-a follower=node-2 value=1 ok=true`

즉 공개 표면은 "라우팅이 된다", "follower가 따라온다", "restart 뒤 local log를 다시 읽는다" 정도다. 이 얇은 표면 덕분에 내부 구현이 한 파일에 몰려 있어도 독자가 어디에 집중해야 하는지는 오히려 분명해진다. 다음 글에서는 그 얇은 표면을 지키는 핵심 invariant를 실제 함수 순서로 붙잡는다.
