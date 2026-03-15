# workspace-backend-v2-msa

이 글은 `workspace-backend` v1의 협업형 도메인을 더 "고급스럽게" 만드는 이야기가 아니다. 같은 public `/api/v1/auth/*`, `/api/v1/platform/*` 흐름을 유지한 채, 내부를 `gateway + identity-service + workspace-service + notification-service`로 다시 풀었을 때 어떤 복잡성이 새로 생기고 무엇을 추가로 증명해야 하는지를 따라간다.

## 이 Todo가 붙잡는 질문
public API는 그대로 두고 내부 서비스만 나누면 정말 더 좋아지는가, 아니면 브라우저 경계, DB ownership, event relay, recovery test 같은 새로운 부담을 함께 떠안게 되는가?

문제 정의는 이미 답을 정해 놓고 시작하지 않는다. 성공 기준도 "gateway가 public route shape를 유지하는가", "각 서비스가 자기 DB만 읽는가", "comment가 outbox -> stream consumer -> websocket fan-out으로 이어지는가", "notification-service 장애 중에도 comment 생성이 성공하고 복구 후 전달되는가"에 맞춰져 있다. 즉 v2의 핵심은 분해 그 자체가 아니라, 분해 뒤에 늘어난 비용을 설명 가능한 상태로 남기는 데 있다.

## 먼저 잡아둘 범위
- `gateway`
  브라우저 쿠키, CSRF, `X-Request-ID`, public route shape, WebSocket edge를 가진다.
- `identity-service`
  register, verify-email, login, google-login, refresh, revoke를 내부 `/internal/auth/*` surface로 소유한다.
- `workspace-service`
  workspace, invite, project, task, comment를 소유하고, comment 시 `OutboxEvent(event_name="comment.created.v1")`를 기록한다.
- `notification-service`
  Redis Streams를 읽어 `Notification` row를 쓰고, `ConsumerReceipt`로 중복 소비를 막은 뒤 Redis pub/sub으로 gateway에 fan-out 한다.
- `gateway`의 `notifications/drain`
  내부적으로 `workspace-service /internal/events/relay`와 `notification-service /internal/notifications/consume`을 순서대로 호출한다.

이 구조는 v1보다 "자동화가 많다"기보다 "수동 seam이 더 명시적이다"에 가깝다. drain은 여전히 수동 trigger이고, `notification-service.consume()`도 consumer group 대신 `xread(..., "0-0", count=100)`으로 stream 처음부터 읽은 뒤 receipt로 dedupe 한다. 즉 recovery는 내장돼 있지만 한 번의 drain으로 무한 backlog를 다 비우는 구조는 아니다. 학습용 MSA로는 충분하지만, production-grade delivery 파이프라인으로 읽으면 과장된다.

## 이번 글에서 따라갈 순서
1. 왜 v1 기준선에서 gateway를 따로 세워야 했는지 정리한다.
2. 쿠키/CSRF는 gateway에만 두고 내부는 bearer claims만 읽는 구조를 본다.
3. workspace-service가 왜 user 정보를 DB join 대신 claims와 event payload로 들고 다녀야 하는지 본다.
4. outbox -> Redis Streams -> receipt dedupe -> pub/sub -> WebSocket fan-out 흐름을 따라간다.
5. system test가 notification-service 장애 복구를 어떻게 공용 API 시나리오로 증명하는지 본다.
6. 현재 호스트 재검증 결과가 어디서 막히는지 사실대로 닫는다.

## 가장 중요한 코드 신호
- `fastapi/gateway/app/main.py`
  request id middleware, metrics counter, RedisNotificationRelay thread, WebSocket edge를 묶는다.
- `fastapi/gateway/app/runtime.py`
  upstream 요청 전파와 `X-Request-ID` 전달, pub/sub 메시지 수신 후 WebSocket dispatch를 맡는다.
- `fastapi/services/workspace-service/app/domain/services/platform.py`
  comment write path에서 outbox event를 기록하고 relay 시 stream으로 내보낸다.
- `fastapi/services/notification-service/app/domain/services/notifications.py`
  stream consume, `ConsumerReceipt` dedupe, pub/sub 발행을 담당한다.
- `fastapi/tests/test_system.py`
  notification-service 중단과 복구를 포함한 전체 협업 시나리오를 고정한다.

## 이번 턴의 재검증 메모
- `make lint`: `/opt/homebrew/opt/python@3.14/bin/python3.14: No module named ruff`
- `make test`: gateway test import 단계에서 `ModuleNotFoundError: No module named 'fastapi'`
- `make smoke`: `tests/compose_harness.py` import 단계에서 `ModuleNotFoundError: No module named 'httpx'`
- `python3 -m pytest tests/test_system.py -q`: `ModuleNotFoundError: No module named 'httpx'`

즉, 이번 호스트에서는 분산 시스템의 동작 이전에 Python toolchain 자체가 비어 있는 상태다. 문서도 이 사실을 숨기지 않고, "설계는 소스에서 확인했고 canonical verification은 재실행했지만 현재 interpreter에는 필요한 모듈이 없다"는 현재형 사실 위에 서 있다.

## 다 읽고 나면 남는 것
- 왜 v2가 단순한 "서비스 분리판"이 아니라 브라우저 경계, DB ownership, event recovery까지 함께 떠안는 비교판인지 설명할 수 있다.
- `comment.created.v1` 한 이벤트가 gateway, workspace-service, notification-service를 어떻게 가로지르는지 이해하게 된다.
- v1의 단순함을 어디서 잃었는지, 그리고 그 대가로 무엇을 얻었는지 비교할 준비가 된다.
