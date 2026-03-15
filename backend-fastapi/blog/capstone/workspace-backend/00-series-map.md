# workspace-backend

이 글은 `backend-fastapi`의 A~G 랩을 "한 앱 안에 다 넣어 보기"로 끝내지 않고, 어떤 경계는 합치고 어떤 경계는 아직 수동으로 남겨 두는지가 왜 중요한지 추적한다. `workspace-backend`는 완성형 제품 설명서가 아니라, 이후 `workspace-backend-v2-msa`와 비교할 수 있는 단일 백엔드 기준선이다.

## 이 Todo가 붙잡는 질문
인증, 워크스페이스 인가, 프로젝트/태스크/댓글 쓰기 흐름, queued notification, WebSocket 전달을 한 프로세스 안에 다시 조합할 때 무엇이 단순해지고 무엇이 아직 남는가?

문제 정의는 기능 수를 늘리는 데 있지 않다. 실제 성공 기준도 "로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명되는가", "워크스페이스 멤버십이 프로젝트/태스크/댓글 API에 실제로 연결되는가", "알림 생성이 큐와 실시간 전달로 이어지는가"에 맞춰져 있다. 이 capstone은 그 질문을 한 번에 보여 주는 최소 통합선이다.

## 먼저 잡아둘 범위
- 인증 surface는 `register -> verify-email -> local login`과 `google/login` 두 갈래를 모두 같은 `User` 모델로 모은다.
- 플랫폼 surface는 `workspace -> invite -> project -> task -> comment` 생성 흐름에 집중한다.
- 알림은 댓글 생성 시 `Notification(status="queued")`를 쌓고, `POST /api/v1/platform/notifications/drain`이 그 큐를 WebSocket 연결로 밀어 넣는다.
- 실시간은 broker나 background worker가 아니라 `app.state.connection_manager`와 `PresenceTracker`로 유지된다.
- 운영 신호는 `/api/v1/health/live`, `/api/v1/health/ready`, Compose의 Postgres/Redis/API 세 서비스 정도로만 닫힌다.

이 말은 곧, 이 프로젝트가 "협업형 SaaS의 모든 기능"을 다루는 것은 아니라는 뜻이기도 하다. 실제 route surface를 보면 목록 조회, 수정, 삭제, 검색보다 쓰기 경로와 경계 연결부가 우선이다. `RateLimiter` 구현 파일은 존재하지만 auth/platform route에 실제로 연결되지는 않아, 보안 hardening까지 끝난 상태로 읽으면 과장된다.

## 이번 글에서 따라갈 순서
1. 왜 capstone v1이 랩 재사용보다 재조합 문제로 읽혀야 하는지 정리한다.
2. `auth.py`와 `platform.py`가 어떤 식으로 한 사용자 흐름을 한 앱 안에 봉합하는지 본다.
3. 통합 테스트가 owner와 collaborator를 어떻게 한 시나리오로 묶는지 따라간다.
4. `notifications/drain`, WebSocket, presence TTL이 어디까지는 실제 동작이고 어디부터는 다음 단계 과제인지 구분한다.
5. 실제 재실행 결과를 기준으로 현재 검증 상태와 한계를 닫는다.

## 가장 중요한 코드 신호
- `fastapi/app/domain/services/auth.py`
  로컬 인증, Google 로그인, refresh token family rotation을 같은 사용자 모델로 묶는다.
- `fastapi/app/domain/services/platform.py`
  workspace membership 검사, invite 수락, comment 생성, queued notification 생성과 drain을 한 서비스에 둔다.
- `fastapi/app/runtime.py`
  notification fan-out과 presence TTL이 외부 broker 없이 메모리 객체로 유지된다는 사실을 보여 준다.
- `fastapi/tests/integration/test_capstone.py`
  owner의 로컬 로그인과 collaborator의 Google 로그인이 하나의 협업 흐름으로 실제 연결되는지를 가장 잘 보여 준다.

## 이번 턴의 재검증 메모
- `make lint`: 통과
- `make test`: `ModuleNotFoundError: No module named 'app'`
- `make smoke`: `ModuleNotFoundError: No module named 'fastapi'`
- `python3 -m pytest tests/integration/test_capstone.py -q`: `ModuleNotFoundError: No module named 'fastapi'`

즉, 코드가 지향하는 기준선은 분명하지만 현재 호스트 검증 환경은 두 갈래로 어긋나 있다. `pytest` 진입점은 editable install 또는 `PYTHONPATH`가 잡히지 않은 상태에서 `app` import를 못 찾고, `python3` 진입점은 FastAPI 의존성이 없는 interpreter를 보고 있다. `fastapi/README.md`가 `.venv`와 `make install`을 먼저 요구하는 이유도 바로 여기 있다. 이 상태 자체가 지금의 사실이고, 본문도 그 전제를 숨기지 않는다.

## 다 읽고 나면 남는 것
- 왜 `workspace-backend`가 "단일 앱이라서 단순하다"가 아니라 "무엇을 일부러 아직 단순하게 남겼는가"의 기준선인지 설명할 수 있다.
- comment write path가 auth, membership, queue, websocket을 묶는 중심선이라는 점을 이해하게 된다.
- 다음 `workspace-backend-v2-msa`에서 복잡도가 어디서 생기는지 비교할 준비가 된다.
