# 30 Verification And Boundaries

## Day 1
### Session 4

검증은 routing 정확성과 rebalance 이동량 두 축으로 본다.

```bash
cd python/ddia-distributed-systems/projects/03-shard-routing
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m shard_routing
```

검증 신호:

- `3 passed`
- demo: `{'node-a': [...], 'node-b': [...]}` 형태 batch routing 결과

테스트 경계:

- empty ring / single node
- 다중 node 분산도(각 node share 범위)
- node 추가/제거 시 reassignment count
- batch routing 그룹화

boundary 정리:

- 다루는 것:
  - consistent hash ring
  - virtual node 기반 분산도 개선
  - key 이동량 관측
- 다루지 않는 것:
  - membership gossip
  - replica health 기반 routing
  - cross-shard transaction

다음 단계 연결:

`04-clustered-kv-capstone`에서 이 routing 결과가 실제 `put/delete/read` pipeline과 leader-follower 복제로 합쳐진다.