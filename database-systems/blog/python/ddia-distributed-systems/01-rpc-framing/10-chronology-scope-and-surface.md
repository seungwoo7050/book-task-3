# 10 범위를 다시 좁히기: 이 슬롯의 중심은 RPC 기능이 아니라 wire contract다

처음엔 RPC 프로젝트라서 handler registration이나 request/response API가 중심일 거라고 생각하기 쉽다. 그런데 테스트와 문제 정의를 다시 읽어 보면, 실제 초점은 훨씬 더 아래에 있다. 이 슬롯이 먼저 고정하는 건 application method가 아니라 `frame boundary`와 `correlation_id` 계약이다.

## Phase 1. 테스트가 boundary recovery와 pending map을 먼저 앞으로 끌어낸다

`tests/test_rpc_framing.py`를 다시 보면 다섯 테스트가 두 덩어리로 나뉜다.

- decoder가 split chunk와 single frame을 어떻게 복구하는가
- client/server가 concurrent call, server error, timeout을 어떻게 처리하는가

이 배치는 중요하다. 여기서 이미 "RPC method call 기능"보다 "TCP stream 위에서 어떻게 메시지를 분리하고 다시 대응시키는가"가 먼저라는 사실이 드러난다. 특히 `test_rpc_handles_concurrent_calls`가 있는 순간, 이 프로젝트는 순차 요청 데모를 넘어선다. 응답 순서와 요청 순서가 어긋나도 caller별 결과를 분리할 수 있어야 한다는 뜻이다.

이번 재실행:

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/01-rpc-framing
PYTHONPATH=src python3 -m pytest
```

결과:

```text
5 passed, 1 warning in 0.05s
```

## Phase 2. 문제 정의가 일부러 transport core만 남긴다

`problem/README.md`를 다시 보면 이 슬롯이 의도적으로 다루지 않는 것도 분명하다.

- TLS 없음
- 인증 없음
- streaming RPC 없음
- 서비스 디스커버리/로드 밸런싱 없음

즉 이 프로젝트는 RPC framework를 만드는 게 아니라, 분산 트랙의 나머지 슬롯이 올라탈 최소 transport core를 먼저 만든다. 그래서 docs도 `frame-boundary`와 `pending-map` 두 문서만 앞에 둔다. method registry보다 먼저, byte stream과 pending state가 문제라는 뜻이다.
