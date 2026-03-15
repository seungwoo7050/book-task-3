# H-service-boundary-lab 근거 정리

## 1. 문제 정의와 현재 범위

- `problem/README.md`
  - 목표를 `identity-service`와 `workspace-service` 분리, claims 기반 전달, cross-DB 금지로 제한한다.
  - 제외 범위를 event broker, edge gateway, websocket으로 명시한다.
- `README.md`
  - 이 랩을 "서비스를 어디서 나누고 무엇을 공유하지 말아야 하는지 배우는 MSA 입문 랩"으로 소개한다.

## 2. 실제 compose 런타임

- `fastapi/compose.yaml`
  - `identity-service`와 `workspace-service` 두 컨테이너만 정의한다.
  - 각 서비스에 별도 DB URL 환경 변수와 별도 volume을 준다.
  - gateway, notification-service는 compose에 포함되지 않는다.
- `fastapi/README.md`
  - 빠른 실행 경로를 `docker compose up --build`로 제시하고, 노출 포트를 `8111`, `8011`로 고정한다.

## 3. identity-service가 발급하는 계약

- `fastapi/services/identity-service/app/api/v1/routes/auth.py`
  - register, verify-email, login, google-login, refresh, revoke, debug mailbox latest를 제공한다.
- `fastapi/services/identity-service/app/domain/services/auth.py`
  - login 후 session bundle을 발급하고 refresh rotation/reuse detection 흐름을 유지한다.
- `fastapi/services/workspace-service/app/core/security.py`
  - access token payload에 `sub`, `handle`, `email`, `display_name`, `type`, `iss`, `iat`, `exp`를 넣는다.

## 4. workspace-service가 claims만으로 유지하는 경계

- `fastapi/services/workspace-service/app/api/deps.py`
  - `Authorization: Bearer ...`를 받아 서비스 내부에서 직접 토큰을 decode한다.
  - identity-service에 사용자 조회를 다시 요청하지 않는다.
- `fastapi/services/workspace-service/app/api/v1/routes/platform.py`
  - workspace, invite, project, task, comment, relay, outbox debug endpoint를 내부 API로 노출한다.
- `fastapi/services/workspace-service/app/domain/services/platform.py`
  - workspace 생성 시 owner membership을 즉시 생성한다.
  - invite 수락은 claims email과 invite email 일치를 강제한다.
  - project, task, comment 생성 전에 membership을 확인한다.
  - comment 저장 후 actor를 제외한 멤버별 `OutboxEvent`를 `queued`로 적재한다.

## 5. 현재 범위를 넘어 보이는 seam

- `fastapi/contracts/README.md`
  - public API를 gateway 기준 `/api/v1/auth/*`, `/api/v1/platform/*`로 적어 둔다.
  - internal notification contract와 `comment.created.v1` event contract까지 문서화한다.
- `fastapi/gateway/app/api/v1/routes/auth.py`
  - public auth surface를 identity-service 내부 API에 프록시한다.
- `fastapi/gateway/app/api/v1/routes/platform.py`
  - workspace 도메인 호출뿐 아니라 notifications drain, presence heartbeat, websocket surface까지 포함한다.
- `fastapi/services/notification-service/app/domain/services/notifications.py`
  - Redis Stream을 읽고 notification row와 consumer receipt를 기록한다.

정리하면, repo 안에는 H 랩의 범위를 넘어서는 scaffold가 있다. 하지만 top-level compose와 smoke/system 검증은 이 전체를 올리지 않는다. 그래서 문서에서는 이를 "현재 핵심 구현"이 아니라 "이미 들어온 다음 seam"으로 다뤘다.

## 6. 테스트와 재실행 명령

- `fastapi/services/identity-service/tests/integration/test_identity_service.py`
  - register -> verify -> login -> refresh 흐름을 확인한다.
- `fastapi/services/workspace-service/tests/integration/test_workspace_service.py`
  - workspace 생성, invite/accept, project/task/comment 생성, outbox pending 1건을 확인한다.
  - 즉 workspace 도메인 내부의 deeper 흐름은 이 테스트가 가장 직접적으로 잠근다.
- `fastapi/tests/test_system.py`
  - identity-service에서 발급한 access token으로 workspace-service의 workspace 생성까지 end-to-end로 확인한다.
  - invite, project, task, comment, outbox까지 top-level에서 모두 잠그지는 않는다.
- `fastapi/tests/smoke.py`
  - compose stack을 띄우고 `/health/live`, `/health/ready`가 열릴 때까지 기다린다.

## 7. 이번 턴에서 다시 실행한 명령과 결과

- `cd fastapi && make lint`
  - 통과.
- `cd fastapi && make test`
  - `services/identity-service` 테스트 진입 시 `ModuleNotFoundError: No module named 'argon2'`로 실패.
- `cd fastapi && make smoke`
  - 통과.
- `cd fastapi && python3 -m pytest tests/test_system.py -q`
  - 최종 통과.
  - 첫 재실행은 `Bind for 0.0.0.0:8011 failed: port is already allocated`로 실패했고, 남아 있던 compose 스택 정리 후 재실행에서 통과.

## 8. 문서에 반영한 핵심 판단

- 이 랩의 현재 답은 "DB ownership + claims contract"까지다.
- top-level system proof는 first workspace creation까지이고, workspace 내부 협업 흐름은 service-local integration test가 맡는다.
- outbox, Redis relay, gateway, notification-service는 이미 보이지만 top-level 검증 범위 밖에 있다.
- 따라서 본문은 서비스 분리 입문 랩의 중심 질문을 유지하되, 다음 단계 seam이 소스 안에 들어와 있다는 사실만 과장 없이 연결한다.
