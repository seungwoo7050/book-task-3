# 04 Buffer Pool — Structure Outline

## 이번 문서의 중심

- 이 슬롯을 LRU 구현 설명이 아니라 page lifecycle 관리로 설명한다.
- 서사는 `범위 재설정 -> LRU/pin/dirty invariant -> 검증과 seam` 순서로 둔다.
- pinned eviction failure가 완전 rollback이 아니라는 현재 runtime 확인도 함께 남긴다.

## Planned Files

- `00-series-map.md`
  - 질문, 읽는 순서, source-of-truth 파일, 재검증 명령
- `10-chronology-scope-and-surface.md`
  - 테스트와 문제 정의로 page lifecycle 중심 범위를 다시 잡는 글
- `20-chronology-core-invariants.md`
  - `LRUCache`, `fetch_page`, `unpin_page`, `flush_page`를 중심으로 읽는 글
- `30-chronology-verification-and-boundaries.md`
  - pytest, demo, 보조 재실행으로 current seam까지 정리하는 글

## 꼭 남길 검증 신호

- `PYTHONPATH=src python3 -m pytest` -> `7 passed`
- `PYTHONPATH=src python3 -m buffer_pool` -> `pin_count: 1`, `prefix: page-0`
- 보조 재실행 -> pinned eviction 시 `RuntimeError`
- error 뒤 cache keys가 `['...:0', '...:2']`로 남는 현재 seam

## 탈락 기준

- buffer pool을 단순 cache로 축소하면 안 된다.
- pin/dirty semantics를 빼면 안 된다.
- failed eviction rollback 문제를 빼면 문서가 지나치게 깨끗해진다.
