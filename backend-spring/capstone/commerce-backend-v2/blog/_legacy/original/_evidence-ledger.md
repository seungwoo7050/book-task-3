# commerce-backend-v2 Evidence Ledger

- 복원 기준:
  - `problem/README.md`, `docs/architecture-overview.md`, `docs/domain-model-and-state-transitions.md`, `docs/verification.md`, 실제 모듈 코드, 테스트, `2026-03-13` 재실행 CLI를 사용했다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어서 격리 대상은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - baseline을 같은 도메인에서 더 깊게 구현하되, 읽기 난도는 modular monolith 수준으로 유지한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/architecture-overview.md`
  - `docs/domain-model-and-state-transitions.md`
  - `docs/verification.md`
- 처음 가설:
  - 도메인을 바꾸지 않고 구현 깊이만 올려야 baseline 대비 개선점이 선명해진다.
- 실제 조치:
  - auth, catalog, cart, order, payment, notification, global 패키지 경계를 명시했다.
  - Redis와 Kafka를 feature justification이 있는 지점에만 제한적으로 연결했다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - architecture 문서가 modular monolith, request flow, Redis/Kafka 사용 이유를 먼저 정리한다.
- 핵심 코드 앵커:
  - `AuthService`, `CartService`, `OrderService`, `PaymentService`, `OutboxPublisher`, `OrderPaidEventConsumer`.
- 새로 배운 것:
  - 대표 capstone은 많은 기술을 썼다는 사실보다, 각 기술이 어떤 문제에만 연결돼 있는지를 분명히 말할 수 있어야 한다.
- 다음:
  - persisted auth와 checkout foundation부터 닫는다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - persisted local auth, mocked Google linking, cookie + CSRF, rate limit bucket을 먼저 만든다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/auth/application/AuthService.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/api/AuthController.java`
  - `spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java`
  - `spring/src/test/java/com/webpong/study2/app/AuthApiTest.java`
- 처음 가설:
  - baseline과 가장 큰 차이는 auth depth이므로, refresh token hashing, cookie rotation, mocked Google linking을 먼저 닫아야 한다.
- 실제 조치:
  - user, role, refresh token, oauth account, audit event persistence를 붙였다.
  - login/refresh/logout은 refresh token cookie와 CSRF header 조합으로 동작하게 했다.
  - Google authorize/callback은 live provider 대신 state/nonce contract를 구현했다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL in 2m 1s`로 끝났다.
- 핵심 코드 앵커:

```java
refreshTokenRepository.save(
    new RefreshTokenEntity(
        HashingSupport.sha256(refreshToken),
        user.getId(),
        csrfToken,
        Instant.now().plusSeconds(authProperties.refreshTokenSeconds())));
```

- 새로 배운 것:
  - refresh token은 토큰 문자열 자체보다, 해시를 저장하고 CSRF와 같이 검증하는 방식으로 다뤄야 보안 경계가 선명해진다.
- 다음:
  - auth 위에서 cart와 checkout foundation을 닫는다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - cart, checkout, inventory reservation을 modular monolith 안에서 연결한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/cart/application/CartService.java`
  - `spring/src/main/java/com/webpong/study2/app/order/application/OrderService.java`
  - `spring/src/test/java/com/webpong/study2/app/CommercePortfolioApiTest.java`
- 처음 가설:
  - cart를 Redis-friendly interface 뒤에 두고, checkout에서 stock reservation과 order item snapshot을 만들면 baseline보다 훨씬 설명 가능한 주문 흐름이 된다.
- 실제 조치:
  - `CartStore` 뒤에 in-memory/Redis 구현을 둘 수 있게 만들었다.
  - checkout은 product stock reserve, order 생성, order item snapshot, inventory reservation row 생성을 한 트랜잭션으로 묶었다.
  - optimistic locking conflict는 `ConflictException`으로 번역했다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `CommercePortfolioApiTest`가 admin category/product -> customer cart -> checkout -> payment -> admin fulfill 흐름을 한 테스트로 검증한다.
- 핵심 코드 앵커:

```java
inventoryReservationRepository.save(
    new InventoryReservationEntity(order.getId(), product.getId(), entry.getValue()));
```

- 새로 배운 것:
  - checkout은 단순 order insert가 아니라, stock, reservation, order snapshot이 같이 생겨야 이후 payment와 cancellation을 안정적으로 설명할 수 있다.
- 다음:
  - payment idempotency와 outbox/Kafka를 닫고, Testcontainers로 최종 proof를 만든다.

## Phase 4

- 시간 표지: Phase 4
- 당시 목표:
  - payment confirmation이 order status, reservation, outbox, notification까지 이어지게 만든다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/payment/application/PaymentService.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OutboxPublisher.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OrderPaidEventConsumer.java`
  - `spring/src/test/java/com/webpong/study2/app/CommerceMessagingIntegrationTest.java`
- 처음 가설:
  - idempotent mock payment와 outbox/Kafka handoff만 제대로 연결해도 portfolio-grade capstone의 핵심 증명은 충분하다.
- 실제 조치:
  - `Idempotency-Key`로 기존 payment를 재생할 수 있게 했다.
  - payment 성공 시 order를 `PAID`로 옮기고 reservation을 confirm하며 outbox row를 만든다.
  - publisher는 pending outbox row를 topic으로 보내고, consumer는 notification을 저장한다.
  - Testcontainers로 PostgreSQL, Redis, Kafka를 띄워 end-to-end messaging test를 만들었다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 9개, `failures=0`이 확인됐다.
  - `CommerceMessagingIntegrationTest`를 포함한 전체 suite가 `BUILD SUCCESSFUL in 2m 1s`로 끝났다.
  - `2026-03-09` 검증 메모에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.
- 핵심 코드 앵커:

```java
outboxEventRepository.save(
    new OutboxEventEntity(
        "order",
        String.valueOf(order.getId()),
        messagingProperties.orderPaidTopic(),
        serialize(
            new OrderPaidPayload(
                messagingProperties.orderPaidTopic(),
                order.getId(),
                order.getUserId(),
                order.getTotalAmount()))));
```

- 새로 배운 것:
  - portfolio-grade capstone의 결정적 차이는 "Kafka를 쓴다"가 아니라, 결제 성공 사실이 outbox row, scheduled publisher, consumer, notification row까지 어떻게 이어지는지 끝까지 증명하는 데 있다.
- 다음:
  - live provider integration, real payment gateway, live infra는 이후 확장 과제로 남긴다.
