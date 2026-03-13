# 30 Verification And Boundaries

## Day 1
### Session 5

마지막 확인은 "실제로 reopen 복구가 되는가"였다.

CLI:

```bash
cd python/database-internals/projects/02-wal-recovery
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m wal_recovery
```

검증 신호:

- `7 passed in ...`
- `{'recovered': True, 'value': '1'}`

demo는 `put("alpha", "1")` 후 close/reopen으로 recovery가 되는 가장 짧은 경로를 보여 준다. 테스트는 그 주변 경계를 채운다.

- `test_store_recovers_from_wal_after_reopen`: flush 없이 종료해도 WAL replay로 복구되는가
- `test_stop_at_corrupted_record`: 손상 tail을 신뢰하지 않고 중단하는가
- `test_force_flush_rotates_wal`: flush 후 active WAL이 회전되어 replay 범위가 줄었는가

이 시점의 boundary를 명확히 적어 두면:

- 다루는 것:
  - append-before-apply
  - CRC 기반 손상 감지
  - flush 시 WAL rotation
- 의도적으로 다루지 않는 것:
  - group commit / fsync policy 튜닝
  - partial write 복구를 위한 segment-level repair
  - compaction 시 WAL와 SSTable의 고급 상호작용

다음 단계 연결:

`03-index-filter`는 여기서 만든 "durable state" 위에서 point lookup 비용을 줄이는 단계다. WAL 복구가 write-path 안정성이라면, index/filter는 read-path 비용 제어다.