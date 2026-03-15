# workspace-backend-v2-msa 개발 타임라인

`workspace-backend-v2-msa`는 v1의 기능 목록을 나눠 담은 저장소가 아니다. 같은 협업형 도메인을 유지하면서, 단일 앱 시절엔 숨겨져 있던 브라우저 경계, DB ownership, event relay, 장애 복구를 어디서 비용으로 치르게 되는지를 보여 주는 비교판이다.

## 1. 출발점은 새 기능이 아니라 v1과의 비교 조건 유지였다

문제 정의와 README를 먼저 보면, v2는 v1을 버리는 프로젝트가 아니다. public `/api/v1/auth/*`, `/api/v1/platform/*` route shape를 계속 유지해야 한다고 못 박고 시작한다. 즉 "사용자에게 보이는 흐름은 최대한 그대로 두고, 내부 구조만 다시 푼다"가 첫 원칙이다.

이 선택 때문에 gateway가 가장 먼저 필요해진다. v1에서는 앱 하나가 쿠키도 들고 도메인도 들고 알림도 보냈지만, v2에선 그 브라우저 계약을 누가 계속 책임질지부터 정해야 했기 때문이다.

## 2. gateway는 reverse proxy가 아니라 브라우저 계약을 보존하는 adapter가 되었다

`fastapi/gateway/app/api/v1/routes/auth.py`를 보면 gateway는 register, verify-email, login, google-login, refresh, logout route를 계속 public path에 둔다. 하지만 실제 auth 작업은 모두 `identity-service /internal/auth/*`로 위임한다. gateway는 응답의 `access_token`, `refresh_token`, `csrf_token`을 받아 브라우저 쿠키에 다시 심고, CSRF 검사는 gateway에서만 수행한다.

이 구조가 중요해지는 이유는 내부 서비스가 브라우저 문맥을 몰라도 되기 때문이다. 내부 서비스는 cookie나 CSRF header를 해석하지 않고, bearer claims와 JSON payload만 읽는다. public API를 유지하면서도 내부 경계를 단순화하는 핵심 조치가 바로 여기 있다.

## 3. DB ownership을 지키려면 workspace-service는 identity DB를 보지 못한다

v1에서는 한 DB 안에서 membership과 user를 자연스럽게 연결할 수 있었다. 하지만 v2의 성공 기준은 각 서비스가 자기 DB만 읽어야 한다는 것이다. 그래서 `workspace-service`의 `Membership` 모델은 `user_id`뿐 아니라 `user_email`을 직접 들고 있고, invite accept도 identity DB join 없이 claims의 `email`과 invite의 `email`을 비교해 처리한다.

이건 사소한 구현 디테일이 아니라, 서비스 분리의 대가가 어디서 드러나는지 보여 주는 장면이다. 한 서비스가 다른 서비스의 테이블을 읽지 못하면, 이전에는 암묵적으로 얻던 정보도 claims나 event payload로 다시 옮겨야 한다.

## 4. comment write path는 이제 하나의 함수가 아니라 세 경계로 갈라진다

v2의 핵심 변화는 `create_comment()`가 더 이상 끝점이 아니라는 데 있다.

`workspace-service`의 `create_comment()`는 다음까지만 책임진다.
- membership 검증
- `Comment` row 저장
- 각 수신자별 `OutboxEvent(event_name="comment.created.v1")` 저장

그 다음 단계는 `relay_outbox()`에서 일어난다. 이 함수는 queued outbox를 읽어 Redis Streams에 `xadd()`로 밀어 넣고, outbox status를 `relayed`로 바꾼다. 그리고 마지막 단계는 `notification-service.consume()`이다. 여기서는 stream을 읽어 `Notification` row를 저장하고, `ConsumerReceipt(event_id)`를 남기고, Redis pub/sub으로 gateway에 fan-out 한다.

이 구조는 분산 시스템다운 seam을 보여 주지만, 동시에 학습용 단순화도 함께 노출한다. `consume()`은 consumer group이나 stream offset checkpoint 대신 `xread(..., "0-0", count=100)`으로 처음부터 다시 읽고, 중복 소비는 receipt 존재 여부로 걸러 낸다. 그래서 recovery는 "명시적으로 다시 밀어 넣고 다시 읽는다"는 점을 잘 보여 주지만, backlog가 길어지면 drain 한 번으로는 다 못 비우는 구조이기도 하다. 즉 v2는 완전한 운영용 consumer보다, 분산 이벤트 흐름을 읽을 수 있게 만드는 비교 모델에 가깝다.

## 5. gateway의 `notifications/drain`은 eventual consistency를 눈에 보이게 만든다

v2에서 가장 좋은 설계 선택 중 하나는 eventual consistency를 숨기지 않는다는 점이다. gateway의 `POST /api/v1/platform/notifications/drain`은 내부적으로 두 호출을 순서대로 묶는다.
1. `workspace-service /internal/events/relay`
2. `notification-service /internal/notifications/consume`

반환값도 `{relayed, processed}`로 나뉜다. 이건 "알림이 그냥 간다"는 착시를 없애 준다. 실제로는 write path, relay path, consume path가 서로 다른 서비스와 다른 장애 표면을 가진다는 사실을 public API 레벨에서도 보여 주기 때문이다.

## 6. 실시간과 운영성도 분산 구조에 맞춰 다시 설계된다

gateway `main.py`를 보면 request마다 `X-Request-ID`를 만들거나 이어받고, 이 값을 응답 헤더와 upstream 요청에 다시 실어 보낸다. JSON logging payload에도 `service`, `request_id`가 들어간다. 각 서비스는 `/api/v1/ops/metrics`에서 `app_requests_total{service="..."}` 한 줄 카운터를 내고, health readiness도 역할이 다르다.

- gateway ready: identity/workspace/notification의 `/health/ready`와 Redis ping을 함께 확인
- workspace ready: DB + Redis
- notification ready: DB + Redis
- identity ready: 자체 DB

이 차이는 K-lab에서 분리해 봤던 distributed ops를 capstone 안으로 다시 끌고 들어온 결과다.

## 7. system test는 성공 경로만이 아니라 recovery 경로까지 고정한다

`tests/test_system.py`는 v2가 왜 단순한 분해판이 아닌지를 가장 잘 보여 준다.
1. owner는 gateway를 통해 로컬 가입, 메일 인증, 로그인
2. collaborator는 gateway를 통해 Google 로그인
3. owner가 workspace, invite, project, task를 생성
4. 첫 comment 후 drain 성공, collaborator WebSocket 수신
5. `docker compose stop notification-service`
6. 두 번째 comment는 여전히 성공
7. drain은 503으로 실패
8. notification-service 재시작 후 ready 대기
9. recovery drain 성공
10. collaborator가 두 번째 댓글 알림을 다시 수신

이 시나리오는 "notification-service가 죽어도 comment 생성은 성공해야 한다"는 성공 기준을 코드로 그대로 박아 둔 것이다. v1에 없던 실패 경로가 이제는 주요 기능이 된다.

## 8. 이번 재실행은 설계보다 먼저 환경 공백을 드러냈다

이번 턴의 canonical verification 결과는 아래와 같았다.

```bash
make lint
# python3.14: No module named ruff

make test
# gateway/tests/conftest.py import 단계에서 ModuleNotFoundError: No module named 'fastapi'

make smoke
# tests/compose_harness.py import 단계에서 ModuleNotFoundError: No module named 'httpx'

python3 -m pytest tests/test_system.py -q
# ModuleNotFoundError: No module named 'httpx'
```

즉, 현재 호스트에서는 서비스 간 계약을 검증하기도 전에 Python 도구와 라이브러리부터 비어 있다. 이번 문서는 그래서 "실행이 성공했다"고 포장하지 않고, 소스 구조와 테스트 설계는 확인했지만 현재 환경의 canonical rerun은 dependency 단계에서 멈춘다고 적는다.

## 정리

`workspace-backend-v2-msa`의 가치는 서비스가 많아졌다는 데 있지 않다. public API를 보존한 채 브라우저 경계는 gateway로, 데이터 소유권은 각 서비스로, 알림 전달은 outbox/stream/receipt/pubsub으로 찢어 놓았을 때 어떤 복잡성과 어떤 recovery 책임이 생기는지를 직접 보여 주는 데 있다. 이 capstone은 v1보다 더 편안한 구조가 아니라, 더 비싼 구조를 왜 감수해야 하는지 설명해야 하는 비교판이다.
