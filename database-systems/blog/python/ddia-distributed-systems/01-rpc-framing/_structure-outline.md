# 01 RPC Framing — Structure Outline

## 이번 문서의 중심

- 이 슬롯을 RPC feature demo가 아니라 wire contract 슬롯으로 설명한다.
- 서사는 `범위 재설정 -> frame/pending/error invariant -> 검증과 seam` 순서로 둔다.
- disconnect fan-out은 구현돼 있지만 테스트가 직접 덮지 않는다는 점도 남긴다.

## Planned Files

- `00-series-map.md`
  - 질문, 읽는 순서, source-of-truth 파일, 재검증 명령
- `10-chronology-scope-and-surface.md`
  - 테스트와 문제 정의로 boundary/pending 중심 범위를 다시 잡는 글
- `20-chronology-core-invariants.md`
  - `FrameDecoder`, `RPCClient`, `RPCServer`를 중심으로 읽는 글
- `30-chronology-verification-and-boundaries.md`
  - pytest, demo, 보조 재실행으로 split/multi-frame과 failure path를 정리하는 글

## 꼭 남길 검증 신호

- `PYTHONPATH=src python3 -m pytest` -> `5 passed`
- `PYTHONPATH=src python3 -m rpc_framing` -> `{'msg': 'hello'}`
- 보조 재실행 -> split decoder가 마지막 chunk에서 2 frame 동시 복원
- unknown method -> `RuntimeError`, timeout -> `TimeoutError`

## 탈락 기준

- RPC를 method registration 설명으로 축소하면 안 된다.
- pending map의 역할을 빼면 안 된다.
- disconnect fan-out의 test gap을 숨기면 안 된다.
