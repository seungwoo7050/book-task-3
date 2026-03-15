# 30 다시 돌려 보기: 현재 RPC 계층이 실제로 보장하는 것

마지막으로 남는 건 demo와 테스트, 그리고 보조 재실행에서 나온 실제 신호다. framing 계층은 말로만 설명하면 쉽게 과장된다. 실제로 어떤 입력이 어떤 예외와 어떤 출력으로 돌아오는지 다시 확인해야 현재 구현의 크기가 보인다.

## Phase 3-1. pytest는 기본 wire contract는 잘 잠근다

이번 재실행에서 pytest는 `5 passed, 1 warning in 0.05s`였다. 경고는 앞과 같은 `pytest_asyncio` deprecation이라 핵심과는 무관했다.

테스트가 잠그는 건 이렇다.

- single frame decode
- split chunk decode
- request/response round trip
- concurrent calls
- server error와 timeout 전파

즉 이 프로젝트는 단순 `echo` 데모를 넘어서, 최소한의 concurrency와 failure propagation은 이미 공개 계약에 올린다.

## Phase 3-2. demo는 "method call works"보다 "end-to-end wire path is alive"를 보여 준다

demo entry point를 다시 돌리면 이런 출력이 나온다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/01-rpc-framing
PYTHONPATH=src python3 -m rpc_framing
```

```text
{'msg': 'hello'}
```

겉보기엔 단순한 echo지만, 실제로는 frame encode, socket send, server decode/dispatch, response encode, client decode, pending map routing까지 한 번씩 다 지난 결과다. demo는 이 최소 happy path를 밖으로 보여 주는 표면이다.

## Phase 3-3. 보조 재실행이 split/multi-frame과 caller-facing 예외를 더 선명하게 보여 줬다

이번 Todo에서는 decoder와 failure path를 한 번 더 직접 확인했다.

- split decode:
  - `split1 []`
  - `split2 []`
  - `split3 ['{"a": 1}', '{"b": 2}']`
- failure propagation:
  - `unknown RuntimeError unknown method: unknown`
  - `timeout TimeoutError rpc call timed out`

이 결과는 현재 contract를 꽤 명확하게 보여 준다.

1. decoder는 half-frame을 절대 조급하게 내놓지 않는다
2. multi-frame chunk도 한 번에 분리한다
3. unknown method는 caller에게 `RuntimeError`
4. 응답이 늦으면 caller에게 `TimeoutError`

즉 이 RPC 계층은 transport-level 이벤트를 "결과가 없다"로 흐리지 않고, 호출자 입장에서 구분 가능한 실패 타입으로 다시 내보낸다.

## Phase 3-4. 지금 상태에서 비워 둔 것

- disconnect fan-out은 구현돼 있지만 테스트가 직접 덮진 않는다
- JSON codec 고정이라 binary codec pluggability가 없다
- streaming RPC가 없다
- backpressure, retry, tracing, service discovery가 없다
- server는 malformed JSON payload를 조용히 무시하고 명시적 protocol error를 보내지 않는다

그래도 이 슬롯이 중요한 이유는 분명하다. 분산 트랙의 나머지 프로젝트들이 replication이든 shard routing이든 결국 RPC transport 위에 올라가는데, 그 출발점인 frame boundary와 pending correlation을 아주 작고 선명한 코드로 먼저 고정하기 때문이다.
