# 40 Verification And Boundaries

## Day 1
### Session 6

최종 검증은 core 테스트와 demo를 함께 본다.

```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
python3 -m pip install -e '.[dev]'
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m clustered_kv
```

검증 신호:

- `4 passed`
- demo 출력: `{'key': 'alpha', 'value': '1', 'found': True, 'shard_id': '...'}`

테스트가 보장하는 경계:

- leader write 후 follower replication
- auto_replicate off 상태에서 수동 catch-up
- delete propagation
- node restart 후 disk log reload
- FastAPI round-trip이 core semantics를 유지

boundary 정리:

- 다루는 것:
  - shard-based routing
  - leader-follower replication
  - node-local durable log
  - API boundary 노출
- 다루지 않는 것:
  - dynamic shard movement
  - quorum/election/failure detector
  - cross-shard transaction

트랙 연결:

Python DDIA는 여기서 "정적이지만 끝까지 동작하는 작은 분산 KV"를 완성한다. Go 심화 트랙에서는 같은 골격 위에 election, quorum, failure handling이 추가된다.