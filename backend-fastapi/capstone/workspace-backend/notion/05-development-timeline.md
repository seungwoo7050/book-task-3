# 개발 타임라인: Capstone workspace-backend

이 문서는 소스 코드에서 드러나지 않는 개발 과정—설계 의사결정, 패키지 선택,
모델 통합, Docker 구성, 테스트 전략—을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화

```bash
mkdir -p capstone/workspace-backend/fastapi && cd capstone/workspace-backend/fastapi

# pyproject.toml 생성 (name: workspace-backend-fastapi)
# 핵심 의존성: fastapi, sqlalchemy, pydantic-settings, argon2-cffi,
#              PyJWT[crypto], email-validator, psycopg[binary], redis, httpx, uvicorn[standard]
# dev 의존성: pytest, ruff

python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

capstone이므로 모든 lab의 의존성이 한 곳에 모인다:
- `argon2-cffi`: 패스워드 해싱 (A-auth-lab)
- `PyJWT[crypto]`: JWT access token (A-auth-lab, B-federation-security-lab)
- `email-validator`: 이메일 형식 검증
- `psycopg[binary]`: PostgreSQL 연결 (compose 환경)
- `redis`: rate limiter + compose

## Phase 2: core/ — 설정, 보안, 로깅, 에러

```python
# app/core/config.py — Settings 클래스
#   DB, Redis, JWT, cookie, CSRF 관련 설정 30+ fields
#   presence_ttl_seconds = 10 (F-realtime-lab에서 가져옴)
#   access_token_ttl_seconds = 900 (15분)
#   refresh_token_ttl_seconds = 14일

# app/core/security.py — 보안 함수 모음
#   password_hasher (argon2), hash_secret (hmac-sha256)
#   build_access_token, decode_access_token (PyJWT)
#   validate_csrf, set_*_cookie, clear_auth_cookies

# app/core/logging.py — JsonFormatter + configure_logging
# app/core/errors.py — AppError + register_exception_handlers
# app/core/rate_limit.py — RateLimiter (Redis/in-memory dual backend)
```

security.py에 7개 랩에서 배운 보안 패턴이 집중된다:
- Argon2 패스워드 해싱 (A)
- JWT 발행/검증 (A+B)
- HMAC으로 refresh token hash (A)
- Cookie 설정 (httpOnly, SameSite) (capstone 고유)
- CSRF double-submit 검증 (capstone 고유)

## Phase 3: DB 모델 통합

```python
# app/db/models/auth.py — 4 테이블
#   User (handle, email, password_hash, email_verified_at)
#   ExternalIdentity (user_id FK, provider, provider_subject)
#   RefreshToken (family_id, parent_token_id, token_hash, revoked_at)
#   EmailToken (kind, token_hash, expires_at, used_at)

# app/db/models/platform.py — 7 테이블
#   Workspace (name, owner_user_id FK)
#   Membership (user_id, workspace_id, role)
#   Invite (workspace_id, email, token, status)
#   Project (workspace_id, title)
#   Task (project_id, title)
#   Comment (task_id, author_user_id, body)
#   Notification (recipient_user_id, message, status)
```

총 11개 테이블. 모델 파일을 auth/platform으로 분리하되,
`bootstrap.py`에서 모두 explicit import해야 `create_all()`이 전부 생성한다.

## Phase 4: runtime.py — 실시간 상태

```python
# app/runtime.py
#   ConnectionManager: dict[str, set[WebSocket]] + connect/disconnect/send_notification
#   PresenceTracker: dict[str, float] + heartbeat/is_online

# app/main.py에서:
#   app.state.mailbox = []  # 이메일 큐 (인메모리)
#   app.state.connection_manager = ConnectionManager()
#   app.state.presence_tracker = PresenceTracker(ttl_seconds=settings.presence_ttl_seconds)
```

F-realtime-lab의 구조를 거의 그대로 가져왔지만,
`send_notification` 메서드가 `send_to_user` 대신 사용되어
notification 도메인에 맞는 이름으로 변경되었다.

## Phase 5: 서비스 레이어

```python
# app/domain/services/auth.py — AuthService
#   register: handle/email/password → User + EmailToken + mailbox append
#   verify_email: token lookup → email_verified_at 설정
#   login_local: email/password → User (이메일 인증 확인)
#   login_google: subject/email/display_name → User + ExternalIdentity
#   issue_session: User → (access_token, refresh_token, csrf_token)
#   rotate_refresh: raw_token → revoke old + issue new (reuse detection)
#   revoke_refresh: logout 시 호출

# app/domain/services/platform.py — PlatformService
#   create_workspace, invite_member, accept_invite
#   create_project, create_task, create_comment
#   drain_notifications: queued → WebSocket send → sent
#   heartbeat, is_online
```

코멘트 생성 시 같은 워크스페이스의 다른 멤버에게 Notification을 자동 생성한다.
이것은 E-async-jobs-lab의 "outbox에 기록" 패턴을 간소화한 것이다.

## Phase 6: API 라우트

```python
# app/api/v1/routes/auth.py
#   POST /register, /verify-email, /login, /google/login
#   GET /me
#   POST /token/refresh (requires CSRF), /logout (requires CSRF)

# app/api/v1/routes/platform.py
#   POST /workspaces, /workspaces/{id}/invites, /invites/{token}/accept
#   POST /workspaces/{id}/projects, /projects/{id}/tasks, /tasks/{id}/comments
#   POST /notifications/drain
#   POST /presence/heartbeat, GET /presence/{user_id}
#   WS /ws/notifications?access_token=

# app/api/v1/routes/health.py
#   GET /health/live, /health/ready
```

## Phase 7: Docker Compose 구성

```yaml
# compose.yaml — 3개 서비스
services:
  api:       # FastAPI, 포트 8010:8000
             # depends_on: db (healthy), redis (healthy)
             # healthcheck: python urllib → /health/live
  db:        # PostgreSQL 16, 포트 5440:5432
             # DB name: workspace_backend
  redis:     # Redis 7, 포트 6390:6379
```

capstone의 compose는 worker 서비스 없이 api + db + redis 3개로 구성된다.
drain이 API 프로세스 안에서 실행되므로 별도 worker가 필요 없다.

```bash
docker compose up --build -d
docker compose logs -f api     # 로그 확인
```

## Phase 8: 테스트

```python
# tests/conftest.py
#   app_env fixture:
#     - tmp_path에 SQLite DB
#     - SECRET_KEY, TOKEN_ISSUER monkeypatch
#     - get_settings.cache_clear() → configure_engine() → create_all()
#   app_client fixture:
#     - create_app() → TestClient

# tests/integration/test_capstone.py
#   test_local_auth_workspace_flow_and_google_member_notification:
#     1. owner 회원가입 → 이메일 인증 → 로그인
#     2. collaborator Google 로그인
#     3. workspace 생성 → invite → accept
#     4. WebSocket 연결 (access_token query param)
#     5. project → task → comment → drain → WS receive
#     6. /me 확인
```

하나의 통합 테스트가 7개 랩의 핵심 개념을 모두 관통한다.
이 테스트의 통과가 capstone의 가장 중요한 검증 포인트다.

```bash
pytest -q    # 통합 테스트 실행
```

## Phase 9: 검증

```bash
make install  # pip install -e ".[dev]"
make lint     # ruff check app tests
make test     # pytest
make smoke    # smoke test

# Compose 검증
docker compose up --build -d
curl http://localhost:8010/api/v1/health/live
curl http://localhost:8010/api/v1/health/ready

# 수동 통합 테스트
# 1. 회원가입
curl http://localhost:8010/api/v1/auth/register -X POST \
  -H "Content-Type: application/json" \
  -d '{"handle":"demo","email":"demo@example.com","password":"pass1234"}'

# 2. 로그인 (이메일 인증 후)
curl http://localhost:8010/api/v1/auth/login -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"pass1234"}' \
  -c cookies.txt

# 3. 워크스페이스 생성
curl http://localhost:8010/api/v1/platform/workspaces -X POST \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name":"Demo Workspace"}'

docker compose down
```

---

## 타임라인 요약

| 단계 | 핵심 산출물 |
|------|-------------|
| 초기화 | pyproject.toml (전체 의존성 통합) |
| core | config, security, logging, errors, rate_limit |
| 모델 | auth 4 테이블 + platform 7 테이블 = 11 테이블 |
| runtime | ConnectionManager, PresenceTracker |
| 서비스 | AuthService, PlatformService |
| API | auth 라우트, platform 라우트, health, WebSocket |
| Compose | api + postgres + redis (3 서비스) |
| 테스트 | 전체 흐름 통합 테스트 1개 |
| 검증 | lint, test, smoke, Compose curl |
