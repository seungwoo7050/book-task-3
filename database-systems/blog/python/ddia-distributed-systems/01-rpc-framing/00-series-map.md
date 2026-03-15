# 01 RPC Framing 시리즈 맵

분산 트랙의 첫 슬롯이라서 네트워크 프로토콜 전부를 다룰 것처럼 보이지만, 실제로는 훨씬 작고 선명한 문제를 붙잡는다. `01 RPC Framing`의 중심은 TCP byte stream 위에서 message boundary를 복구하고, 동시에 여러 요청이 날아갈 때 응답을 올바른 caller에게 되돌리는 최소 계약을 만드는 데 있다.

## 먼저 보고 갈 질문

- framing에서 가장 먼저 고정해야 하는 건 payload 형식인가, boundary recovery인가?
- 왜 pending map이 없으면 concurrent RPC는 바로 불안정해지는가?
- timeout, unknown method, disconnect 같은 실패는 어디서 caller에게 다시 전파되는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
   테스트와 문제 정의를 다시 보며 이 슬롯의 중심이 serialization보다 stream boundary와 pending map이라는 점을 먼저 잡는다.
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
   `encode_frame`, `FrameDecoder`, `RPCClient.call/_read_loop/_fail_all`, `RPCServer._dispatch`가 실제로 어떤 wire contract를 고정하는지 본다.
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)
   pytest, demo, 보조 재실행으로 split chunk, multi-frame chunk, concurrent call, error propagation이 실제로 어떤 신호로 보이는지 정리한다.

## 재검증 명령

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/01-rpc-framing
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m rpc_framing
```

## 이번 시리즈의 근거

- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/README.md`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/problem/README.md`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/docs/README.md`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/frame-boundary.md`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/pending-map.md`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/core.py`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/__main__.py`
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/tests/test_rpc_framing.py`

## 보조 메모

작업 메모는 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)에 남긴다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 읽어도 충분하다.
