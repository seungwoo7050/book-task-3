# 01 Mini LSM Store — Structure Outline

## 이번 문서의 중심

- 첫 슬롯을 "toy KV"가 아니라 이후 LSM 계열 invariant의 압축판으로 설명한다.
- 서사는 `범위 재설정 -> flush/tombstone/reopen invariant -> 검증과 한계` 순서로 둔다.
- README 확장판처럼 되지 않도록 테스트와 보조 재실행에서 확인한 semantics를 앞에 둔다.

## Planned Files

- `00-series-map.md`
  - 질문, 읽는 순서, source-of-truth 파일, 재검증 명령
- `10-chronology-scope-and-surface.md`
  - 테스트와 문제 정의를 근거로 이 슬롯의 범위를 다시 좁히는 글
- `20-chronology-core-invariants.md`
  - `force_flush`, tombstone `None`, `open()`의 sequence ordering을 중심으로 읽는 글
- `30-chronology-verification-and-boundaries.md`
  - pytest, demo, 보조 재실행으로 공개 표면과 다음 슬롯 경계를 정리하는 글

## 꼭 남길 검증 신호

- `PYTHONPATH=src python3 -m pytest` -> `9 passed`
- `PYTHONPATH=src python3 -m mini_lsm_store` -> `{'key': 'alpha', 'found': True, 'value': '3', 'sstables': 1}`
- 보조 재실행 -> reopen 뒤 `['000002.sst', '000001.sst']`
- tombstone key -> `(None, True)` 유지

## 탈락 기준

- 단순 key-value store 소개로 끝나면 안 된다.
- tombstone `None` semantics를 빼면 안 된다.
- reopen ordering과 `_next_sequence` seam을 놓치면 다음 WAL/recovery 슬롯과 연결이 약해진다.
