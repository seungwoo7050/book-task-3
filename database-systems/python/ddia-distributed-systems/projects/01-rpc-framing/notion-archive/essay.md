# "바이트 스트림 위에 메시지를 올리는 법" — Python으로 RPC Framing 만들기

## TCP의 한계

TCP는 바이트 스트림이다. 메시지 경계가 없다. `send("hello")` 한 번과 `send("world")` 한 번을 보내면, 수신 측은 `"helloworld"` 한 덩어리를 받을 수도 있고, `"hel"`, `"loworld"`로 나눠 받을 수도 있다. 이것이 분산 시스템 트랙의 출발점이다: **바이트 스트림 위에 메시지 경계를 복원하는 것**.

## Length-Prefixed Framing

가장 간단한 해결책: 메시지 앞에 길이를 붙인다.

```python
def encode_frame(payload) -> bytes:
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode("utf-8")
    return struct.pack(">I", len(payload)) + payload
```

`struct.pack(">I", ...)` — 4바이트 big-endian unsigned int. 이 4바이트가 뒤따르는 페이로드의 길이를 알려준다. 수신 측은 먼저 4바이트를 읽어서 길이를 알고, 그만큼만 더 읽으면 메시지 하나가 완성된다.

### FrameDecoder: 조각 모아 메시지 만들기

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

`feed()`는 TCP에서 받은 chunk를 내부 버퍼에 쌓는다. 충분한 바이트가 모이면 메시지를 추출한다. 한 번의 `feed()`에서 메시지가 0개일 수도, 여러 개일 수도 있다.

테스트가 두 가지 시나리오를 검증한다:

```python
# 단일 메시지
payloads = decoder.feed(frame)
assert len(payloads) == 1

# 분할된 chunk
assert decoder.feed(frame[:half]) == []     # 아직 불완전
payloads = decoder.feed(frame[half:])       # 나머지가 오면 완성
assert len(payloads) == 1
```

Go 버전과 동일한 `while` 루프 패턴이다. 버퍼에 4바이트 이상 있으면 길이를 확인하고, 전체 페이로드가 있으면 추출하고, 없으면 더 기다린다.

## RPCServer: 요청을 받아 처리하는 쪽

### 소켓 초기화와 accept 루프

```python
class RPCServer:
    def __init__(self, address: str = "127.0.0.1:0") -> None:
        host, port = address.rsplit(":", 1)
        self._bind = (host, int(port))
```

포트 0은 OS가 빈 포트를 자동 할당한다. 테스트에서 포트 충돌을 방지하는 표준 패턴.

```python
def start(self) -> None:
    self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._socket.bind(self._bind)
    self._socket.listen()
    self._socket.settimeout(0.1)
    self._running.set()
    self._accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
    self._accept_thread.start()
```

`SO_REUSEADDR`는 서버 재시작 시 "address already in use" 방지. `settimeout(0.1)`은 accept 블로킹을 0.1초로 제한하여 `close()` 시 깨끗하게 종료할 수 있게 한다.

Go 버전이 goroutine을 쓴 자리에 Python은 `threading.Thread(daemon=True)`를 쓴다.

### 연결당 핸들러

```python
def _handle_conn(self, conn: socket.socket) -> None:
    decoder = FrameDecoder()
    writer_lock = threading.Lock()
```

각 연결마다 독립적인 FrameDecoder와 writer_lock을 갖는다. writer_lock이 필요한 이유: 서버가 하나의 연결에서 여러 요청을 동시에 처리하므로(`_dispatch`가 별도 스레드에서 실행), 응답 전송이 겹칠 수 있다.

### dispatch: handler 찾아 실행

```python
def _dispatch(self, conn, writer_lock, request):
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

핸들러가 없으면 에러 응답. 핸들러가 예외를 던지면 에러 문자열로 감싸서 응답. **correlation_id를 그대로 복사**하는 것이 핵심 — 클라이언트가 어떤 요청의 응답인지 식별할 수 있다.

## RPCClient: 요청을 보내고 응답을 기다리는 쪽

### Pending Map: 동시 요청의 비밀

```python
class RPCClient:
    def __init__(self, address: str) -> None:
        self._pending: dict[str, queue.Queue] = {}
        self._ids = count(1)
```

`_pending`은 `{correlation_id: queue.Queue}` 매핑이다. 각 요청마다 고유한 correlation_id를 생성하고, 응답을 받을 큐를 만들어 pending map에 등록한다.

### call: 요청 전송 + 응답 대기

```python
def call(self, method, params, timeout=None):
    correlation_id = f"req-{next(self._ids)}"
    response_queue = queue.Queue(maxsize=1)
    with self._pending_lock:
        self._pending[correlation_id] = response_queue
    # ... sendall ...
    response = response_queue.get(timeout=timeout)
```

`itertools.count(1)`로 단조 증가 ID를 생성한다. Go의 `atomic.AddUint64`와 같은 역할.

`queue.Queue(maxsize=1)`은 정확히 하나의 응답만 담는 채널이다. Go의 `chan`과 동등.

### read_loop: 응답 라우팅

```python
def _read_loop(self) -> None:
    while not self._closed.is_set():
        chunk = self._conn.recv(4096)
        for payload in self._decoder.feed(chunk):
            response = json.loads(payload)
            correlation_id = response["correlation_id"]
            with self._pending_lock:
                pending = self._pending.pop(correlation_id, None)
            if pending is not None:
                pending.put(response)
```

백그라운드 스레드가 소켓에서 계속 읽는다. 응답이 오면 correlation_id로 pending map에서 큐를 찾아 응답을 넣는다. `call()`에서 대기 중인 `queue.get()`이 풀린다.

### fail_all: 연결 끊김 처리

```python
def _fail_all(self, message: str) -> None:
    with self._pending_lock:
        pending = self._pending
        self._pending = {}
    for response_queue in pending.values():
        response_queue.put({"error": message})
```

연결이 끊기면 대기 중인 모든 요청에 에러를 전파한다. Go 버전의 `failAll`과 동일한 패턴.

## 동시 요청 테스트

```python
def test_rpc_handles_concurrent_calls():
    threads = []
    for index, pair in enumerate(((1, 2), (10, 20), (100, 200))):
        def worker(slot=index, a=pair[0], b=pair[1]):
            sums[slot] = client.call("add", {"a": a, "b": b})["sum"]
        thread = threading.Thread(target=worker)
        threads.append(thread)
    # ...
    assert sums == [3, 30, 300]
```

세 스레드가 동시에 `call()`을 호출한다. correlation_id 덕분에 각 응답이 올바른 caller에게 돌아간다. 이것이 pending map의 존재 이유다.

## Go 버전과의 차이

| 항목 | Go DDIA-01 | Python DDIA-01 |
|------|-----------|----------------|
| 동시성 모델 | goroutine + channel | threading + queue.Queue |
| ID 생성 | atomic.AddUint64 | itertools.count |
| 타이머 | time.Timer | queue.get(timeout=) |
| 연결 관리 | net.Listener | socket + threading.Event |
| 직렬화 | JSON | JSON (동일) |
| 테스트 수 | 5개 | 5개 |

Python의 GIL 때문에 진정한 병렬 실행은 아니지만, I/O 바운드 작업(소켓 읽기/쓰기)에서는 스레딩이 충분히 효과적이다.

## 마무리

이 프로젝트는 분산 시스템의 가장 기초적인 문제를 해결한다: **네트워크를 통해 함수를 호출하는 것**. TCP의 바이트 스트림에서 메시지를 복원하고, correlation_id로 동시 요청을 구분하고, timeout과 에러를 전파한다.

소스코드에서 드러나지 않는 핵심: **`queue.Queue(maxsize=1)`이 Go의 `chan`과 동일한 역할을 한다.** 각 요청마다 1-slot 큐를 만들고, read_loop이 응답을 넣고, call()이 꺼내는 구조. 이 패턴이 동시 요청을 가능하게 하는 핵심 메커니즘이다.
