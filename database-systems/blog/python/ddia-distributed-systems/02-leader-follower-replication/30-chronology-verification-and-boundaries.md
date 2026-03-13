# 30 Verification And Boundaries

## Day 1
### Session 3

검증은 아래 두 명령으로 끝난다.

```bash
cd python/ddia-distributed-systems/projects/02-leader-follower-replication
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m leader_follower
```

검증 신호:

- `3 passed`
- demo: `{'applied': 1, 'value': '1'}`

이 단계의 의미:

- `ReplicationLog`가 sequential offset을 보장
- follower는 watermark로 incremental pull
- duplicate apply는 무해(idempotent)

boundary 정리:

- 다루는 것:
  - static leader-follower 모델
  - ordered log shipping
  - delete propagation
- 다루지 않는 것:
  - leader election
  - quorum ack / majority commit
  - network partition recovery

다음 단계 연결:

`03-shard-routing`은 "어느 리더 그룹으로 보낼지"를 결정하는 슬롯이다. 02가 그룹 내부 복제라면 03은 그룹 선택이다.