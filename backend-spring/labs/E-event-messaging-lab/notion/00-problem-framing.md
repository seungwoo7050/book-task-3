# Problem Framing — request-response를 넘어서는 첫 걸음

## 이 랩이 존재하는 이유

백엔드 서비스가 HTTP 요청을 받고 응답을 반환하는 것만으로 충분한 시점은 어디까지인가. 주문이 접수되었을 때 결제 서비스에 알려야 하고, 재고를 차감해야 하고, 이메일을 보내야 한다면 — 이 모든 것을 한 번의 요청 안에서 동기적으로 처리할 것인가?

E-event-messaging-lab은 이 질문에서 출발한다. 마이크로서비스 아키텍처로 바로 뛰어가는 대신, 단일 서비스 안에서 "이벤트를 어떻게 안전하게 발행할 것인가"라는 문제를 먼저 다룬다. outbox 테이블에 이벤트를 기록하고, PENDING → PUBLISHED 상태 전환을 통해 발행 흐름을 시연한다. Kafka(Redpanda) 브로커는 Compose 스택에 포함되어 있지만, 현재 단계에서는 실제 토픽 발행보다 "메시지 발행의 경계를 어디에 둘 것인가"에 집중한다.

## 구체적으로 무엇을 다루는가

**Outbox 패턴**. 주문 이벤트를 생성할 때, 이벤트를 `outbox_events` 테이블에 PENDING 상태로 저장한다. 이 저장은 비즈니스 트랜잭션과 같은 DB 트랜잭션 안에서 일어난다. 이렇게 하면 "비즈니스 로직은 성공했는데 메시지 발행은 실패했다"는 불일치가 일어나지 않는다.

**상태 전환 시연**. `POST /api/v1/outbox-events/publish`를 호출하면, PENDING 상태의 outbox row들을 조회해서 PUBLISHED로 전환한다. 현재 구현에서 이 "발행"은 상태를 바꾸는 것뿐이지, 실제로 Kafka 토픽에 메시지를 보내지는 않는다. 이 간극이 중요한 학습 포인트다.

**이벤트 목록 조회**. `GET /api/v1/outbox-events`로 저장된 모든 이벤트를 확인한다. aggregate type, aggregate ID, event type, status가 포함된 응답을 통해 outbox가 어떤 정보를 담고 있는지 볼 수 있다.

## 의도적으로 다루지 않는 것들

- **Long-running publisher**: PENDING 상태의 이벤트를 주기적으로 Kafka에 발행하는 스케줄러가 없다. 현재는 수동으로 `/publish` 엔드포인트를 호출하는 방식이다.
- **실제 Kafka consumer**: Redpanda가 Compose에 있지만, 토픽에서 메시지를 소비하는 consumer 코드가 없다. "발행했다"는 것이 outbox 상태 변경으로만 표현된다.
- **DLQ(Dead Letter Queue)와 재시도 정책**: 발행 실패 시 재시도하거나, 재시도 불가능한 메시지를 DLQ로 보내는 로직이 없다. 이것은 개념 수준으로만 인지하고 있다.
- **중복 처리(Idempotency)**: 같은 이벤트가 두 번 발행되거나 소비되었을 때의 처리 전략이 아직 없다.

## 기술 스택과 제약 조건

| 항목 | 선택 |
|------|------|
| 언어 | Java 21 |
| 프레임워크 | Spring Boot 3.4.x |
| 메시지 브로커 | Redpanda v24.3.8 (Kafka 호환) |
| DB | PostgreSQL 16 (Docker), H2 (로컬) |
| ORM | Spring Data JPA |
| 스키마 관리 | Flyway |
| 메시징 라이브러리 | Spring Kafka (의존성 포함, 미사용) |

## 성공 기준

1. outbox 테이블에 이벤트가 PENDING 상태로 저장되어야 한다
2. publish 호출 시 PENDING → PUBLISHED 상태 전환이 일어나야 한다
3. 이벤트 목록 조회에서 aggregate type, event type, status가 확인 가능해야 한다
4. `make test`와 `make smoke`가 통과해야 한다
5. 현재 구현이 실제 Kafka 발행과 어떻게 다른지 문서에 명시되어 있어야 한다

## 남아 있는 불확실성

scaffold만으로 메시지 신뢰성을 충분히 체감할 수 있는지는 의문이다. outbox에 행을 저장하는 것은 DB 트랜잭션의 일부이므로 신뢰할 수 있지만, 거기서 Kafka까지의 거리를 실제로 경험하려면 scheduled publisher와 consumer가 필요하다. 그래도 outbox boundary를 먼저 이해하는 것이 순서상 맞다고 판단했다.

