# 05 MVCC — Structure Outline

## 이번 문서의 중심

- 이 슬롯을 generic transaction manager가 아니라 snapshot visibility core로 설명한다.
- 서사는 `범위 재설정 -> snapshot/conflict/gc invariant -> 검증과 한계` 순서로 둔다.
- GC가 active reader가 없을 때 최신 version 하나만 남길 수 있는 현재 semantics도 분명히 남긴다.

## Planned Files

- `00-series-map.md`
  - 질문, 읽는 순서, source-of-truth 파일, 재검증 명령
- `10-chronology-scope-and-surface.md`
  - 테스트와 문제 정의로 visibility core 범위를 다시 잡는 글
- `20-chronology-core-invariants.md`
  - `VersionStore`와 `TransactionManager`를 중심으로 읽는 글
- `30-chronology-verification-and-boundaries.md`
  - pytest, demo, 보조 재실행으로 chain semantics와 한계를 정리하는 글

## 꼭 남길 검증 신호

- `PYTHONPATH=src python3 -m pytest` -> `7 passed`
- `PYTHONPATH=src python3 -m mvcc_lab` -> `{'tx': 1, 'read_your_own_write': 10}`
- 보조 재실행 -> `snapshot_read v1`
- conflict 후 loser version cleanup, GC 후 latest one-version chain

## 탈락 기준

- MVCC를 transaction 전반으로 과장하면 안 된다.
- read-your-own-write를 빼면 안 된다.
- aggressive GC semantics를 숨기면 문서가 지나치게 매끈해진다.
