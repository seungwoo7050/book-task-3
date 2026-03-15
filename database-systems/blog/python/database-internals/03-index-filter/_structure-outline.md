# 03 Index Filter — Structure Outline

## 이번 문서의 중심

- 이 슬롯을 Bloom filter 설명서가 아니라 read-cost optimization 슬롯으로 설명한다.
- 서사는 `범위 재설정 -> bloom/index/footer invariant -> 검증 숫자와 한계` 순서로 둔다.
- docs와 source가 어긋나는 해시 설명도 source-based limitation으로 남긴다.

## Planned Files

- `00-series-map.md`
  - 질문, 읽는 순서, source-of-truth 파일, 재검증 명령
- `10-chronology-scope-and-surface.md`
  - 테스트와 문제 정의로 이 슬롯의 중심이 bytes read 경계라는 점을 다시 잡는 글
- `20-chronology-core-invariants.md`
  - filter, sparse index, footer, lookup stats를 중심으로 읽는 글
- `30-chronology-verification-and-boundaries.md`
  - pytest, demo, 보조 재실행으로 bloom reject와 bounded scan 숫자를 정리하는 글

## 꼭 남길 검증 신호

- `PYTHONPATH=src python3 -m pytest` -> `4 passed`
- `PYTHONPATH=src python3 -m index_filter` -> `{'found': True, 'value': 'value-k023', 'bytes_read': 176}`
- 보조 재실행 -> `footer_magic b'SIF1'`
- missing key -> `bytes_read=0`, hit key -> bounded `block_range`

## 탈락 기준

- Bloom filter 이론 설명으로만 끝나면 안 된다.
- sparse index의 bounded scan 역할을 빼면 안 된다.
- 문서와 source의 해시 구현 차이를 숨기면 안 된다.
