# F-realtime-lab development timeline

이 글은 F 랩을 "알림을 WebSocket으로 보내는 예제"로 요약하지 않는다. 현재 남아 있는 source of truth를 따라가면, 이 프로젝트의 핵심은 연결 상태와 사용자 상태를 어떻게 분리해서 모델링할 것인가에 있다. 실제로 눈에 띄는 건 `token == user_id` 수준으로 단순화된 WebSocket 인증, TTL 기반 presence 판정, 한 사용자당 여러 소켓을 묶는 fan-out, 그리고 이 모든 것을 `app.state` 인메모리 객체로 유지하는 구조다.

## Phase 1. 문제 정의가 메시지 내용보다 연결 모델을 먼저 요구한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/problem/README.md) 와 [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/docs/README.md) 를 먼저 보면, 이 랩이 진짜로 묻는 건 "알림 payload를 어떻게 보내는가"보다 "HTTP로는 안 보이는 연결 상태를 어떻게 별도 모델로 설명할 것인가"에 가깝다. WebSocket 인증, TTL heartbeat, fan-out, reconnect 보조 HTTP surface가 성공 기준으로 같이 붙어 있는 이유도 여기에 있다.

이 순서가 중요하다. 실시간 기능을 읽을 때 흔히 message broker나 payload format부터 보게 되지만, F 랩은 먼저 connection lifecycle을 세운다. 누가 지금 연결돼 있는지, 누가 online으로 간주되는지, 그 둘이 언제 어긋날 수 있는지가 먼저다.

## Phase 2. WebSocket 연결과 presence 판정은 일부러 다른 표면으로 나뉜다

[`realtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py) 를 보면 surface가 세 갈래로 나뉜다. 하나는 `POST /presence/heartbeat`, 다른 하나는 `GET /presence/{user_id}`, 마지막은 `POST /notifications`와 `GET /ws/notifications/{user_id}`다. 이 배열이 중요한 이유는 "연결이 살아 있다"와 "online으로 보인다"를 같은 API로 처리하지 않기 때문이다.

```python
@router.post("/presence/heartbeat", response_model=PresenceResponse)
def heartbeat(
    payload: PresenceHeartbeatRequest,
    tracker: Annotated[PresenceTracker, Depends(get_presence_tracker)],
) -> PresenceResponse:
    tracker.heartbeat(payload.user_id)
    return PresenceResponse(user_id=payload.user_id, online=True)
```

이 랩은 receive loop 안에서도 heartbeat를 밀어 넣지만, 동시에 HTTP heartbeat surface를 따로 둔다. 그래서 reconnect 직후나 보조 채널에서 online 판정을 다시 세우는 이야기를 분리해서 할 수 있다.

## Phase 3. 실제 핵심 로직은 DB가 아니라 app.state의 인메모리 runtime에 있다

이 프로젝트의 중심은 [`runtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/runtime.py) 와 [`main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/main.py) 를 같이 볼 때 보인다. 앱 시작 시 `ConnectionManager()`와 `PresenceTracker(ttl_seconds=...)`를 `app.state`에 넣고, dependency는 그 객체를 그대로 꺼내 쓴다.

```python
app.state.connection_manager = ConnectionManager()
app.state.presence_tracker = PresenceTracker(ttl_seconds=settings.presence_ttl_seconds)
```

`ConnectionManager`는 `dict[str, set[WebSocket]]`으로 사용자별 소켓 집합을 들고 있고, `send_notification()`은 그 집합 전체에 JSON을 쏜다. `PresenceTracker`는 `last_seen` monotonic timestamp만 저장하고 TTL 내인지 여부로 online을 계산한다. 즉 Redis와 DB는 readiness surface에는 남아 있지만, 현재 실시간 전달 자체는 아직 메모리 모델이 핵심이다.

## Phase 4. 인증도 fan-out도 학습 목적에 맞게 아주 좁게 남겨 두었다

`notifications_ws()`에서 인증은 꽤 의도적으로 단순하다. `ConnectionManager.connect()`는 `token != user_id`면 WebSocket을 `1008`로 닫고 `PermissionError`를 던진다.

```python
async def connect(self, *, user_id: str, token: str, websocket: WebSocket) -> None:
    if token != user_id:
        await websocket.close(code=1008)
        raise PermissionError("invalid websocket token")
    await websocket.accept()
    self.connections[user_id].add(websocket)
```

이 선택 덕분에 문서는 복잡한 인증 체계 대신 "연결이 인증된 사용자와 묶여야 한다"는 최소 규칙만 붙잡으면 된다. 같은 이유로 fan-out도 현재는 한 사용자의 여러 소켓에 보내는 수준까지로 선명하고, 방/채널, replay, broker 확장 같은 더 큰 문제는 범위 밖으로 남겨 둔다.

## Phase 5. 테스트는 잘못된 연결과 TTL 만료를 가장 먼저 고정한다

[`test_realtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py) 는 두 가지를 같이 고정한다. 하나는 정상 WebSocket 연결 뒤 HTTP notification이 실제로 해당 소켓에 fan-out 되는지다. 다른 하나는 잘못된 token 접속은 즉시 끊겨야 하고, heartbeat 뒤 TTL이 지나면 `online`이 `False`가 되어야 한다는 점이다.

```python
try:
    with client.websocket_connect("/api/v1/realtime/ws/notifications/bob?token=wrong"):
        raise AssertionError("connection should not stay open")
except WebSocketDisconnect:
    pass

heartbeat = client.post("/api/v1/realtime/presence/heartbeat", json={"user_id": "carol"})
assert heartbeat.status_code == 200
time.sleep(1.1)
assert client.get("/api/v1/realtime/presence/carol").json()["online"] is False
```

이 테스트가 중요한 이유는 실시간 랩의 핵심을 "메시지를 받았다"에서 멈추지 않게 만들기 때문이다. 연결이 실패할 때와 상태가 만료될 때의 수렴 방식이 같이 보여야 connection model이 설명 가능해진다.

## Phase 6. 오늘 다시 돌린 검증은 runtime 자체와 공식 진입점 문제를 분리해서 보여 준다

2026-03-14 현재 셸에서 다시 실행한 명령은 아래와 같다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇게 갈렸다.

- `make lint`: 통과.
- `make test`: `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: Homebrew `python3` 기준 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`: WebSocket 통합 테스트 2개 통과. 다만 `pytest_asyncio` deprecation warning이 남는다.
- `PYTHONPATH=. python -m tests.smoke`: `/api/v1/health/live` 200으로 통과.

즉 F 랩은 현재 셸에서도 runtime 모델과 통합 테스트 핵심 경로 자체는 살아 있다. 다만 기본 `make` 진입점은 여전히 import path와 interpreter 선택 때문에 바로 닫히지 않는다. 문서가 이 차이를 남겨야만 "실시간 모델은 작동한다"와 "공식 재검증 루프는 아직 매끈하지 않다"를 동시에 전달할 수 있다.

## 정리

F-realtime-lab이 실제로 남기는 건 WebSocket route 하나가 아니다. 연결 상태와 사용자 상태를 분리하고, presence를 TTL로 계산하며, fan-out을 사용자별 소켓 집합으로 다루는 태도다. 현재 구현은 그 모든 걸 인메모리 runtime으로 아주 작게 보여 주고, Redis/DB는 readiness와 확장 경계 쪽에만 남겨 둔다. 다음 G 랩이 운영성과 관찰 가능성으로 넘어갈 때도, 먼저 무엇을 상태로 보고 무엇을 health surface로 닫을지 여기서 이미 배워 둔 셈이다.
