# 30 Integration And Tradeoffs

## Day 1
### Session 5

서버 쪽 통합 지점은 `_dispatch()`다.

```python
response = {"type": "response", "correlation_id": request["correlation_id"]}
handler = self.handlers.get(request["method"])
if handler is None:
    response["error"] = f"unknown method: {request['method']}"
else:
    try:
        response["result"] = handler(request.get("params"))
    except Exception as error:
        response["error"] = str(error)
```

핵심은 예외를 소켓 레벨에서 터뜨리지 않고 protocol response로 반환한다는 점이다. 그래서 client는 `RuntimeError`/`TimeoutError`를 일관된 surface로 받는다.

tradeoff:

- 장점:
  - 구조 단순, correlation/timeout 책임 명확
  - split chunk, concurrency, error path를 테스트로 고정 가능
- 한계:
  - streaming RPC 없음
  - TLS/auth 없음
  - request cancellation/backpressure 없음

CLI:

```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
PYTHONPATH=src python3 -m pytest -q
```

다음 단계 연결:

`02-leader-follower-replication`에서 이 RPC 계층 위에 "ordered log shipping" 의미를 붙인다. 01이 통신 프레이밍이라면 02는 상태 동기화 semantics다.