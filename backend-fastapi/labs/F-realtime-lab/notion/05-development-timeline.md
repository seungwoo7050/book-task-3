# 개발 타임라인: F-realtime-lab

이 문서는 소스 코드에서 드러나지 않는 개발 과정—환경 설정, 패키지 선택,
Docker 구성, 테스트 전략—을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화 — DB 없는 FastAPI

```bash
mkdir -p labs/F-realtime-lab/fastapi && cd labs/F-realtime-lab/fastapi

# pyproject.toml 생성 (name: f-realtime-lab-fastapi)
# 핵심 의존성: fastapi, httpx, pydantic-settings, redis, uvicorn[standard]
# ⚠️ sqlalchemy, alembic, psycopg 없음 — 의도적

python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

이 랩은 의도적으로 PostgreSQL과 Alembic을 제외했다.
모든 상태가 인메모리에 있으므로 마이그레이션 파일도 없다.
pyproject.toml의 의존성 목록이 다른 lab보다 가벼운 이유다.

`uvicorn[standard]`를 설치해야 WebSocket 지원(websockets 패키지)이 포함된다.
`uvicorn`만 설치하면 WebSocket handshake에서 실패할 수 있다.

## Phase 2: runtime.py — 인메모리 상태 컨테이너

```python
# app/runtime.py에 두 클래스를 정의:
#   ConnectionManager: dict[str, set[WebSocket]]
#   PresenceTracker: dict[str, float] + ttl

# app/main.py에서:
#   app.state.connections = ConnectionManager()
#   app.state.presence = PresenceTracker(ttl=settings.presence_ttl_seconds)
```

`app.state`에 저장하는 이유: FastAPI/Starlette의 `Request` 객체에서
`request.app.state`로 접근할 수 있다.
전역 변수 대신 app 인스턴스에 바인딩하면
테스트에서 앱을 새로 만들 때 상태가 격리된다.

## Phase 3: WebSocket 라우트 구현

```python
# app/api/v1/routes/realtime.py

# WS /ws/notifications/{user_id}?token=
#   1. token != user_id → close(1008)
#   2. manager.connect(user_id, ws)
#   3. while True: await ws.receive_text()  # keep-alive loop
#   4. except WebSocketDisconnect: manager.disconnect(user_id, ws)
```

`receive_text()`를 무한 루프로 호출하는 것이 WebSocket 서버의 기본 패턴이다.
클라이언트가 close frame을 보내면 `WebSocketDisconnect`가 발생하고,
finally 블록에서 정리한다.

## Phase 4: HTTP 알림 + Presence 엔드포인트

```python
# POST /notifications
#   body: {user_id, message}
#   → manager.send_to_user(user_id, {type: "notification", ...})

# POST /presence/heartbeat
#   body: {user_id}
#   → tracker.heartbeat(user_id)

# GET /presence/{user_id}
#   → {user_id, online: tracker.is_online(user_id)}
```

HTTP POST로 메시지를 받아서 WebSocket으로 fan-out하는 구조.
이것은 "쓰기는 REST, 읽기는 WebSocket"이라는 실무 패턴의 축소판이다.

## Phase 5: Docker Compose 구성

```yaml
# compose.yaml — 2개 서비스
services:
  api:       # FastAPI, 포트 8004:8000, uvicorn --reload
  redis:     # Redis 7, 포트 6381:6379
# ⚠️ PostgreSQL 서비스 없음 — 의도적
```

다른 lab들은 최소 3개 서비스(api + postgres + redis)인데,
이 랩은 api + redis 2개뿐이다.
Redis도 현재 코드에서는 직접 사용하지 않지만,
향후 pub/sub 확장을 위해 compose에 포함해 두었다.

```bash
docker compose up --build -d
# WebSocket 테스트는 wscat 또는 websocat으로:
# wscat -c "ws://localhost:8004/api/v1/ws/notifications/user1?token=user1"
```

## Phase 6: 테스트 작성

```bash
# tests/integration/test_realtime.py

# test 1: WebSocket 연결 + HTTP POST → WebSocket 수신 + presence 확인
#   1. TestClient(app)로 WebSocket 연결
#   2. HTTP POST /notifications → 메시지 전송
#   3. ws.receive_json() → 내용 확인
#   4. POST /presence/heartbeat → 상태 갱신
#   5. GET /presence/{user_id} → online 확인

# test 2: 잘못된 token → disconnect + presence TTL 만료
#   1. 잘못된 token으로 WebSocket 연결 → 1008 close
#   2. heartbeat → sleep(1.1) → presence 확인 → offline
```

WebSocket 테스트의 까다로운 점:
- Starlette `TestClient`의 WebSocket 지원은 context manager 기반이다
- close code 검증이 HTTP status code보다 불안정하다
- `time.sleep`이 필요한 시간 기반 테스트는 경계값을 피해야 한다

## Phase 7: Config와 Settings

```python
# app/core/config.py
# presence_ttl_seconds: int = 1  ← 테스트 편의를 위한 1초
# redis_url: str | None = None   ← 현재 직접 사용하지 않음
```

`presence_ttl_seconds`를 Settings에 넣어서 환경별로 조정 가능하게 했다.
프로덕션에서는 30~60초로 올려야 한다.

## Phase 8: 검증

```bash
make lint     # ruff check app tests
make test     # pytest -q

# Compose 검증
docker compose up --build -d

# HTTP 알림 → WebSocket 수신 확인 (두 터미널 필요)
# Terminal 1: WebSocket 연결
wscat -c "ws://localhost:8004/api/v1/ws/notifications/alice?token=alice"

# Terminal 2: HTTP POST
curl http://localhost:8004/api/v1/notifications -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"alice","message":"hello realtime"}'

# Terminal 1에서 메시지 수신 확인

# Presence 확인
curl http://localhost:8004/api/v1/presence/heartbeat -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"alice"}'
curl http://localhost:8004/api/v1/presence/alice

docker compose down
```

---

## 타임라인 요약

| 단계 | 핵심 산출물 |
|------|-------------|
| 초기화 | pyproject.toml (DB 없는 경량 구성) |
| runtime | ConnectionManager, PresenceTracker |
| WebSocket | /ws/notifications/{user_id} 라우트 |
| HTTP | POST /notifications, heartbeat, presence |
| Compose | api + redis (PostgreSQL 없음, 2 서비스) |
| 테스트 | WebSocket 수신 검증, close code, TTL 만료 |
| 검증 | lint, test, wscat 수동 검증 |
