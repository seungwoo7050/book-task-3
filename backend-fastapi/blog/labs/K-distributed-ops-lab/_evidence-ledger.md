# K-distributed-ops-lab 근거 정리

## 1. 문제 정의와 범위

- `problem/README.md`
  - 모든 서비스의 `/health/live`, `/health/ready`, `/ops/metrics`, request id 로그 문맥, AWS target shape 문서 해석을 성공 기준으로 둔다.
  - 제외 범위를 실제 클라우드 배포 자동화, trace backend, log shipping으로 명시한다.
- `README.md`
  - 이 랩을 운영성 주제를 별도 학습 단위로 분리한 랩으로 소개한다.

## 2. 실제 compose 런타임

- `fastapi/compose.yaml`
  - `gateway`, `identity-service`, `workspace-service`, `notification-service`, `redis`를 함께 띄운다.
  - public entrypoint는 `8014`의 gateway다.
  - 내부 서비스 포트는 `8131`, `8132`, `8133`, Redis는 `6394`다.
- `fastapi/README.md`
  - 모든 서비스가 `health`/`metrics` surface를 갖는다는 해석을 명시한다.

## 3. health/readiness 의미 차이

- `fastapi/services/identity-service/app/api/v1/routes/health.py`
  - `/live`는 단순 ok.
  - `/ready`는 DB `SELECT 1`로 readiness를 판단한다.
- `fastapi/services/workspace-service/app/api/v1/routes/health.py`
  - `/ready`는 DB와 Redis `ping()`을 함께 본다.
- `fastapi/services/notification-service/app/api/v1/routes/health.py`
  - `/ready`는 DB와 Redis `ping()`을 함께 본다.
- `fastapi/gateway/app/api/v1/routes/health.py`
  - `/ready`는 내부 세 서비스의 `/health/ready`를 모두 호출하고, 필요 시 자체 Redis도 `ping()`한다.
  - gateway ready는 프로세스 자체가 아니라 upstream readiness 집계에 더 가깝다.

## 4. metrics surface

- `fastapi/gateway/app/api/v1/routes/ops.py`
  - `app_requests_total{service="gateway"}` 반환.
- `fastapi/services/identity-service/app/api/v1/routes/ops.py`
  - `app_requests_total{service="identity-service"}` 반환.
- `fastapi/services/workspace-service/app/api/v1/routes/ops.py`
  - `app_requests_total{service="workspace-service"}` 반환.
- `fastapi/services/notification-service/app/api/v1/routes/ops.py`
  - `app_requests_total{service="notification-service"}` 반환.
- 각 서비스 `app/main.py`
  - middleware에서 `app.state.metrics.increment()`를 호출한다.

## 5. JSON 로그와 request correlation

- `fastapi/gateway/app/core/logging.py`
- `fastapi/services/identity-service/app/core/logging.py`
- `fastapi/services/workspace-service/app/core/logging.py`
- `fastapi/services/notification-service/app/core/logging.py`
  - 모두 JSON formatter에 `service`, `request_id`, `timestamp`, `level`, `logger`, `message`를 포함한다.
- 각 서비스 `app/main.py`
  - 요청 헤더의 `X-Request-ID`를 읽거나 생성해 response header에 다시 넣는다.

## 6. 운영 signal을 다루는 테스트

- `fastapi/gateway/tests/integration/test_gateway_health.py`
  - `/api/v1/health/live`와 `/api/v1/ops/metrics`가 200인지 확인한다.
  - metrics 본문 값이나 `request_id` 로그 payload는 검증하지 않는다.
- `fastapi/services/notification-service/tests/integration/test_notification_service.py`
  - `/api/v1/health/live`와 `/api/v1/ops/metrics`가 200인지 확인한다.
  - notification-service 쪽도 관측 surface availability까지만 잠그고, counter 증가량이나 로그 JSON 필드까지는 보지 않는다.
- `fastapi/tests/test_system.py`
  - gateway를 통해 end-to-end 흐름과 notification-service 중지/복구 시나리오를 재현한다.
  - recovery 직전 `wait_for("http://127.0.0.1:8133/api/v1/health/ready")`를 호출하지만, metrics scrape나 log line parse는 하지 않는다.

## 7. AWS target shape 문서의 경계

- `docs/aws-deployment.md`
  - ALB, ECS Fargate, RDS PostgreSQL, ElastiCache for Redis, Secrets Manager 조합을 target shape로 제시한다.
  - 실제 AWS 계정 실행, IaC 존재, 비용/보안/성능 검증은 보장하지 않는다고 명시한다.

## 8. 이번 턴에서 다시 실행한 명령과 결과

- `cd fastapi && make lint`
  - 통과.
- `cd fastapi && make test`
  - gateway 테스트 import 단계에서 `ModuleNotFoundError: No module named 'argon2'`로 실패.
- `cd fastapi && make smoke`
  - 통과.
- `cd fastapi && python3 -m pytest tests/test_system.py -q`
  - 통과.

## 9. 문서에 반영한 핵심 판단

- 이 랩의 핵심은 운영 endpoint가 "있다"보다, 각각 무엇을 확인하는지 다르다는 점이다.
- request id와 JSON 로그는 tracing 대체물이 아니라 최소 correlation baseline으로 읽는 편이 정확하다.
- 자동 테스트가 직접 잠근 것은 ops surface availability와 recovery flow까지이고, observability payload semantics는 여전히 source-assisted conclusion이다.
- AWS 문서는 배치 가정 문서이지, 배포 완료 보고서가 아니다.
- 기능 흐름 자체보다 운영 signal 해석이 본문 중심이 되어야 한다.
