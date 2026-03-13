# 10 framing 은 시작일 뿐, 핵심은 요청-응답 상관관계

## Day 1
### Session 1

이 프로젝트를 처음 볼 때는 "length-prefixed protocol 연습"으로 예상했다. `encode_frame()`만 보면 맞는 말처럼 보인다.

```python
def encode_frame(payload) -> bytes:
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode("utf-8")
    return struct.pack(">I", len(payload)) + payload
```

그런데 테스트 목록을 보면 scope가 framing을 넘는다.

```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
grep -n "def test_" tests/test_rpc_framing.py
```

```text
18:def test_rpc_server_client_round_trip():
30:def test_rpc_handles_concurrent_calls():
54:def test_rpc_propagates_server_errors_and_timeout():
```

즉 핵심은 byte 경계 복원 + correlation + timeout/error surface까지다.

- 목표: framing 구현과 RPC lifecycle 책임을 분리해서 읽기
- 진행: `FrameDecoder`와 `RPCClient/RPCServer`를 따로 추적

### Session 2

`FrameDecoder.feed()`는 stream chunk를 message 단위로 재조립한다.

```python
size = struct.unpack(">I", self._buffer[:4])[0]
if len(self._buffer) < 4 + size:
    break
payloads.append(bytes(self._buffer[4 : 4 + size]))
```

`test_decoder_handles_split_chunks`가 이 경계를 고정한다. chunk 단위 네트워크 수신과 메시지 단위 처리 사이를 끊어 주는 첫 레이어다.

다음 질문:

- 동시 요청을 어떻게 구분해서 응답에 매칭하나
- timeout 시 pending 요청 정리는 어디서 처리하나
