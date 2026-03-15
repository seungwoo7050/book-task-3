# Core Invariants

## 1. placement hash는 MurmurHash3 위에서 deterministic하게 계산된다

`NodeForKey()`는 shared hash package의 `MurmurHash3`를 사용한다. node virtual position도 `nodeID+"#v"+index` 문자열을 같은 hash로 계산한다.

즉 이 랩의 consistent hashing은 runtime-dependent hash가 아니라 deterministic shared hash 함수 위에 선다. 같은 key와 같은 node 집합이면 placement는 항상 같다.

## 2. virtual node는 각 physical node를 ring 위 여러 점으로 쪼갠다

`AddNode()`는 `VirtualNodes` 횟수만큼 entry를 만들어 ring에 삽입한다.

```go
for i := 0; i < ring.VirtualNodes; i++ {
    entry := ringEntry{
        Hash:   hash.MurmurHash3([]byte(nodeID+"#v"+itoa(i)), 0),
        NodeID: nodeID,
    }
    ...
}
```

즉 physical node 하나가 ring 위 단일 점이 아니라 여러 점으로 퍼져 들어간다. docs의 [`virtual-nodes.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/virtual-nodes.md)가 말하는 분산도 보완이 바로 이 구조다.

## 3. lookup은 `first hash >= target`, 없으면 0번으로 wrap 한다

`NodeForKey()`는 ring에서 target hash 이상인 첫 entry를 찾고, 못 찾으면 `index = 0`으로 감아 돌아간다.

즉 hash space 끝에 있는 key도 ring 앞쪽 node로 안전하게 배치된다. consistent hash ring의 핵심 wrap-around semantics가 정확히 이 한 줄에서 나온다.

## 4. moved key count는 이전 assignment와 현재 assignment의 diff다

`MovedKeys()`는 이전 assignment map과 현재 assignment map을 비교해서 바뀐 key 수를 센다.

```go
if previous[key] != "" && previous[key] != current[key] {
    moved++
}
```

즉 actual data migration은 수행하지 않지만, "이 membership change가 얼마나 비싼가"를 정량적으로 보여 준다. 추가 재실행의 `moved_after_add 259`가 바로 이 accounting의 결과다.

## 5. source-only nuance: duplicate add/remove는 조용히 흡수된다

`AddNode()`는 이미 존재하는 node면 그냥 return하고, `RemoveNode()`는 `delete(ring.nodes, nodeID)` 뒤 filtering을 수행한다. 즉 duplicate add나 missing remove는 error가 아니라 idempotent membership update처럼 처리된다. 테스트는 이 경계를 직접 다루지 않지만, 현재 lab이 strict membership epoch보다 simple ring math를 우선했다는 신호다.
