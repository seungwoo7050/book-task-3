# 지식 인덱스

## 먼저 꺼내 볼 판단 규칙

- 외부 API 경로는 유지해야 하지만 내부 서비스 분해가 필요하다면 gateway를 먼저 의심한다.
- 서비스가 다른 서비스 DB를 읽고 싶어질 때는 “쿼리가 하나 더 필요하다”가 아니라 ownership 규칙이 무너지는 신호로 본다.
- 저장 성공과 전달 성공을 같은 트랜잭션으로 묶을 수 없다면 outbox를 고려한다.
- relay 재시도나 consumer 재기동 뒤에 중복 결과가 생길 수 있다면 idempotent consumer가 필요하다.
- tracing backend가 없어도 “이 503이 어느 내부 호출에서 왔는가”를 알아야 하면 request id를 먼저 남긴다.

## 개념별 판단 카드

### `gateway`

언제 쓰는가:
- public route shape를 유지한 채 내부 contract를 바꾸고 싶을 때
- 브라우저 쿠키, CSRF, access token cookie 같은 상태를 edge에 고정하고 싶을 때
- 내부 서비스 오류를 외부용 HTTP 응답으로 번역해야 할 때

언제 과한가:
- 클라이언트가 이미 내부 서비스 경로를 직접 알고 있고, public contract를 보존할 이유가 없을 때
- gateway가 1:1 forwarding만 하고 번역 책임이 거의 없을 때

이 레포의 근거:
- [../fastapi/gateway/app/api/v1/routes/auth.py](../fastapi/gateway/app/api/v1/routes/auth.py)
- [../fastapi/gateway/app/api/v1/routes/platform.py](../fastapi/gateway/app/api/v1/routes/platform.py)
- [../fastapi/gateway/app/main.py](../fastapi/gateway/app/main.py)

### `service DB ownership`

언제 쓰는가:
- “누가 어떤 테이블을 직접 읽고 쓰는가”를 서비스 경계의 첫 기준으로 삼고 싶을 때
- 서비스별 독립 변경, 독립 테스트, 책임 분리를 설명해야 할 때

실패 징후:
- 다른 서비스 DB를 직접 join하고 싶어진다.
- service boundary보다 shared model 재사용이 먼저 보인다.
- 인증 서비스가 내려가면 도메인 서비스의 단순 조회도 같이 막히게 설계된다.

이 레포의 근거:
- [../fastapi/services/workspace-service/app/db/models/platform.py](../fastapi/services/workspace-service/app/db/models/platform.py)
- [../fastapi/services/notification-service/app/db/models/notifications.py](../fastapi/services/notification-service/app/db/models/notifications.py)
- [../fastapi/services/notification-service/README.md](../fastapi/services/notification-service/README.md)

### `outbox`

언제 쓰는가:
- 댓글 저장은 성공해야 하지만, 이후 알림 전달은 나중에 회복 가능해도 될 때
- DB commit과 외부 브로커 publish를 같은 성공 사건으로 보지 않을 때

실패 징후:
- comment는 저장됐는데 알림이 유실됐는지 설명할 수 없다.
- relay 실패 시 재시도 기준이 없다.
- 이벤트를 브로커에 바로 쏘고 끝내서 “저장 성공”과 “전달 성공”을 구분할 수 없다.

이 레포의 근거:
- [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)
- [../fastapi/services/workspace-service/app/api/v1/routes/platform.py](../fastapi/services/workspace-service/app/api/v1/routes/platform.py)
- [../fastapi/services/workspace-service/app/db/models/platform.py](../fastapi/services/workspace-service/app/db/models/platform.py)

### `idempotent consumer`

언제 쓰는가:
- 같은 event를 두 번 읽을 가능성을 가정해야 할 때
- consumer 재기동, relay 재시도, stream replay 뒤에도 결과를 한 번만 남기고 싶을 때

실패 징후:
- notification-service를 다시 켜면 같은 알림이 여러 번 저장된다.
- event dedupe 기준이 없어서 replay를 겁낸다.

이 레포의 근거:
- [../fastapi/services/notification-service/app/domain/services/notifications.py](../fastapi/services/notification-service/app/domain/services/notifications.py)
- [../fastapi/services/notification-service/app/db/models/notifications.py](../fastapi/services/notification-service/app/db/models/notifications.py)

### `Redis Streams`와 `Redis pub/sub`

왜 둘 다 필요한가:
- Streams는 `workspace-service -> notification-service` 전달 기록과 재처리 가능성을 위해 필요하다.
- pub/sub는 `notification-service -> gateway`의 실시간 fan-out을 위해 필요하다.

잘못 쓰는 신호:
- Streams만으로 websocket fan-out까지 설명하려 하거나
- pub/sub만으로 durable event delivery까지 해결했다고 말할 때

이 레포의 근거:
- [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)
- [../fastapi/services/notification-service/app/domain/services/notifications.py](../fastapi/services/notification-service/app/domain/services/notifications.py)
- [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)

### `request id`

언제 먼저 넣는가:
- tracing backend가 없어도 gateway와 내부 서비스의 같은 요청을 연결해야 할 때
- upstream 503을 봤을 때 어느 hop에서 끊겼는지 로그 상관관계를 남기고 싶을 때

이 레포의 근거:
- [../fastapi/gateway/app/main.py](../fastapi/gateway/app/main.py)
- [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)
- [../fastapi/services/identity-service/app/main.py](../fastapi/services/identity-service/app/main.py)
- [../fastapi/services/workspace-service/app/main.py](../fastapi/services/workspace-service/app/main.py)
- [../fastapi/services/notification-service/app/main.py](../fastapi/services/notification-service/app/main.py)

## v2를 읽을 때 반복해서 보이는 실패 징후

| 징후 | 먼저 의심할 개념 | 왜 그런가 |
| --- | --- | --- |
| comment는 저장됐는데 알림이 안 갔다 | outbox, relay, consumer | 저장과 전달이 분리돼 있기 때문이다 |
| 알림이 두 번 온다 | idempotent consumer | replay를 한 번 더 처리했을 가능성이 있다 |
| gateway 503인데 어느 서비스 문제인지 모르겠다 | request id, upstream translation | edge 로그와 내부 서비스 로그를 묶을 식별자가 약하다 |
| 다른 서비스 DB를 직접 읽고 싶다 | DB ownership | event payload나 claim 계약이 얇거나 경계가 잘못 잘렸다 |
| websocket은 되는데 durable delivery 설명이 안 된다 | Streams vs pub/sub 구분 | 실시간 fan-out과 저장 가능한 전달은 다른 층위다 |

## 이 레포에서 개념을 가장 빨리 확인하는 순서

1. [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)로 전체 사용자 흐름을 본다.
2. [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)에서 comment 저장과 outbox relay를 본다.
3. [../fastapi/services/notification-service/app/domain/services/notifications.py](../fastapi/services/notification-service/app/domain/services/notifications.py)에서 consume, dedupe, pub/sub 발행을 본다.
4. [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)와 [../fastapi/gateway/app/main.py](../fastapi/gateway/app/main.py)에서 websocket fan-out과 request id 전파를 본다.

## 참고 자료

- 제목: `capstone/workspace-backend/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: v1 기준선의 범위와 비교 기준을 다시 정리하기 위해 읽었다.
  - 배운 점: v2는 새 제품이 아니라 같은 도메인의 다른 아키텍처 버전이어야 한다.
  - 반영 결과: problem framing과 approach log의 비교 기준에 반영했다.
- 제목: `capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: v2가 실제로 어떤 end-to-end 흐름을 검증하는지 기록하기 위해 확인했다.
  - 배운 점: owner local auth, collaborator social auth, invite, comment, outage recovery를 한 흐름으로 묶어야 v2의 설명력이 생긴다.
  - 반영 결과: development timeline과 retrospective에 반영했다.

## 다음에 더 보강할 질문

- event version을 `comment.created.v1`에서 바꿔야 할 때 어떤 migration 규칙을 둘 것인가
- request id만으로 부족해지는 시점은 언제이고, 그다음에 어떤 tracing backend가 필요한가
- gateway가 public contract 보존 이상의 책임을 계속 가져도 되는가, 아니면 BFF와 edge를 분리해야 하는가
