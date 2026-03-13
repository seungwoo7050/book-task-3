# 01 RPC Framing — Series Map

이 시리즈는 TCP byte stream 위에서 "메시지 경계가 없으면 RPC도 없다"는 가장 기초적인 사실부터 시작한다. framing을 붙인 뒤에야 timeout, error, concurrent call 같은 문제가 비로소 제대로 보이기 시작한다.

## 이 프로젝트가 답하는 질문

- length-prefix framing만으로 split chunk를 안전하게 복원할 수 있는가
- pending map과 correlation id 없이 동시 RPC 호출을 안전하게 처리할 수 있는가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-integration-and-tradeoffs.md](30-chronology-integration-and-tradeoffs.md)
4. [40-chronology-verification-and-boundaries.md](40-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/core.py`
- `python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/__main__.py`
- `python/ddia-distributed-systems/projects/01-rpc-framing/tests/test_rpc_framing.py`
- `python/ddia-distributed-systems/projects/01-rpc-framing/README.md`
- `python/ddia-distributed-systems/projects/01-rpc-framing/problem/README.md`
- `python/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/frame-boundary.md`
- `python/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/pending-map.md`
- `python/ddia-distributed-systems/projects/01-rpc-framing/pyproject.toml`

## 재검증 명령

```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m rpc_framing
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
