# Scope, Ring Surface, First Measurements

## 1. 문제는 router를 만든다고 해서 cluster를 만드는 건 아니다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/problem/README.md)는 요구사항을 네 가지로 자른다. deterministic consistent hash ring, batch routing, add/remove 이후 reassignment count 계산, 그리고 empty/single/multi-node 상황 검증이다.

여기서 중요한 건 일부러 빠진 범위다. dynamic membership protocol, gossip, 실제 data movement execution은 포함하지 않는다. 즉 이 랩의 목적은 "cluster membership control plane"이 아니라 "routing function과 rebalance accounting"이다.

## 2. 코드 표면은 Ring과 Router 두 개면 끝난다

핵심 구현은 [`core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py)에 모두 들어 있다.

- `Ring`: node membership, ring entry 정렬, key lookup, moved key 계산을 담당한다.
- `Router`: `Ring` 위에서 단건 `route()`와 batch `route_batch()`를 제공한다.

이 구조가 보여 주는 건 shard routing을 별도 분산 프로토콜이 아니라 "deterministic pure function에 가까운 계층"으로 보는 시각이다. 실제 데이터 노드는 등장하지 않고, node identifier 문자열만으로도 대부분의 개념을 설명할 수 있다.

## 3. virtual node는 물리 노드를 여러 점으로 찢는다

docs의 [`virtual-nodes.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/virtual-nodes.md)는 `nodeID#v<index>`를 해시해 ring entry를 만든다고 요약한다. 실제 구현도 같다.

```python
for index in range(self.virtual_nodes):
    entry = RingEntry(hash_value(f"{node_id}#v{index}"), node_id)
    bisect.insort(self.ring, entry)
```

기본 virtual node 수는 `Ring(virtual_nodes=150)`이지만, `0`이 들어와도 `self.virtual_nodes = virtual_nodes or 150` 때문에 결국 150으로 보정된다. 즉 "virtual node를 끄는" 모드는 현재 없다.

## 4. 첫 데모가 보여 주는 것

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing
PYTHONPATH=src python3 -m shard_routing
```

출력은 아래와 같았다.

```python
{'node-a': ['k1', 'k3', 'k4'], 'node-b': ['k2']}
```

demo는 ring에 `node-a`, `node-b`를 넣고 `route_batch()`를 실행한다. 여기서 중요한 건 특정 key가 어느 노드로 갔는지가 아니라, batch 결과가 "node별로 key를 묶은 map"이라는 점이다. 즉 router 표면은 key 하나씩 조회하는 API보다 "다음 단계에서 병렬 전송하기 쉬운 grouped assignment"를 더 중시한다.

## 5. 수동 재실행으로 다시 본 분산도

추가로 3000개 key를 넣어 distribution을 다시 계산했다.

```python
distribution {'node-a': 1010, 'node-b': 889, 'node-c': 1101}
```

비율로 바꾸면 대략 33.7%, 29.6%, 36.7%다. 테스트가 요구하는 `0.2 < share < 0.5` 범위 안에 들어온다. 이 수치는 "완벽하게 균등하다"는 뜻이 아니라, virtual node를 통해 단일 물리 노드에 과도하게 몰리지 않도록 만들었다는 현재 수준의 보장을 의미한다.
