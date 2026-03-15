# 20 핵심 상태 전이: route, append, catch-up, restart

이 capstone에서 중요한 것은 기능 목록이 아니라 상태 전이의 연결 순서다. `Put` 한 번이 어디서 shard를 고르고, 어떤 파일에 append되고, follower는 어느 offset부터 따라오며, restart는 무엇만 복원하는지를 붙잡아야 문서가 README 확장판이 되지 않는다.

## Session 1 — `RouteShard`는 routing만 하는 것이 아니라 replica group 선택의 입구다

`Cluster`의 write/read path는 모두 `RouteShard`에서 시작한다.

```go
func (cluster *Cluster) Put(key string, value string) (string, error) {
	shardID := cluster.RouteShard(key)
	group := cluster.groups[shardID]
	store := cluster.nodes[group.Leader].stores[shardID]
	if _, err := store.AppendPut(key, value); err != nil {
		return shardID, err
	}
```

`RouteShard` 자체는 `router.ShardForKey` 한 줄이지만, 그 다음 줄에서 곧바로 `group := cluster.groups[shardID]`가 붙는다. 그래서 이 함수는 단순 hash helper가 아니라 "어느 leader store가 authoritative write target인가"를 결정하는 입구가 된다.

여기서 실제 routing 규칙은 `shardRing.AddShard`와 `ShardForKey`가 잡고 있다.

- shard마다 `virtualNodes` 개수만큼 ring entry를 추가한다.
- hash는 `MurmurHash3(shardID+"#v"+itoa(i), 0)`로 계산한다.
- key hash보다 크거나 같은 첫 entry를 고르고, 없으면 ring 처음으로 wrap-around한다.

이 구조 때문에 capstone은 dynamic rebalancing을 구현하지 않으면서도, 앞선 shard-routing project의 핵심인 "consistent ring 위의 정적 배치"는 그대로 재사용한다.

## Session 2 — append-before-visibility와 follower watermark

local persistence 쪽 invariant는 `Store.Apply`가 거의 전부 말해 준다.

```go
func (store *Store) Apply(op Operation) error {
	if op.Offset < len(store.log) {
		return nil
	}
	if op.Offset != len(store.log) {
		return fmt.Errorf("store: non-sequential offset %d", op.Offset)
	}
	...
	if _, err := file.Write(append(buffer, '\n')); err != nil {
		return err
	}
	store.applyInMemory(op)
	store.log = append(store.log, op)
	return nil
}
```

여기서 중요한 점은 세 가지다.

- offset이 현재 log 길이보다 작으면 duplicate replay로 보고 무시한다.
- 중간 offset이 오면 non-sequential error를 낸다.
- 파일 append가 끝난 뒤에야 in-memory map과 log slice를 갱신한다.

즉 visibility보다 append가 먼저다. follower catch-up도 이 규칙 위에서 돌아간다.

```go
func (cluster *Cluster) SyncFollower(shardID string, followerID string) (int, error) {
	leaderStore := cluster.nodes[group.Leader].stores[shardID]
	followerStore := cluster.nodes[followerID].stores[shardID]
	entries := leaderStore.EntriesFrom(followerStore.Watermark() + 1)
```

`EntriesFrom(follower watermark + 1)`라는 한 줄이 이 프로젝트의 replication contract를 거의 다 설명한다. follower는 term이나 quorum을 모른다. 대신 "내가 마지막으로 가진 offset 다음부터"만 가져온다. 그래서 이 capstone의 replication은 consensus가 아니라 ordered log shipping에 가깝다.

## Session 3 — restart는 cluster recovery가 아니라 local replay다

테스트 이름만 보면 `RestartNode`가 꽤 큰 recovery를 하는 것처럼 느껴질 수 있다. 그런데 실제 구현은 훨씬 더 제한적이다.

```go
func (cluster *Cluster) RestartNode(nodeID string) error {
	node := cluster.nodes[nodeID]
	...
	for shardID := range node.stores {
		store, err := LoadStore(filepath.Join(cluster.dataDir, nodeID, shardID+".log"))
		if err != nil {
			return err
		}
		node.stores[shardID] = store
	}
	return nil
}
```

`RestartNode`는 각 shard log file을 다시 읽어 `Store`를 재구성할 뿐이다. 실제로 임시 검증에서 `autoReplicate=false` 상태로 follower를 lagging 상태에 둔 뒤 restart하면 `restart_without_sync_ok=false`가 나왔다. 즉 restart는 "이미 내 디스크에 있던 것"만 복구한다. leader에게 가서 모자란 entry를 가져오지는 않는다.

이 차이를 명확히 적어 둬야 하는 이유는, `TestRestartNodeLoadsFromDisk`가 보장하는 것은 disk replay이지 cluster-wide healing이 아니기 때문이다. 그 경계를 흐리면 이후 quorum/election 단원과 이 capstone의 역할이 섞여 버린다.
