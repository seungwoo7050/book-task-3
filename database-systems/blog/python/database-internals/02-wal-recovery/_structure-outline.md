# 02 WAL Recovery — Structure Outline

## 이번 문서의 중심

- WAL을 부가 기능이 아니라 write path 재정의로 설명한다.
- 서사는 `범위 재설정 -> append/recover/rotate invariant -> 검증과 한계` 순서로 둔다.
- `fsync_enabled` seam처럼 이름과 실제 동작이 어긋나는 지점도 source-based limitation으로 남긴다.

## Planned Files

- `00-series-map.md`
  - 질문, 읽는 순서, source-of-truth 파일, 재검증 명령
- `10-chronology-scope-and-surface.md`
  - 테스트와 문제 정의로 durable write path 범위를 다시 잡는 글
- `20-chronology-core-invariants.md`
  - WAL record format, stop-on-corruption, replay, rotation을 중심으로 읽는 글
- `30-chronology-verification-and-boundaries.md`
  - pytest, demo, 보조 재실행으로 file-level 결과와 다음 확장 경계를 정리하는 글

## 꼭 남길 검증 신호

- `PYTHONPATH=src python3 -m pytest` -> `7 passed`
- `PYTHONPATH=src python3 -m wal_recovery` -> `{'recovered': True, 'value': '1'}`
- 보조 재실행 -> `before_flush_wal_size 37`, `after_flush_wal_size 0`
- corruption 재실행 -> 앞의 두 record만 replay

## 탈락 기준

- WAL을 로그 파일 추가 정도로 축소하면 안 된다.
- corruption 이후 stop-on-corruption policy를 빼면 안 된다.
- `fsync_enabled`가 실제 fsync를 호출하는 것처럼 쓰면 안 된다.
