# 10 01 RPC Framing를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 여기서는 구현 세부사항을 서둘러 설명하지 않고, 무엇을 먼저 고정해야 하는지 범위부터 다시 좁힌다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

이번 세션의 목표는 `01 RPC Framing`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악하는 것이었다. 초기 가설은 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

막상 다시 펼쳐 보니 `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. 특히 `test_rpc_propagates_server_errors_and_timeout`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `encode_frame` 주변의 invariant를 고정하는 일이라는 게 보였다. 여기서 해석을 바꾼 단서는 `test_decoder_handles_single_message`는 가장 기본 표면을 보여 줬고, `test_rpc_propagates_server_errors_and_timeout`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/README.md`, `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/tests/test_rpc_framing.py`

CLI:

```bash
$ find src tests -type f | sort
src/rpc_framing/__init__.py
src/rpc_framing/__main__.py
src/rpc_framing/__pycache__/__init__.cpython-312.pyc
src/rpc_framing/__pycache__/__init__.cpython-314.pyc
src/rpc_framing/__pycache__/__main__.cpython-312.pyc
src/rpc_framing/__pycache__/__main__.cpython-314.pyc
src/rpc_framing/__pycache__/core.cpython-312.pyc
src/rpc_framing/__pycache__/core.cpython-314.pyc
src/rpc_framing/core.py
tests/__pycache__/test_rpc_framing.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_rpc_framing.cpython-312-pytest-9.0.2.pyc
tests/__pycache__/test_rpc_framing.cpython-314-pytest-9.0.2.pyc
tests/test_rpc_framing.py
```

```bash
$ rg -n "^def test_" tests
tests/test_rpc_framing.py:7:def test_decoder_handles_single_message():
tests/test_rpc_framing.py:14:def test_decoder_handles_split_chunks():
tests/test_rpc_framing.py:23:def test_rpc_server_client_round_trip():
tests/test_rpc_framing.py:35:def test_rpc_handles_concurrent_calls():
tests/test_rpc_framing.py:60:def test_rpc_propagates_server_errors_and_timeout():
```

검증 신호:
- `test_decoder_handles_single_message`는 가장 기본 표면을 보여 줬고, `test_rpc_propagates_server_errors_and_timeout`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `encode_frame` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```python
def test_rpc_propagates_server_errors_and_timeout():
    server = RPCServer()

    def fail(_params):
        raise ValueError("intentional failure")

    def slow(_params):
        time.sleep(0.2)
        return {"status": "done"}
```

왜 여기서 판단이 바뀌었는가:

`test_rpc_propagates_server_errors_and_timeout`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Frame Boundary Recovery`에서 정리한 요점처럼, TCP는 message 단위가 아니라 byte stream이다. 따라서 sender가 한 번 `Write` 했다고 receiver가 한 번 `Read`로 같은 단위를 받는다는 보장이 없다.

다음으로 넘긴 질문:
- `encode_frame`와 `FrameDecoder`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이 구간에서 먼저 붙잡으려 한 것은 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 처음 읽을 때는 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

그런데 가장 큰 구현 파일인 `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/core.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `encode_frame` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/01-rpc-framing/src/rpc_framing/core.py`

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
- `encode_frame` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `FrameDecoder`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`encode_frame`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Pending Map`에서 정리한 요점처럼, 동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `FrameDecoder`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
