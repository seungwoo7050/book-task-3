# workspace-backend Evidence Ledger

## 독립 Todo 판정
- 판정: `done`
- 이유: `problem/README.md`가 별도 성공 기준과 제외 범위를 가진 독립 capstone으로 정의하고, `fastapi/tests/integration/test_capstone.py`가 이 프로젝트만의 통합 시나리오를 고정한다.
- 이번 Todo에서 기존 blog 본문은 입력 근거로 사용하지 않았다.

## 이번 턴에 읽은 근거
- `backend-fastapi/capstone/workspace-backend/problem/README.md`
- `backend-fastapi/capstone/workspace-backend/README.md`
- `backend-fastapi/capstone/workspace-backend/docs/README.md`
- `backend-fastapi/capstone/workspace-backend/fastapi/README.md`
- `backend-fastapi/capstone/workspace-backend/fastapi/Makefile`
- `backend-fastapi/capstone/workspace-backend/fastapi/compose.yaml`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/main.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/bootstrap.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/api/deps.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/api/v1/router.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/api/v1/routes/auth.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/api/v1/routes/health.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/core/config.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/core/logging.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/core/rate_limit.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/core/security.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/domain/services/auth.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/domain/services/platform.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/repositories/auth_repository.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/repositories/platform_repository.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/runtime.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/db/models/auth.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/db/models/platform.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/schemas/platform.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/tests/conftest.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/tests/integration/test_capstone.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/tests/smoke.py`

## 소스에서 확인한 핵심 사실
- capstone v1의 runtime topology는 단일 API + Postgres + Redis 조합이다.
- 앱 시작 시 `initialize_schema()`로 `Base.metadata.create_all()`을 수행해 로컬 반복 실행을 우선한다.
- 인증은 local register/login과 Google login을 같은 `User` 모델로 모으고, 둘 다 access/refresh/CSRF 규약으로 닫힌다.
- refresh token은 family 단위 rotation과 revoke를 구현하지만, 통합 테스트의 중심은 refresh보다 협업 시나리오다.
- 플랫폼 surface는 쓰기 경로 중심이다: workspace 생성, invite, invite accept, project 생성, task 생성, comment 생성, drain, presence, notification websocket.
- comment 생성은 다른 workspace 멤버에게 `Notification(status="queued")`를 만들고, `notifications/drain`이 그 row를 WebSocket payload로 fan-out 한 뒤 `sent`로 바꾼다.
- WebSocket 연결과 presence는 `app.state.connection_manager`, `PresenceTracker`에 메모리로 유지된다.
- `RateLimiter` 구현은 존재하지만 auth/platform route에 실제로 연결돼 있지 않다.
- health surface는 `/live`와 `/ready`만 있고, readiness는 DB `SELECT 1`과 optional Redis `ping()` 수준이다.
- logging formatter는 JSON이지만 request_id나 service correlation은 없다.
- `fastapi/README.md`의 canonical bootstrap은 `.venv` 생성과 `make install`을 먼저 요구한다.

## 검증 명령과 실제 결과

| 명령 | 결과 | 메모 |
| --- | --- | --- |
| `make lint` | 통과 | `ruff check app tests` -> `All checks passed!` |
| `make test` | 실패 | `tests/conftest.py` import 단계에서 `ModuleNotFoundError: No module named 'app'` |
| `make smoke` | 실패 | `python3 -m tests.smoke` 실행 시 `ModuleNotFoundError: No module named 'fastapi'` |
| `python3 -m pytest tests/integration/test_capstone.py -q` | 실패 | `conftest.py` import 단계에서 `ModuleNotFoundError: No module named 'fastapi'` |
| `PYTHONPATH=. pytest tests/integration/test_capstone.py -q` | 실패 | 셸에서 `pytest` command not found |
| `PYTHONPATH=. pytest -q` | 실패 | 셸에서 `pytest` command not found |
| `PYTHONPATH=. python -m tests.smoke` | 실패 | 셸에서 `python` command not found |

## 이번 문서가 기대는 중심 앵커
- 인증 조합 앵커: `fastapi/app/domain/services/auth.py`
- 협업 경계 앵커: `fastapi/app/domain/services/platform.py`
- 실시간/Presence 앵커: `fastapi/app/runtime.py`
- 통합 시나리오 앵커: `fastapi/tests/integration/test_capstone.py`
- 현재 검증 상태 앵커: 이번 턴 CLI 재실행 출력

## 이번 턴의 품질 메모
- README 확장판처럼 보이지 않게, route 목록보다 "owner와 collaborator가 어떻게 한 시나리오로 묶이는가"를 중심축으로 재서술했다.
- "단일 앱이라 다 해결했다"는 식의 과장을 피하기 위해 drain 수동 호출, 메모리 WebSocket, 미연결 rate limit, 최소 health surface를 한계로 명시했다.
- bare `make test/smoke` 실패를 곧바로 앱 결함으로 몰지 않고, README가 요구하는 bootstrap 절차와 현재 interpreter 상태를 분리해 적었다.
