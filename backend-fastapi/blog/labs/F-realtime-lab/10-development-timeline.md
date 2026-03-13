# F-realtime-lab: HTTP로는 표현되지 않는 연결 상태를 별도 모델로 만들기

이 글은 `labs/F-realtime-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py::notifications_ws`, `labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py::test_invalid_token_disconnects_and_presence_expires`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

F 랩은 기능을 하나 더 붙이는 프로젝트가 아니라, 시간과 연결을 API surface로 옮기는 프로젝트다. problem/README.md가 WebSocket 인증, TTL heartbeat, fan-out, reconnect용 보조 HTTP surface를 같이 요구하는 이유도 이 때문이다. 이 글에서도 '알림을 보냈다'보다 '연결 상태를 어떻게 모델링했는가'를 따라가는 편이 맞다.

## 1. 실시간 전달을 별도 상태 모델로 정의하기
먼저 WebSocket을 HTTP 확장으로 보지 않고 별도 모델로 잡았다. docs/README.md는 연결 상태와 사용자 상태의 차이, heartbeat와 TTL, fan-out을 먼저 묻는다. 그래서 이 랩의 public surface도 단순 /notifications와 /ws 조합이 아니라, presence heartbeat와 presence 조회 endpoint를 같이 가진다.

## 2. WebSocket connect와 heartbeat를 분리된 surface로 두기
핵심 코드는 notifications_ws다. 여기서는 connection manager가 token을 검증해 websocket을 붙이고, tracker가 heartbeat(user_id)를 즉시 갱신한다. 이후 receive loop가 돌 때마다 다시 heartbeat를 밀어 넣는다. 이 함수 하나로 '연결이 살아 있음'과 '사용자가 지금 online으로 간주됨'이 어떻게 이어지는지가 보인다.

```python
async def notifications_ws(
    websocket: WebSocket,
    user_id: str,
    token: str = Query(...),
) -> None:
    manager: ConnectionManager = websocket.app.state.connection_manager
    tracker: PresenceTracker = websocket.app.state.presence_tracker
    try:
        await manager.connect(user_id=user_id, token=token, websocket=websocket)
        tracker.heartbeat(user_id)
        while True:
            await websocket.receive_text()
```

이 장면은 연결 인증, presence 갱신, 수신 loop가 하나의 연결 lifecycle을 이룬다는 사실을 보여 준다.

## 3. presence 만료와 잘못된 token을 테스트로 고정하기
테스트는 이 구조의 취약한 지점을 바로 찌른다. 하나는 잘못된 token으로 접속했을 때 연결이 유지되면 안 된다는 점, 다른 하나는 heartbeat를 끊으면 TTL이 지나 offline으로 바뀌어야 한다는 점이다. tests/integration/test_realtime.py는 time.sleep(1.1)까지 써서 이 만료 semantics를 아주 노골적으로 고정한다.

```python
def test_invalid_token_disconnects_and_presence_expires(client) -> None:
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

테스트는 잘못된 token disconnect와 TTL 만료가 runtime에서 어떻게 드러나는지 보여 준다.

## 4. 2026-03-09 재검증으로 health/probe surface를 닫기
재검증 단계에서는 다른 랩과 마찬가지로 compile, lint, test, smoke, Compose probe가 남아 있다. 실시간 프로젝트라도 마지막 확인 surface는 결국 /health/live, /health/ready 같은 HTTP endpoint다. 이 균형 덕분에 연결 모델을 다루는 랩이면서도 독립 워크스페이스로 관리할 수 있다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/F-realtime-lab/fastapi 8004
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다. 실시간 메시지 자체보다 연결과 presence semantics를 다시 재현할 수 있는지가 핵심이었다.

## 정리
F 랩에서 새로 배운 것은 WebSocket route를 하나 만드는 법이 아니다. 더 중요한 건 연결 상태, 사용자 상태, 메시지 전달을 같은 값처럼 보지 않는 태도다. 다음 G 랩이 운영성에 집중할 수 있는 것도, 여기서 이미 '무엇을 관찰해야 하는가'의 대상을 분리해 두었기 때문이다.
