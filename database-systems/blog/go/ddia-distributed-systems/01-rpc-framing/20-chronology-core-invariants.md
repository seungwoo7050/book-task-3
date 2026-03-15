# Core Invariants

## 1. framing decoder는 4-byte header가 다 모일 때까지 payload length를 계산하지 않는다

docs의 [`frame-boundary.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/frame-boundary.md)가 설명하듯, 이 랩의 decoder는 `[4-byte payload length][JSON payload]` 형식을 쓴다. 추가 재실행의 `split_payloads 0 1`은 바로 이 규칙의 증거다. 첫 half에서는 아직 완전한 frame이 없으니 아무 것도 내지 않고, 둘째 half가 붙은 뒤에야 payload 하나를 꺼낸다.

즉 TCP read boundary와 RPC message boundary는 전혀 다른 것으로 다뤄진다.

## 2. pending map은 correlation id를 통해 response reordering을 흡수한다

`Client.Call()`은 새 correlation id를 만들고 `pending[correlationID] = pendingCall{response chan}`를 넣는다. `readLoop()`는 response가 도착하면 그 correlation id로 pending entry를 찾아 map에서 제거하고 channel에 response를 보낸다.

이 구조 덕분에 concurrent call은 요청 순서와 다른 응답 순서에도 안전하다. 테스트 `TestRPCHandlesConcurrentCalls`가 바로 이 점을 검증한다.

## 3. unknown method와 handler error는 server가 response error로 바꿔 돌려준다

`dispatch()`는 handler가 없으면 `unknown method: ...`를 `resp.Error`에 넣고 돌려준다. handler가 error를 반환해도 마찬가지다.

즉 transport layer는 business error를 "연결이 끊겼다"와 구분되는 정상 response envelope로 실어 나른다. caller 입장에서는 `Call()`이 error를 반환하지만, wire 상에서는 response frame이 돌아온 것이다.

## 4. timeout과 disconnect는 client가 pending entry를 실패로 정리한다

`Call()`의 select는 세 갈래다.

- response channel
- `ctx.Done()`
- `client.closed`

timeout이 나면 `failPending(correlationID, ctx.Err())`로 pending entry를 정리하고 error를 반환한다. disconnect가 나면 `readLoop()`가 `failAll(err)`를 호출해 남은 pending call 전부를 실패시킨다.

즉 timeout과 connection close는 서로 다른 원인이지만, 둘 다 "pending call이 영원히 남지 않게 정리한다"는 공통 invariant를 가진다.

## 5. source-only nuance: malformed JSON request/response는 조용히 무시된다

server `handleConn()`과 client `readLoop()`는 `json.Unmarshal()`에 실패하면 그냥 `continue` 한다. 즉 malformed frame은 connection 전체를 죽이는 게 아니라 그 payload만 버린다. 테스트는 이 경계를 직접 다루지 않지만, 현재 구현이 strict protocol enforcement보다 minimal transport lab semantics를 택했다는 신호다.
