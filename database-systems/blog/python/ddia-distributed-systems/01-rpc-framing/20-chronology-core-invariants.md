# 20 01 RPC Framing에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 여기서는 추상 설명을 줄이고, 실제 구현에서 invariant가 어디서 잠기는지 핵심 코드만 붙잡아 따라간다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — encode_frame에서 invariant가 잠기는 지점 보기

이 구간에서 먼저 붙잡으려 한 것은 `encode_frame`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 처음 읽을 때는 `encode_frame` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

그런데 `rg -n "encode_frame|FrameDecoder" src`로 핵심 함수 위치를 다시 잡고, `encode_frame`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `encode_frame` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/core.py`의 `encode_frame`

CLI:

```bash
$ rg -n "encode_frame|FrameDecoder" src
src/rpc_framing/core.py:13:def encode_frame(payload) -> bytes:
src/rpc_framing/core.py:19:class FrameDecoder:
src/rpc_framing/core.py:95:        decoder = FrameDecoder()
src/rpc_framing/core.py:129:        frame = encode_frame(response)
src/rpc_framing/core.py:142:        self._decoder = FrameDecoder()
src/rpc_framing/core.py:178:            self._conn.sendall(encode_frame(request))
src/rpc_framing/__init__.py:1:from .core import FrameDecoder, RPCClient, RPCServer, encode_frame
src/rpc_framing/__init__.py:3:__all__ = ["FrameDecoder", "RPCClient", "RPCServer", "encode_frame"]
```

검증 신호:
- `encode_frame` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `TCP stream에서 message boundary를 복구하는 방법을 익힙니다.`

핵심 코드:

```python
def encode_frame(payload) -> bytes:
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode("utf-8")
    return struct.pack(">I", len(payload)) + payload


class FrameDecoder:
    def __init__(self) -> None:
        self._buffer = bytearray()
```

왜 여기서 판단이 바뀌었는가:

`encode_frame`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Pending Map`에서 정리한 요점처럼, 동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

다음으로 넘긴 질문:
- `FrameDecoder`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — FrameDecoder로 같은 규칙 다시 확인하기

여기서 가장 먼저 확인한 것은 `FrameDecoder`가 `encode_frame`와 어떤 짝을 이루는지 확인한다. 처음에는 `FrameDecoder`는 단순 보조 함수일 거라고 생각했다.

하지만 실제로는 두 번째 앵커를 읽고 나니, 실제로는 `encode_frame`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 결정적으로 방향을 잡아 준 신호는 `FrameDecoder`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/core.py`의 `FrameDecoder`

CLI:

```bash
$ rg -n "^(class|def) " src
src/rpc_framing/core.py:13:def encode_frame(payload) -> bytes:
src/rpc_framing/core.py:19:class FrameDecoder:
src/rpc_framing/core.py:35:class RPCServer:
src/rpc_framing/core.py:137:class RPCClient:
src/rpc_framing/core.py:216:def demo() -> None:
```

검증 신호:
- `FrameDecoder`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_rpc_propagates_server_errors_and_timeout` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class FrameDecoder:
    def __init__(self) -> None:
        self._buffer = bytearray()

    def feed(self, chunk: bytes) -> list[bytes]:
        self._buffer.extend(chunk)
        payloads: list[bytes] = []
        while len(self._buffer) >= 4:
            size = struct.unpack(">I", self._buffer[:4])[0]
            if len(self._buffer) < 4 + size:
                break
            payloads.append(bytes(self._buffer[4 : 4 + size]))
            del self._buffer[: 4 + size]
        return payloads
```

왜 여기서 판단이 바뀌었는가:

`FrameDecoder`가 없으면 `encode_frame`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Pending Map`에서 정리한 요점처럼, 동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
