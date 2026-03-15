# Scope, Ring Surface, And First Distribution

## 1. 문제 범위는 membership protocol보다 placement math에 있다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/problem/README.md)는 deterministic ring, batch routing, reassignment count, empty/single/multi-node 분산 검증을 요구한다. dynamic membership protocol, gossip, actual rebalancing execution은 뺀다.

즉 이 랩은 cluster control plane이 아니라 routing function을 먼저 고정하는 단계다.

## 2. 코드 표면은 Ring과 Router 두 층이면 끝난다

핵심 구현은 [`routing.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go)에 모여 있다.

- `Ring`: node membership, virtual node insertion, lookup, moved key count
- `Router`: single key route, batch grouping

즉 물리 data node나 shard movement worker는 등장하지 않는다. 문자열 node id와 hash ring만으로 placement semantics를 설명한다.

## 3. demo는 placement 결과 shape를 짧게 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing
GOWORK=off go run ./cmd/shard-routing
```

출력은 아래였다.

```text
alpha -> node-a
beta -> node-c
gamma -> node-b
```

이 출력은 key마다 node가 deterministic하게 정해진다는 최소 사실을 보여 준다. 하지만 이 랩의 더 중요한 부분은 distribution aggregate와 moved-key accounting이므로, 추가 재실행으로 그 숫자도 따로 고정했다.

## 4. 추가 재실행으로 분산도와 이동량을 고정했다

이번에 project root 내부 임시 Go 파일로 아래 결과를 추가로 확인했다.

```text
empty  false
distribution map[node-a:1148 node-b:939 node-c:913]
moved_after_add 259
batch map[node-a:[k5] node-b:[k1 k4] node-c:[k2 k3]]
nodes_after_remove [node-a node-c node-d]
```

이 결과는 다섯 가지를 보여 준다.

- empty ring은 lookup을 거부한다
- 3000 key 분산이 한 노드에 극단적으로 쏠리지 않는다
- 1000 key 기준 node 추가 뒤 이동량은 `259`로 절반 이하에 머문다
- batch routing은 node별 key 목록을 묶어서 돌려준다
- node 제거 뒤 membership 목록에서 해당 node는 사라진다
