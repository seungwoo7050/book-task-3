# 01 RPC Framing — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
python3 --version
# Python 3.14.x

python3 -m pip install -U pytest
```

### 디렉토리 구조 생성

```bash
mkdir -p src/rpc_framing tests docs/concepts docs/references
touch src/rpc_framing/__init__.py
touch src/rpc_framing/__main__.py
touch src/rpc_framing/core.py
touch tests/test_rpc_framing.py
```

**결정**: 모든 구현을 `core.py` 하나에 집중. 프레임 인코딩, 디코더, 서버, 클라이언트가 긴밀하게 연결되므로 분리 불필요.

---

## Phase 1: Frame Encoding / Decoding

### 1.1 encode_frame

```python
def encode_frame(payload) -> bytes:
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode("utf-8")
    return struct.pack(">I", len(payload)) + payload
```

`struct.pack(">I", ...)` — 4바이트 big-endian unsigned int. Go 버전의 `binary.BigEndian.PutUint32`와 동일.

**결정**: dict가 들어오면 자동 JSON 직렬화. bytes가 들어오면 그대로 사용.

### 1.2 FrameDecoder

```python
class FrameDecoder:
    def __init__(self) -> None:
        self._buffer = bytearray()

    def feed(self, chunk: bytes) -> list[bytes]:
```

`bytearray` 내부 버퍼에 chunk를 쌓고, 완전한 프레임이 있으면 추출.

### 1.3 디코더 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_rpc_framing.py::test_decoder_handles_single_message -v
PYTHONPATH=src python3 -m pytest tests/test_rpc_framing.py::test_decoder_handles_split_chunks -v
```

- 단일 메시지: 한 번에 전체 프레임 → 1개 추출
- 분할 chunk: 반만 보내면 0개, 나머지 보내면 1개

---

## Phase 2: RPCServer

### 2.1 소켓 설정

```python
self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
self._socket.bind(self._bind)
self._socket.listen()
self._socket.settimeout(0.1)
```

**결정 사항**:
- `SO_REUSEADDR`: 테스트 반복 실행 시 포트 재사용
- `settimeout(0.1)`: accept 블로킹을 짧게 제한하여 `close()` 시 빠른 종료
- 포트 0: OS 자동 할당으로 충돌 방지

### 2.2 accept 루프

```python
def _accept_loop(self) -> None:
    while self._running.is_set():
        try:
            conn, _ = self._socket.accept()
        except TimeoutError:
            continue
```

`threading.Event`로 실행/종료 상태 관리. `TimeoutError`는 `settimeout(0.1)` 때문에 정상적으로 발생.

### 2.3 연결 핸들러

각 연결마다:
1. 독립적인 `FrameDecoder`
2. 독립적인 `writer_lock` (응답 전송 직렬화)
3. 요청마다 별도 스레드에서 `_dispatch` 실행

### 2.4 handler 등록과 dispatch

```python
server.register("echo", lambda params: params)
```

lambda로 간단한 핸들러 등록. `_dispatch`에서 핸들러를 찾아 실행하고, 결과 또는 에러를 correlation_id와 함께 응답.

---

## Phase 3: RPCClient

### 3.1 Pending Map 패턴

```python
self._pending: dict[str, queue.Queue] = {}
self._ids = count(1)
```

**결정**: `itertools.count(1)`로 단조 증가 ID. Go의 `atomic.AddUint64`에 해당. Python의 GIL 덕분에 별도 동기화 불필요.

### 3.2 call() 구현

```python
correlation_id = f"req-{next(self._ids)}"
response_queue = queue.Queue(maxsize=1)
```

**결정**: `queue.Queue(maxsize=1)` = Go의 `chan` 역할. 요청당 하나의 1-slot 큐를 생성하여 응답을 받음.

### 3.3 read_loop

백그라운드 스레드에서 소켓 읽기 → FrameDecoder → JSON 파싱 → correlation_id로 pending map에서 큐 찾기 → 응답 전달.

### 3.4 fail_all

연결 끊김 시 대기 중인 모든 요청에 에러 전파.

### 3.5 round-trip 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_rpc_framing.py::test_rpc_server_client_round_trip -v
```

echo 핸들러로 기본 요청/응답 확인.

---

## Phase 4: 동시성과 에러 처리

### 4.1 동시 요청 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_rpc_framing.py::test_rpc_handles_concurrent_calls -v
```

3개 스레드에서 동시에 `call()`. correlation_id 덕분에 각 응답이 올바른 caller에게 돌아감.

**Python threading 세부사항**: worker 함수의 기본 인수 `slot=index, a=pair[0], b=pair[1]`는 closure 캡처 문제 방지. 루프 변수를 기본 인수로 바인딩하는 Python 관용구.

### 4.2 에러와 타임아웃 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_rpc_framing.py::test_rpc_propagates_server_errors_and_timeout -v
```

두 가지 시나리오:
1. 핸들러 예외 → `response["error"]`로 전파 → 클라이언트에서 `RuntimeError`
2. 느린 핸들러(0.2초) + 짧은 timeout(0.02초) → `TimeoutError`

---

## Phase 5: Demo와 마무리

### 5.1 demo 실행

```bash
PYTHONPATH=src python3 -m rpc_framing
# {"msg": "hello"}
```

### 5.2 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

5개 테스트 모두 통과 확인.

---

## Phase 6: 개념 문서 작성

### docs/concepts/frame-boundary.md
- TCP 바이트 스트림에서 메시지 경계 복원
- 4-byte length prefix 프로토콜

### docs/concepts/pending-map.md
- correlation ID + pending call map
- 동시 요청의 응답 라우팅

---

## 소스코드에서 드러나지 않는 결정들

1. **threading vs asyncio**: Python 분산 시스템에서 asyncio가 더 자연스럽지만, Go 버전과의 구조적 대응을 위해 threading 선택. goroutine ↔ Thread, channel ↔ Queue 매핑.

2. **writer_lock**: 서버에서 하나의 연결에 대해 여러 _dispatch 스레드가 동시에 응답을 보낼 수 있으므로 Lock 필요. Go에서는 channel로 직렬화했지만 Python에서는 Lock이 더 직관적.

3. **daemon=True**: 모든 스레드를 데몬으로 설정. 메인 스레드 종료 시 자동 종료. 테스트에서 잔여 스레드가 남지 않게 보장.

4. **settimeout(0.1)**: accept 루프의 블로킹을 짧게 제한. 이것이 없으면 `close()` 호출 후에도 스레드가 block 상태로 남음.

5. **`queue.Queue(maxsize=1)`**: maxsize=1은 의도적. 하나의 요청에 하나의 응답만 대응. Go의 unbuffered channel과 동등.

6. **JSON 직렬화**: 프레임 내용은 항상 JSON. 바이너리 프로토콜이 아닌 이유 — 학습 목적에서 디버깅 편의성이 성능보다 중요.
