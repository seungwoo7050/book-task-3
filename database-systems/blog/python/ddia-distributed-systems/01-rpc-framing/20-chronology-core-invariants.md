# 20 핵심 invariant 붙잡기: split chunk, correlation id, failure fan-out

이 슬롯의 코드는 네트워크 치고는 매우 작지만, wire contract는 꽤 또렷하다. `encode_frame`, `FrameDecoder`, `RPCClient.call/_read_loop/_fail_all`, `RPCServer._dispatch`만 따라가면 이 프로젝트가 무엇을 보장하고 어디까지 비워 두는지 거의 다 설명된다.

## Phase 2-1. `FrameDecoder`는 byte stream에서 message boundary를 복구한다

`encode_frame()`은 payload 길이를 4-byte big-endian으로 앞에 붙인다. 이건 단순하다. 더 중요한 건 `FrameDecoder.feed()`다. 내부 buffer에 chunk를 계속 누적하고, 최소 4바이트 header가 있을 때만 size를 읽는다. 그다음 `len(buffer) >= 4 + size`가 될 때까지 기다렸다가 frame 하나를 꺼낸다.

이번 보조 재실행도 이 contract를 그대로 보여 줬다.

```text
split1 []
split2 []
split3 ['{"a": 1}', '{"b": 2}']
```

즉 split chunk가 들어와도 조급하게 half-frame을 내놓지 않고, 한 번에 두 frame이 붙어 들어와도 둘 다 정확히 분리한다.

## Phase 2-2. client의 핵심은 socket보다 pending map이다

`RPCClient.call()`을 다시 보면 진짜 중심은 `correlation_id -> queue.Queue` 맵이다.

1. 새 `correlation_id` 발급
2. pending map에 response queue 등록
3. frame 전송
4. queue에서 timeout까지 응답 대기

응답이 오면 `_read_loop()`가 JSON을 decode하고 correlation id로 pending entry를 찾아 queue에 response를 넣는다. 이 구조 덕분에 응답 도착 순서가 요청 순서와 달라도 각 caller는 자기 queue에서 자기 응답만 받는다.

즉 concurrent RPC의 진짜 계약은 request ordering이 아니라, pending map이 response routing을 보장하느냐다.

## Phase 2-3. 실패는 각 층에서 caller 쪽 예외로 다시 번역된다

`RPCServer._dispatch()`는 method lookup과 handler execution을 try/except로 감싸고, 실패하면 response에 `error` 문자열을 넣어 보낸다. client 쪽 `call()`은 응답에 `"error"`가 있으면 `RuntimeError`로 다시 올린다.

timeout은 더 직접적이다. `response_queue.get(timeout=timeout)`이 `queue.Empty`면 pending map에서 entry를 제거하고 `TimeoutError("rpc call timed out")`를 던진다.

이번 보조 재실행 결과도 그대로였다.

```text
unknown RuntimeError unknown method: unknown
timeout TimeoutError rpc call timed out
```

즉 이 슬롯은 transport error를 그냥 내부 로그로 묻지 않고, caller 입장에서 잡을 수 있는 예외로 다시 번역하는 데 집중한다.

## Phase 2-4. source-based seam: disconnect fan-out은 구현돼 있지만 테스트가 직접 덮지는 않는다

`_read_loop()`는 recv가 비면 `ConnectionError("connection closed")`를 던지고, 예외가 나면 `_fail_all(str(error))`를 호출한다. `_fail_all()`은 남아 있는 모든 pending queue에 `{"error": message}`를 넣는다. 구조상 disconnect fan-out은 분명히 구현돼 있다.

하지만 현재 테스트는 unknown method와 timeout은 직접 다루어도, connection close로 pending call 전부가 실패하는 경로를 별도 테스트로 고정하진 않는다. `close()` 경로와 `_read_loop()` 예외 처리에 source-level seam이 남아 있는 셈이다.

이 차이는 문서에 남길 가치가 있다. 지금 구현은 꽤 그럴듯하지만, 테스트 coverage가 닿는 경계와 source가 암시하는 경계는 분리해서 읽어야 하기 때문이다.
