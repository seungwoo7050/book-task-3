# Verification And Boundaries

## 1. 자동 검증은 empty ring, distribution, rebalance, batch routing을 함께 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/ddia-distributed-systems/projects/03-shard-routing/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- empty ring rejection
- single-node routing
- multi-node distribution
- moved key count after add
- removed node exclusion
- batch routing total size

즉 placement semantics와 rebalance accounting이 둘 다 검증된다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
alpha -> node-a
beta -> node-c
gamma -> node-b
```

추가 재실행 출력:

```text
empty  false
distribution map[node-a:1148 node-b:939 node-c:913]
moved_after_add 259
batch map[node-a:[k5] node-b:[k1 k4] node-c:[k2 k3]]
nodes_after_remove [node-a node-c node-d]
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- empty ring은 명시적으로 miss를 돌려준다
- virtual node 덕분에 3-node 분산이 한 노드에 과도하게 치우치지 않는다
- membership 추가 뒤 moved key 수는 제한적이다
- batch routing은 network fan-out 친화적인 grouped shape를 준다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 full sharding control plane으로 읽으면 안 된다.

- gossip이 없다
- membership epoch가 없다
- actual data relocation job이 없다
- replica placement가 없다
- rack awareness와 hotspot mitigation이 없다

즉 static placement function과 rebalance accounting만 다룬다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "실전 shard management를 구현했다"
- "rebalancing을 자동화했다"
- "cluster membership 문제를 해결했다"

현재 소스와 테스트가 실제로 보여 주는 것은 virtual node ring, deterministic placement, moved-key accounting, batch grouping까지다. 그보다 큰 sharding claim은 근거가 없다.
