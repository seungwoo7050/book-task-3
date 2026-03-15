# workspace-backend-v2-msa Evidence Ledger

## 독립 Todo 판정
- 판정: `done`
- 이유: `problem/README.md`가 v1과 구분되는 별도 성공 기준을 갖고 있고, `tests/test_system.py`가 recovery까지 포함한 독립 capstone 시나리오를 고정한다.
- 이번 Todo에서도 기존 blog 본문은 입력 근거로 사용하지 않았다.

## 이번 턴에 읽은 근거
- `backend-fastapi/capstone/workspace-backend-v2-msa/problem/README.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/README.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/docs/README.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/docs/aws-deployment.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/README.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/Makefile`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/compose.yaml`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/contracts/README.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/main.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/runtime.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/core/logging.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/core/security.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/v1/routes/auth.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/v1/routes/platform.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/v1/routes/health.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/v1/routes/ops.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/identity-service/app/api/v1/routes/auth.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/identity-service/app/api/v1/routes/ops.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/api/v1/routes/platform.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/api/v1/routes/health.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/api/v1/routes/ops.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/domain/services/platform.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/db/models/platform.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/notification-service/app/api/v1/routes/notifications.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/notification-service/app/api/v1/routes/ops.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/notification-service/app/domain/services/notifications.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/services/notification-service/app/db/models/notifications.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/tests/compose_harness.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/tests/smoke.py`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py`

## 소스에서 확인한 핵심 사실
- public API shape는 gateway가 유지하고, 내부 auth는 `identity-service /internal/auth/*`, 내부 workspace는 `workspace-service /internal/*`, 내부 notification은 `notification-service /internal/notifications/*`로 분리된다.
- gateway는 쿠키, CSRF, `X-Request-ID`, WebSocket edge, Redis pub/sub relay thread를 가진다.
- gateway는 upstream 호출 때 `X-Request-ID`를 그대로 전달하고, JSON logging payload에 `service`, `request_id`를 포함한다.
- `workspace-service`는 identity DB를 읽지 않는다. membership에 `user_email`을 저장하고 claims의 `sub/email`을 이용해 invite accept와 membership guard를 처리한다.
- comment 생성은 `OutboxEvent(status="queued")`를 남기고, relay 단계에서 Redis Streams로 내보낸다.
- `notification-service`는 stream을 `xread({stream: "0-0"})`로 읽고 `ConsumerReceipt(event_id)`로 dedupe 한 뒤, `Notification(status="delivered")`를 저장하고 Redis pub/sub으로 fan-out 한다.
- `notification-service`는 stream을 `xread({stream: "0-0"}, count=100)`로 읽고 `ConsumerReceipt(event_id)`로 dedupe 한 뒤, `Notification(status="delivered")`를 저장하고 Redis pub/sub으로 fan-out 한다.
- gateway의 `notifications/drain`은 `relay`와 `consume`을 조합한 수동 recovery surface다.
- 따라서 recovery는 명시적이지만 backlog가 100건을 넘으면 drain 한 번으로 모두 비우지 못한다는 현재 배치 경계가 있다.
- gateway ready는 세 내부 서비스 ready + Redis ping을 함께 확인하고, 각 서비스는 `/ops/metrics`에 한 줄 카운터를 제공한다.
- `docs/aws-deployment.md`는 AWS target shape 문서일 뿐 실제 배포 성공을 주장하지 않는다.

## 검증 명령과 실제 결과

| 명령 | 결과 | 메모 |
| --- | --- | --- |
| `make lint` | 실패 | `/opt/homebrew/opt/python@3.14/bin/python3.14: No module named ruff` |
| `make test` | 실패 | `gateway/tests/conftest.py` import 단계에서 `ModuleNotFoundError: No module named 'fastapi'` |
| `make smoke` | 실패 | `tests/compose_harness.py` import 단계에서 `ModuleNotFoundError: No module named 'httpx'` |
| `python3 -m pytest tests/test_system.py -q` | 실패 | test collection 단계에서 `ModuleNotFoundError: No module named 'httpx'` |

## 이번 문서가 기대는 중심 앵커
- 브라우저 경계 앵커: `fastapi/gateway/app/api/v1/routes/auth.py`, `fastapi/gateway/app/main.py`
- 서비스 간 계약 앵커: `fastapi/gateway/app/runtime.py`, `fastapi/contracts/README.md`
- 이벤트 흐름 앵커: `fastapi/services/workspace-service/app/domain/services/platform.py`
- dedupe/recovery 앵커: `fastapi/services/notification-service/app/domain/services/notifications.py`
- end-to-end 증거 앵커: `fastapi/tests/test_system.py`

## 이번 턴의 품질 메모
- "MSA라서 더 좋다"는 서술을 피하고, v1 대비 늘어난 seam과 recovery 비용을 중심으로 다시 썼다.
- stale verification report 대신 이번 턴의 실제 CLI 실패 결과를 그대로 반영했다.
- AWS 문서는 target shape로만 취급하고, 검증 완료 주장과 분리했다.
