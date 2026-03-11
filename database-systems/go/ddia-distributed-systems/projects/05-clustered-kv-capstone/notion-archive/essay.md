# Clustered KV Capstone — 모든 조각을 하나로 합치다

## 들어가며

분산 시스템 시리즈의 마지막 프로젝트다. 지금까지 독립적으로 만들어 온 네 가지 구성요소를 하나의 시스템으로 통합한다:

- **01-rpc-framing**: 네트워크 통신 기반 (이 프로젝트에서는 in-process 호출로 대체)
- **02-leader-follower-replication**: mutation log와 watermark 기반 복제
- **03-shard-routing**: consistent hash ring으로 키를 샤드에 배치
- **04-raft-lite**: 합의 알고리즘 (이 프로젝트에서는 정적 리더로 단순화)

그리고 database-internals 시리즈에서 다룬 **디스크 영속화**까지 결합한다. 결과물은 "작지만 완전한 분산 KV 스토어"다.

## 설계 결정: 정적 토폴로지

이 캡스톤의 가장 중요한 설계 결정은 **정적 토폴로지**다. 샤드 집합과 각 샤드의 leader/follower 배치가 초기화 시점에 고정된다. 멤버십 변경, 리더 재선출, 동적 리밸런싱은 범위 밖이다.

왜? 저장 엔진, 라우팅, 복제를 **한 번에 연결하는 첫 통합 단계**에서 reconfiguration 복잡도를 배제하기 위해서다. 각 개별 패턴이 올바르게 연결되는지 확인하는 것만으로도 충분히 의미가 있다.

```go
cluster, err := capstone.NewCluster(dataDir, []capstone.ReplicaGroup{
    {ShardID: "shard-a", Leader: "node-1", Followers: []string{"node-2"}},
    {ShardID: "shard-b", Leader: "node-2", Followers: []string{"node-3"}},
}, 64)
```

두 개의 샤드, 세 개의 노드. `node-1`은 `shard-a`의 리더이자 `shard-b`의 팔로워가 아닌 — 역할이 겹치지 않게 배치했다. `node-2`는 두 샤드 모두에 참여하여 크로스 샤드 노드 역할을 한다.

## Store: 디스크 위의 Mutation Log

`Store`는 이 프로젝트의 저장 엔진이다. database-internals 시리즈의 WAL과 replication 시리즈의 log를 하나로 합친 것이다.

```go
type Store struct {
    path string
    data map[string]string
    log  []Operation
}
```

세 가지 상태를 동시에 유지한다:
1. **path**: 디스크 파일 경로
2. **data**: 인메모리 키-값 맵 (빠른 읽기)
3. **log**: 인메모리 operation 슬라이스 (복제용 + offset 관리)

### 디스크 포맷

파일은 JSON Lines 형식이다. 한 줄에 하나의 Operation:

```json
{"offset":0,"type":"put","key":"alpha","value":"1"}
{"offset":1,"type":"delete","key":"alpha"}
```

`LoadStore`는 파일을 줄 단위로 읽으며 각 operation을 순서대로 재생한다. 노드 재시작 시 이 함수 하나로 상태가 완전히 복원된다.

### Idempotent Apply

```go
func (store *Store) Apply(op Operation) error {
    if op.Offset < len(store.log) {
        return nil  // 이미 적용한 offset → skip
    }
    if op.Offset != len(store.log) {
        return fmt.Errorf("store: non-sequential offset %d", op.Offset)
    }
    // 디스크에 쓰고, 인메모리에 적용
}
```

두 가지 안전장치:
1. **Idempotent**: offset이 이미 적용된 것이면 무시. 복제 재시도에도 안전.
2. **Non-sequential 감지**: offset이 건너뛰면 에러. 로그 무결성 보호.

## Shard Ring: 내장된 Consistent Hash

`shardRing`은 03-shard-routing의 Ring을 capstone 내부에 재구현한 것이다. 동일한 알고리즘—virtual node, MurmurHash3, wrap-around—을 사용한다.

```go
func (ring *shardRing) ShardForKey(key string) string {
    target := hash.MurmurHash3([]byte(key), 0)
    index := slices.IndexFunc(ring.ring, func(entry ringEntry) bool {
        return entry.Hash >= target
    })
    if index == -1 {
        index = 0
    }
    return ring.ring[index].ShardID
}
```

차이점은 물리 노드를 라우팅하는 대신 **논리 샤드**를 라우팅한다는 것이다. 샤드와 노드의 관계는 `ReplicaGroup`이 정의한다.

## Write Pipeline

```
클라이언트 → Cluster.Put(key, value)
    1. RouteShard(key) → shardID
    2. groups[shardID].Leader → leaderNodeID
    3. nodes[leaderNodeID].stores[shardID].AppendPut(key, value)
    4. 각 follower에 대해 SyncFollower(shardID, followerID)
```

Step 4는 `autoReplicate`가 true일 때만 실행된다. 테스트에서 수동 catch-up을 검증하기 위해 이 플래그를 끌 수 있다.

`SyncFollower`는 02-replication의 `ReplicateOnce`와 동일한 패턴이다:

```go
func (cluster *Cluster) SyncFollower(shardID string, followerID string) (int, error) {
    entries := leaderStore.EntriesFrom(followerStore.Watermark() + 1)
    for _, entry := range entries {
        followerStore.Apply(entry)
    }
}
```

Leader의 로그에서 follower의 watermark 이후 entry를 가져와 적용한다. Idempotent apply 덕분에 중복 전송해도 안전하다.

## Read 경로

두 가지 읽기 방식을 제공한다:

1. **Read(key)**: 라우팅 → 리더에서 읽기. 최신 보장.
2. **ReadFromNode(nodeID, key)**: 특정 노드에서 직접 읽기. follower가 아직 catch-up하지 않았으면 stale read.

```go
func (cluster *Cluster) ReadFromNode(nodeID string, key string) (string, bool, error) {
    shardID := cluster.RouteShard(key)
    node := cluster.nodes[nodeID]
    if node == nil || node.stores[shardID] == nil {
        return "", false, fmt.Errorf("node %s is not replica for shard %s", nodeID, shardID)
    }
    value, ok := node.stores[shardID].Get(key)
    return value, ok, nil
}
```

해당 노드가 그 샤드의 replica가 아니면 에러를 반환한다.

## 노드 재시작과 복구

```go
func (cluster *Cluster) RestartNode(nodeID string) error {
    for shardID := range node.stores {
        store, err := LoadStore(filepath.Join(cluster.dataDir, nodeID, shardID+".log"))
        node.stores[shardID] = store
    }
}
```

노드의 모든 샤드 스토어를 디스크에서 다시 로드한다. JSON Lines 파일의 각 줄을 재생하여 인메모리 상태를 복원한다. 이것이 "디스크 기반 저장소"의 핵심 가치다.

## 테스트가 증명하는 것들

3개 테스트가 통합 시나리오를 검증한다:

1. **WriteRoutesToLeaderAndReplicates**: Put → 리더와 팔로워 모두에서 값 확인
2. **FollowerCatchUpAndDelete**: 자동 복제 끔 → Put → 팔로워 lag 확인 → 수동 SyncFollower → 캐치업 확인 → Delete 복제 확인
3. **RestartNodeLoadsFromDisk**: Put → RestartNode(follower) → 재시작 후에도 값 유지

`newCluster` 헬퍼는 `t.TempDir()`로 테스트 격리된 디렉터리를 사용한다.

## 돌아보며

이 캡스톤은 새로운 알고리즘을 소개하지 않는다. 대신, 지금까지 만든 모든 조각이 실제로 **함께 작동할 수 있는지**를 증명한다. Consistent hash ring이 키를 라우팅하고, leader의 디스크 로그에 기록되고, follower가 watermark로 따라잡고, 노드가 재시작해도 상태가 살아남는다.

레거시에는 이런 통합 프로젝트가 없었다. 분산 모듈과 저장 엔진이 각각 따로 존재했다. 이 프로젝트가 그 간극을 메운다. 정적 토폴로지라는 제약은 있지만, 분산 KV 스토어의 전체 흐름을 한 파일 안에서 처음부터 끝까지 따라갈 수 있다.
