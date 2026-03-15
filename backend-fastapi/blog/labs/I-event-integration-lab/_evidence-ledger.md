# I-event-integration-lab 근거 정리

## 1. 문제 정의와 범위

- `problem/README.md`
  - 목표를 outbox 기록, relay 뒤 consumer consume, 중복 consume 방지로 한정한다.
  - 제외 범위를 consumer group, dead-letter queue, replay UI로 명시한다.
- `README.md`
  - 이 랩을 `workspace-service` outbox와 `notification-service` idempotent consumer를 붙이는 단계로 소개한다.

## 2. 실제 compose 런타임

- `fastapi/compose.yaml`
  - `workspace-service`, `notification-service`, `redis` 세 컨테이너를 정의한다.
  - `workspace-service`는 `8012`, `notification-service`는 `8112`, `redis`는 `6392`를 사용한다.
  - 이 랩의 compose에는 `identity-service`가 없다.
- `fastapi/README.md`
  - 실행 진입점을 `docker compose up --build`로 고정한다.

## 3. workspace-service가 만드는 outbox

- `fastapi/services/workspace-service/app/domain/services/platform.py`
  - `create_comment()`는 comment 저장 후 멤버별 `OutboxEvent(event_name="comment.created.v1", status="queued")`를 적재한다.
  - payload에는 `message`, `recipient_user_id`, `workspace_id`, `task_id`가 들어간다.
  - `relay_outbox()`는 pending outbox를 Redis Stream에 `xadd()`하고 status를 `relayed`로 바꾼다.
- `fastapi/services/workspace-service/app/api/v1/routes/platform.py`
  - `/internal/tasks/{task_id}/comments`, `/internal/events/relay`, `/internal/debug/outbox/pending` 경로를 제공한다.
- `fastapi/services/workspace-service/app/api/deps.py`
  - auth 서비스 호출 없이 Bearer 토큰을 직접 decode한다.

## 4. notification-service가 하는 dedupe

- `fastapi/services/notification-service/app/domain/services/notifications.py`
  - `xread({stream_name: "0-0"}, count=100)`으로 stream을 읽는다.
  - 매 메시지마다 `event_id` 기준으로 `has_receipt()`를 먼저 확인한다.
  - receipt가 없을 때만 notification row와 `ConsumerReceipt`를 함께 저장한다.
  - 저장 후 pub/sub 채널로 메시지를 publish한다.
- `fastapi/services/notification-service/app/repositories/notifications_repository.py`
  - `ConsumerReceipt.event_id` 존재 여부를 기준으로 dedupe를 판단한다.
- `fastapi/services/notification-service/app/db/models/notifications.py`
  - `ConsumerReceipt.event_id`가 unique로 고정돼 있다.
- `fastapi/services/notification-service/app/api/v1/routes/notifications.py`
  - `/internal/notifications/consume`, `/internal/notifications/users/{user_id}` 경로를 제공한다.

## 5. 계약과 테스트가 보여 주는 의도

- `fastapi/contracts/README.md`
  - `comment.created.v1` source/sink를 `workspace-service -> notification-service`, transport를 Redis Streams로 명시한다.
- `fastapi/tests/test_system.py`
  - JWT를 테스트 안에서 직접 서명한다.
  - 관심사를 auth가 아니라 event handoff와 dedupe에 고정한다.
  - 첫 consume는 `processed == 1`, 두 번째 consume는 `processed == 0`, 저장 알림은 1건이라는 성공 기준을 직접 검증한다.
- `fastapi/tests/smoke.py`
  - compose stack을 띄우고 health가 열릴 때까지만 기다린다.
- `fastapi/services/workspace-service/tests/integration/test_workspace_service.py`
  - comment 생성 뒤 pending outbox가 1건인지 확인한다.

## 6. 이번 턴에서 다시 실행한 명령과 결과

- `cd fastapi && make lint`
  - 통과.
- `cd fastapi && make test`
  - `services/workspace-service` 테스트 collection 단계에서 `ModuleNotFoundError: No module named 'argon2'`로 실패.
- `cd fastapi && make smoke`
  - 통과.
- `cd fastapi && python3 -m pytest tests/test_system.py -q`
  - 통과.

## 7. 문서에 반영한 핵심 판단

- 이 랩의 핵심은 auth 재검증이 아니라 event handoff와 idempotent consumer다.
- `xread("0-0")` 때문에 같은 stream 엔트리를 다시 읽을 수 있다는 점을 숨기면 안 된다.
- 다만 현재 `count=100` 단일 batch 구현과 system test는 backlog 전체 drain이 아니라 1건 dedupe 흐름까지만 직접 잠근다.
- 대신 중복 흡수는 `ConsumerReceipt(event_id)`가 맡는다는 사실을 중심에 둬야 한다.
- `relayed`는 notification 저장 완료가 아니라 workspace-service 입장에서 stream handoff 완료에 더 가깝다.
