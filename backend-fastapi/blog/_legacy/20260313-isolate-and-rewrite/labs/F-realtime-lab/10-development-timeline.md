# F-realtime-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: 실시간 기능이라고 하면 "채팅방을 만드는 것"을 먼저 떠올렸다. `problem/README.md`를 읽어 실제 범위를 확인한다.
- 진행: 이 랩은 채팅 제품이 아니라, WebSocket 연결 인증, presence heartbeat, fan-out이라는 세 가지 축만 떼어 연습한다. 범위가 예상보다 좁고 집중되어 있다.
- 이슈: 처음엔 Redis pub/sub을 붙여야 실시간을 설명할 수 있다고 생각했다. 그런데 이 랩은 인메모리 상태만으로 핵심 모델을 설명하고, Redis는 확장 경계로만 남긴다.
- 판단: 인메모리 `ConnectionManager`와 `PresenceTracker`를 먼저 만들고, 테스트에서 바로 검증하는 구조로 가기로 했다.

CLI:

```bash
$ cd labs/F-realtime-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: WebSocket 연결 인증을 구현한다. 처음엔 "WebSocket이니까 HTTP 인증과 완전히 다른 흐름이 필요하다"고 생각했다.
- 진행: HTTP 엔드포인트와 달리 WebSocket은 handshake 이후 헤더를 보낼 수 없다. 그래서 연결 시점에 query parameter로 token을 받아 검증해야 한다.
- 이슈: 학습용으로 어떤 수준의 인증을 넣을까? 실제 JWT 검증을 붙이면 이 랩의 초점이 흐려진다.
- 조치: `token == user_id`라는 최소 규칙으로 "인증된 연결"과 "거부된 연결"의 경계만 보여 주기로 했다.

```python
async def connect(self, *, user_id: str, token: str, websocket: WebSocket) -> None:
    if token != user_id:
        await websocket.close(code=1008)
        raise PermissionError("invalid websocket token")
    await websocket.accept()
    self.connections[user_id].add(websocket)
```

처음엔 이 규칙이 너무 단순해서 의미가 없다고 생각했다. 하지만 테스트에서 잘못된 token으로 연결하면 1008로 끊기는 것을 확인하면, "인증 실패 시 WebSocket이 어떻게 동작하는가"라는 핵심을 배울 수 있다.

- 검증: 잘못된 토큰(`token=wrong`)으로 연결하면 `WebSocketDisconnect`가 발생한다.

```python
try:
    with client.websocket_connect("/api/v1/realtime/ws/notifications/bob?token=wrong"):
        raise AssertionError("connection should not stay open")
except WebSocketDisconnect:
    pass
```

### Session 3

- 목표: presence heartbeat와 TTL 만료를 구현한다.
- 진행: 사용자가 "온라인"이라는 것은 무엇을 뜻하나? 처음엔 WebSocket 연결이 살아 있으면 온라인이라고 봤다. 하지만 연결이 끊기지 않아도 사용자가 자리를 비운 상태일 수 있다.
- 판단: 마지막 heartbeat 시각과 TTL을 비교하는 모델이 더 정확하다. heartbeat를 보내지 않으면 TTL이 지나면서 자동으로 offline이 된다.

```python
def heartbeat(self, user_id: str) -> None:
    self.last_seen[user_id] = time.monotonic()

def is_online(self, user_id: str) -> bool:
    seen_at = self.last_seen.get(user_id)
    return seen_at is not None and (time.monotonic() - seen_at) < self.ttl_seconds
```

`time.monotonic()`을 쓰는 이유는 시스템 시계 변경에 영향받지 않기 위해서다. 처음엔 `time.time()`을 썼는데, NTP 동기화 등으로 시계가 뒤로 갈 수 있어서 monotonic이 안전하다.

- 검증: heartbeat 직후 online, 1.1초 대기 후(TTL=1초) offline으로 바뀌는 것을 확인했다.

```python
heartbeat = client.post("/api/v1/realtime/presence/heartbeat", json={"user_id": "carol"})
assert heartbeat.status_code == 200
time.sleep(1.1)
assert client.get("/api/v1/realtime/presence/carol").json()["online"] is False
```

이 테스트에서 `time.sleep(1.1)`이 있다는 건 실시간 테스트에서 시간 의존성을 어떻게 다루는지 보여 준다. TTL을 1초로 줄여 놨기 때문에 테스트가 빠르게 끝난다.

### Session 4

- 목표: 알림 fan-out을 구현하고 전체를 묶어 확인한다.
- 진행: `send_notification`은 해당 user_id에 연결된 모든 WebSocket에 같은 메시지를 보낸다. 한 사용자가 여러 탭을 열어 놓은 상황을 커버한다.
- 검증: WebSocket 연결 → heartbeat → 알림 전송 → WebSocket 수신까지 하나의 테스트로 고정.

CLI:

```bash
$ pytest tests/integration/test_realtime.py -q
```

```
2 passed
```

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
2 passed
```

```bash
$ make smoke
$ docker compose up --build
```

- 다음: 이 랩은 실시간 연결 모델까지만 잡고, "이 백엔드를 어떻게 믿고 실행할 것인가"라는 운영성 질문은 G-ops-lab으로 넘긴다.
