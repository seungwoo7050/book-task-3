# 02 WAL Recovery 시리즈 맵

이 프로젝트는 바로 앞의 mini LSM store에 durability를 붙이는 첫 단계다. 핵심은 기능을 많이 늘리는 게 아니라, write가 memtable에 반영되기 전에 먼저 어떤 파일 흔적을 남길 것인지 고정하는 데 있다. 그래서 읽을 때도 `append -> apply -> recover -> rotate` 순서를 먼저 붙드는 편이 맞다.

## 먼저 보고 갈 질문

- acknowledged write를 잃지 않으려면 왜 memtable보다 WAL append가 먼저여야 하는가?
- 손상된 WAL을 만났을 때 왜 "첫 손상 지점에서 중단"하는 보수적 정책을 택하는가?
- flush 이후 `active.wal`을 비우고 다시 여는 rotation이 read path와 recovery에 어떤 영향을 주는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
   테스트와 문제 정의를 다시 보며 이 슬롯이 단순 logging이 아니라 durable write path 재구성이라는 점을 먼저 잡는다.
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
   `WriteAheadLog`, `recover()`, `DurableStore.open()`, `force_flush()`가 실제로 어떤 상태 전이를 고정하는지 본다.
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)
   pytest, demo, 보조 재실행으로 recovery와 rotation이 실제 파일 상태에서 어떻게 보이는지 정리한다.

## 재검증 명령

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/02-wal-recovery
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m wal_recovery
```

## 이번 시리즈의 근거

- `database-systems/python/database-internals/projects/02-wal-recovery/README.md`
- `database-systems/python/database-internals/projects/02-wal-recovery/problem/README.md`
- `database-systems/python/database-internals/projects/02-wal-recovery/docs/README.md`
- `database-systems/python/database-internals/projects/02-wal-recovery/docs/concepts/wal-record-format.md`
- `database-systems/python/database-internals/projects/02-wal-recovery/docs/concepts/recovery-policy.md`
- `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/store.py`
- `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/__main__.py`
- `database-systems/python/database-internals/projects/02-wal-recovery/tests/test_wal_recovery.py`

## 보조 메모

작업 메모는 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)에 남긴다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 읽어도 충분하다.
