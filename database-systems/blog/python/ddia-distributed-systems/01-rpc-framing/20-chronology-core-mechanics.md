# 20 Core Mechanics

## Day 1
### Session 3

RPC client의 본체는 pending map이다.

```python
correlation_id = f"req-{next(self._ids)}"
response_queue: queue.Queue = queue.Queue(maxsize=1)
with self._pending_lock:
    self._pending[correlation_id] = response_queue
```

요청을 보내고 reader thread가 응답을 받아 correlation id로 queue를 찾아 넣는다.

```python
response = json.loads(payload.decode("utf-8"))
correlation_id = response["correlation_id"]
with self._pending_lock:
    pending = self._pending.pop(correlation_id, None)
if pending is not None:
    pending.put(response)
```

이 구조가 있어야 `test_rpc_handles_concurrent_calls`가 성립한다. 소켓 하나로 동시 요청 여러 개를 보내도 결과가 섞이지 않는다.

- 목표: 동시 호출 분배가 reader thread에서 안전하게 처리되는지 확인
- 진행: `RPCClient.call/_read_loop`를 테스트와 대조

CLI:

```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
sed -n '120,260p' src/rpc_framing/core.py
sed -n '24,60p' tests/test_rpc_framing.py
```

### Session 4

timeout 경계도 명확하다.

```python
except queue.Empty as error:
    with self._pending_lock:
        self._pending.pop(correlation_id, None)
    raise TimeoutError("rpc call timed out") from error
```

timeout 직후 pending entry를 제거해 늦게 온 응답이 잘못된 호출과 결합되는 걸 막는다.

다음 질문:

- 네트워크 끊김 시 미완료 pending을 어떻게 일괄 실패 처리하나
- retry/backoff를 붙일 때 요청 멱등성은 누가 보장하나