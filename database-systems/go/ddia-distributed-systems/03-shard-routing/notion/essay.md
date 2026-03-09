# Shard Routing — 노드가 바뀌어도 키는 거의 움직이지 않는다

## 들어가며

Leader-Follower Replication이 "같은 데이터를 여러 곳에 두는 법"을 다뤘다면, 이 프로젝트는 **"데이터를 여러 곳에 나눠 두는 법"**을 다룬다. 복제(replication)가 가용성을, 샤딩(sharding)이 확장성을 담당한다.

가장 단순한 분배 방식은 `hash(key) % N`이다. 키의 해시를 노드 수로 나눈 나머지로 어떤 노드에 갈지 결정한다. 문제는 `N`이 바뀔 때 발생한다. 노드 3대에서 4대로 늘리면, 대부분의 키가 다른 노드로 재배치된다. 3000개 키 중 2000개 이상이 움직일 수 있다. 이건 실용적이지 않다.

**Consistent hashing**은 이 문제의 해법이다. 노드가 추가되거나 제거될 때, 전체 키 중 극히 일부만 재배치된다.

## Hash Ring의 원리

Consistent hash ring은 0부터 $2^{32}-1$까지의 원형 공간이다. 키와 노드 모두 이 원 위의 한 점으로 매핑된다.

키를 어떤 노드에 배치할지 결정하는 규칙: **키의 해시 값에서 시계 방향으로 가장 먼저 만나는 노드에 할당한다.**

```go
func (ring *Ring) NodeForKey(key string) (string, bool) {
    if len(ring.ring) == 0 {
        return "", false
    }
    target := hash.MurmurHash3([]byte(key), 0)
    index := slices.IndexFunc(ring.ring, func(entry ringEntry) bool {
        return entry.Hash >= target
    })
    if index == -1 {
        index = 0  // wrap around
    }
    return ring.ring[index].NodeID, true
}
```

`index == -1`은 키의 해시가 ring의 모든 entry보다 큰 경우다. 원형이므로 처음(0번)으로 돌아간다.

## Virtual Node: 편차를 줄이는 트릭

물리 노드 하나를 ring에 점 하나로 놓으면, 해시의 우연한 편향으로 특정 노드에 키가 몰릴 수 있다. Virtual node는 물리 노드 하나를 ring 위의 **여러 점**으로 분산시킨다.

```go
func (ring *Ring) AddNode(nodeID string) {
    ring.nodes[nodeID] = struct{}{}
    for i := 0; i < ring.VirtualNodes; i++ {
        entry := ringEntry{
            Hash:   hash.MurmurHash3([]byte(nodeID+"#v"+itoa(i)), 0),
            NodeID: nodeID,
        }
        // 정렬된 위치에 삽입
    }
}
```

`"node-a#v0"`, `"node-a#v1"`, ..., `"node-a#v149"` 각각을 해시하여 ring에 배치한다. 150개의 virtual node가 ring 전체에 퍼지므로, 3개 물리 노드면 450개 점이 원 위에 분포한다. 이로써 각 노드가 담당하는 키 범위가 훨씬 균일해진다.

테스트에서 이를 검증한다: 3000개 키를 3개 노드로 라우팅했을 때, 각 노드의 점유율이 20%~50% 사이여야 한다. Virtual node 없이는 이 범위를 보장하기 어렵다.

## 노드 추가와 제거

### 추가

새 노드를 ring에 추가하면, 그 노드의 virtual node들 "바로 다음" 구간에 있던 키들만 새 노드로 이동한다. 나머지는 그대로다.

테스트는 1000개 키에 대해 `node-d`를 추가한 후 moved count가 50~500 사이(5%~50%)인지 확인한다. 단순 modulo라면 ~75%가 이동했을 것이다.

### 제거

```go
func (ring *Ring) RemoveNode(nodeID string) {
    delete(ring.nodes, nodeID)
    filtered := make([]ringEntry, 0, len(ring.ring))
    for _, entry := range ring.ring {
        if entry.NodeID != nodeID {
            filtered = append(filtered, entry)
        }
    }
    ring.ring = filtered
}
```

해당 노드의 모든 virtual node를 ring에서 제거한다. 그 노드가 담당하던 키들은 시계 방향으로 다음 노드가 인수한다. 다른 노드들의 키는 변하지 않는다.

## Router: 배치 라우팅

`Router`는 `Ring` 위에 사용 편의를 위한 래퍼다. 단일 키 라우팅과 배치 라우팅을 제공한다.

```go
func (router *Router) RouteBatch(keys []string) map[string][]string {
    grouped := map[string][]string{}
    for _, key := range keys {
        nodeID, ok := router.Ring.NodeForKey(key)
        if !ok {
            continue
        }
        grouped[nodeID] = append(grouped[nodeID], key)
    }
    return grouped
}
```

배치 라우팅의 결과는 `nodeID → keys` 맵이다. 실제 분산 시스템에서는 이 맵을 보고 각 노드에 해당 키들을 한 번에 전송할 수 있다.

## 해시 함수의 선택

이 프로젝트는 `shared/hash` 패키지의 `MurmurHash3`를 사용한다. MurmurHash3는 비암호학적 해시 함수로, 빠르면서도 분포가 균일하다. 암호학적 보안이 필요 없는 consistent hashing에 이상적이다.

`itoa` 함수는 `strconv` 패키지 없이 정수를 문자열로 변환한다. 외부 의존성 최소화의 일환이지만, 실제로는 `fmt.Sprintf`를 써도 무방하다.

## 테스트가 증명하는 것들

3개 테스트가 consistent hashing의 세 가지 핵심 속성을 검증한다:

1. **EmptyAndSingleNodeRouting**: 빈 ring은 라우팅 거부, 노드 1개면 모든 키가 그 노드로
2. **DistributionAndRebalance**: 3000개 키의 분포 균형(20%~50%), 노드 추가 시 이동량 제한(5%~50%), 제거된 노드로 라우팅되지 않음
3. **BatchRouting**: 5개 키 배치 라우팅 → 총 5개 결과

## 돌아보며

Consistent hashing은 "적게 움직인다"는 직관적이고 단순한 아이디어다. 하지만 그 구현에는 virtual node, 정렬된 ring, wrap-around, rebalance accounting 같은 실질적 디테일이 필요하다. DynamoDB, Cassandra, 그리고 대부분의 분산 캐시가 이 알고리즘의 변형을 사용한다.

다음 질문: 여러 노드가 데이터를 나눠 가지면, 한 노드가 죽었을 때 누가 리더가 되는가? 이것이 다음 프로젝트(Raft Lite)의 주제다.
