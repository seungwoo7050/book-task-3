# Knowledge Index — 이 캡스톤에서 꺼내 쓸 수 있는 다섯 가지 개념

## Refresh Token Hashing

refresh token 원문 대신 hash를 DB에 저장하여, 토큰이 탈취되더라도 직접 재사용을 어렵게 만드는 방식이다. `auth` 모듈의 `RefreshTokenEntity`, `HashingSupport`, `AuthService.refresh`에서 이 패턴이 나타난다.

이 방식의 핵심은 **서버가 토큰의 유효성을 판단할 수 있다**는 것이다. self-contained JWT만으로 refresh를 처리하면 "이 토큰을 폐기했는가?"를 서버가 알 수 없다. DB에 hash를 저장하면 rotation 시 이전 hash를 삭제하거나 무효화할 수 있고, 동시에 원문이 DB에 노출되지 않는다. 면접에서 "왜 refresh token을 DB에 저장하나?"라는 질문에 "회전, 폐기, 재사용 감지를 위해"라고 답하고, "왜 원문이 아닌 hash인가?"에 "DB 유출 시에도 토큰 재사용을 방지하기 위해"라고 답할 수 있다.

다른 Spring 인증 프로젝트나 FastAPI auth 설계에서도 그대로 재사용 가능한 패턴이다.

## Optimistic Locking for Inventory

같은 상품 재고를 동시에 수정할 때 `@Version` 충돌로 stale write를 막는 방식이다. `ProductEntity.version` 필드와 `OrderService.checkout`에서 이 패턴이 나타난다.

checkout 시점에 장바구니의 각 상품에 대해 DB에서 현재 stock을 읽고 차감한다. 이때 다른 트랜잭션이 같은 상품을 먼저 차감했다면 version이 달라지고, JPA가 `OptimisticLockException`을 던진다. 결제 시점이 아니라 **checkout 시점에 재고를 예약**하는 이유는 결제 지연 동안 oversell이 발생하는 것을 방지하기 위해서이다.

```java
@Version
private Long version;
```

재고, 좌석 예약, 쿠폰 발급처럼 경쟁이 있는 모든 write path에서 동일한 패턴을 적용할 수 있다.

## Idempotency Key

같은 결제 요청이 중복 도착해도 한 번만 반영되도록 요청 식별자를 저장하는 방식이다. `/api/v1/payments/mock/confirm` 엔드포인트에서 `Idempotency-Key` 헤더를 강제하고, `payments` 테이블에 `idempotency_key`를 UNIQUE 제약으로 저장한다.

이 패턴의 효과는 **네트워크 재시도에 안전**하다는 것이다. 클라이언트가 타임아웃 후 같은 요청을 다시 보내도 서버는 이미 처리된 결과를 반환한다. 외부 PG 연동이 없는 mock 환경에서도 이 계약을 지키면, 실제 PG를 연결할 때 같은 구조를 그대로 쓸 수 있다.

결제 외에도 webhook 처리, 외부 API callback 수신에서 동일한 패턴이 필요하다.

## Outbox Pattern

DB 변경과 메시지 발행 사이의 불일치를 줄이기 위해, 이벤트를 먼저 DB에 적재하고 별도 publisher가 내보내는 방식이다. `PaymentService`가 결제 확인 트랜잭션 안에서 `outbox_events` 테이블에 `order-paid` 이벤트를 삽입하고, `OutboxPublisher`가 미발행 이벤트를 polling하여 Kafka로 전송한다.

이 패턴이 해결하는 문제는 **DB 커밋 성공 + 메시지 전송 실패** 시나리오이다. 만약 `PaymentService`가 트랜잭션 안에서 Kafka에 직접 publish하면, DB는 커밋됐는데 Kafka 전송이 실패할 수 있다. outbox 테이블에 먼저 저장하면 이벤트가 DB 트랜잭션과 함께 보장되고, publisher가 나중에 전송하므로 최소한 한 번은 전달된다(at-least-once).

```
결제 확인 트랜잭션
  ├─ payments INSERT
  ├─ order status UPDATE (PENDING_PAYMENT → PAID)
  └─ outbox_events INSERT (order-paid)

별도 publisher (polling)
  └─ outbox_events → Kafka topic
```

이 캡스톤에서는 polling 방식을 사용했지만, Debezium 같은 CDC 기반으로 교체하면 polling 지연을 줄일 수 있다. 주문 완료, 이메일 발송, 알림 발행, 감사 로그 전달 등에서 동일한 구조를 재사용할 수 있다.

## Selective Redis Usage

모든 상태를 Redis로 옮기지 않고, **짧은 TTL이나 빠른 변경이 필요한 상태에만** 제한적으로 쓰는 판단이다. 이 캡스톤에서 Redis는 cart 저장소와 auth attempt limiter에만 사용한다.

장바구니는 DB에 넣기엔 일시적이고, 서버 메모리에 넣기엔 재시작 시 사라진다. Redis에 JSON으로 저장하면 이 중간 영역을 해결한다. 반면 상품이나 주문 같은 핵심 데이터는 PostgreSQL에 그대로 둔다. "왜 상품 캐시에 Redis를 안 썼나?"에 대해 "캐시 무효화 전략의 구현/설명 비용이 포트폴리오 범위를 넘겼다"라고 답할 수 있다.

`CartStore` 인터페이스 뒤에 `RedisCartStore`와 `InMemoryCartStore`를 두어, Docker 환경에서는 Redis를, 테스트에서는 인메모리를 사용한다. 캐시, rate limiting, ephemeral session-like state에서 같은 판단 기준을 적용할 수 있다.

---

## 용어 정리

| 용어 | 정의 |
|------|------|
| modular monolith | 하나의 배포 단위지만 코드 내부 모듈 경계를 명확히 두는 구조 |
| persisted flow | 요청 처리 결과가 메모리 데모가 아니라 DB나 외부 저장소에 남는 실제 데이터 흐름 |
| compensation | 이미 반영한 작업을 되돌리기 위한 별도 보상 동작. 이 캡스톤에서는 reservation release가 가장 가까운 예 |
| dedup key | 같은 이벤트를 여러 번 처리하지 않기 위해 저장하는 중복 제거 식별자 |
| at-least-once | 메시지가 최소 한 번은 전달됨을 보장하되, 중복 전달 가능성이 있는 전달 보증 수준 |

## 참고 자료

- `spring/README.md` — 공개 README의 구현 범위와 known tradeoff를 Notion 문서 톤과 맞추기 위해 참고
- `docs/verification.md` — 검증 명령(`make test` 등)의 실행 전제 조건(Docker 필요)을 확인하기 위해 참고
- `OrderService.java` — checkout 트랜잭션의 stock reserve + order/item/reservation 생성 규칙을 정확히 적기 위해 참고
- `PaymentService.java` — idempotency, outbox insertion, notification fallback 로직 확인을 위해 참고
- Compose health 확인 절차 — Compose 검증이 health probe 수준이며 도메인 시나리오까지 자동 검증하지 않는다는 한계를 정리하기 위해 참고
