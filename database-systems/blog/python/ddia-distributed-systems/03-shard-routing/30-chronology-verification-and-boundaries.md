# Verification And Boundaries

## 1. 자동 검증은 ring의 세 가지 상태를 잡는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing
PYTHONPATH=src python3 -m pytest
```

결과는 아래였다.

```text
3 passed, 1 warning in 0.06s
```

테스트는 세 갈래다.

- empty ring과 single node에서 lookup이 어떻게 동작하는가
- 3-node distribution이 한 노드에 과도하게 치우치지 않는가
- node add/remove 이후 moved key 수와 post-remove placement가 기대 범위 안에 있는가

특히 distribution 검증은 "균등 분산을 증명한다"보다 훨씬 약한 형태다. 테스트는 3000개 샘플에서 각 노드 share가 `0.2 < share < 0.5` 범위 안에 있는지만 본다. 즉 현재 문서에서 말할 수 있는 것은 loose balance check이지, formal fairness guarantee가 아니다.

## 2. 수동 재실행에서 고정한 관찰값

이번 재작성에서 추가로 확인한 값은 아래와 같다.

- empty ring: `('', False)`
- 3000 key distribution: `{'node-a': 1010, 'node-b': 889, 'node-c': 1101}`
- 1000 key 기준 add 후 movement: `237`
- 4-node batch routing sample: `{'node-d': ['k1', 'k3', 'k4'], 'node-b': ['k2', 'k5']}`
- remove 후 membership: `['node-a', 'node-c', 'node-d']`

이 수치들 덕분에 문서가 "분산이 잘 된다"는 추상어에 머물지 않고, 현재 구현에서 실제로 어느 정도의 이동량과 분산이 관찰됐는지까지 말할 수 있게 됐다.

## 3. 현재 구현이 하지 않는 일

이번 랩을 production shard router처럼 읽으면 안 되는 이유도 분명하다.

- membership version, epoch, gossip이 없다
- data relocation job이나 background rebalance worker가 없다
- hotspot detection, load-based placement, rack awareness가 없다
- replication factor나 replica placement를 고려하지 않는다
- hash collision을 별도 observability signal로 드러내지 않는다

또 하나 분명히 적어 둘 경계가 있다. `Ring.add_node()`의 `_nodes` set과 `remove_node()`의 `discard()` 덕분에 duplicate add/remove는 사실상 idempotent하게 동작한다. 하지만 이 성질은 현재 pytest가 직접 대표 시나리오로 잠그기보다 source inspection에서 더 분명하게 읽힌다.

즉 지금 구현은 "누가 어느 shard를 맡아야 하는가"까지만 다룬다. "실제로 데이터를 어떻게 옮길 것인가"는 다음 단계 문제다.

## 4. 문서에서 일부러 피한 과장

이번 재작성에서는 아래 같은 표현을 피했다.

- "실전 shard rebalancing을 구현했다"
- "membership churn을 안정적으로 처리한다"
- "cluster-aware control plane을 완성했다"

소스가 실제로 보여 주는 것은 static membership과 deterministic placement, 그리고 reassignment accounting이다. 이 범위를 벗어난 주장은 source-first 문서의 품질을 오히려 떨어뜨린다.
