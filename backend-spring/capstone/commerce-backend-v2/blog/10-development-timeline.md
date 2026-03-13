# commerce-backend-v2: 같은 커머스 도메인을 더 깊게 파서 대표 결과물로 만든 과정

`commerce-backend-v2`는 이 트랙의 대표 결과물이다. 중요한 건 새 도메인을 들고 온 데 있지 않다. baseline capstone과 같은 커머스 문제를 유지한 채, auth, order, payment, notification, ops를 어디까지 더 엄격하게 구현하고 검증했는지가 이 프로젝트의 핵심이다.

구현 순서는 세 갈래로 읽힌다. 먼저 `AuthApiTest`와 `CommercePortfolioApiTest`로 persisted auth와 end-to-end commerce flow를 고정했다. 다음으로 `OrderService`와 `PaymentService`에서 checkout, inventory reservation, idempotent payment, outbox 생성을 invariant로 묶었다. 마지막으로 `OutboxPublisher`, `CommerceMessagingIntegrationTest`, `RedisCartStoreTest`, `docs/verification.md`를 통해 Redis와 Kafka를 실제 검증 가능한 구현으로 닫았다.

## Phase 1. 도메인을 바꾸지 않고 auth와 commerce surface를 더 깊게 만들었다

대표 결과물을 만들 때 더 큰 도메인이나 더 많은 서비스 분해를 떠올리기 쉽다. 그런데 [`docs/architecture-overview.md`](../docs/architecture-overview.md)는 이 프로젝트가 modular monolith를 유지한다고 분명히 적는다. 중요한 건 크기보다 설명 가능성이라는 뜻이다.

그 선택은 테스트에서도 그대로 보인다. [`AuthApiTest`](../spring/src/test/java/com/webpong/study2/app/AuthApiTest.java)는 register, login, refresh, logout, Google callback linking까지 잡고, [`CommercePortfolioApiTest`](../spring/src/test/java/com/webpong/study2/app/CommercePortfolioApiTest.java)는 admin이 카테고리와 상품을 만들고 customer가 장바구니에 담아 checkout하고 결제한 뒤 주문 상태를 바꾸는 흐름까지 이어 간다.

```java
mockMvc.perform(
        post("/api/v1/auth/refresh")
            .cookie(new Cookie("refresh_token", loginSession.refreshToken()))
            .header("X-CSRF-TOKEN", "wrong-token"))
    .andExpect(status().isUnauthorized());

mockMvc.perform(
        post("/api/v1/payments/mock/confirm")
            .header("Authorization", "Bearer " + customerAccessToken)
            .header("Idempotency-Key", "idem-" + orderId)
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"orderId\": %d}".formatted(orderId)))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.orderStatus").value("PAID"));
```

왜 이 코드가 중요했는가. 같은 도메인을 유지한 채 baseline보다 더 깊어진 경계가 무엇인지 이 테스트가 바로 보여 주기 때문이다. auth는 cookie + CSRF refresh를 포함하고, commerce는 admin/customer 분리와 payment까지 이어진다.

초기 검증 CLI도 그 방향을 따른다.

```bash
cd spring
./gradlew testClasses --no-daemon
make test
```

`2026-03-13` 테스트 XML 기준으로 `AuthApiTest` 2개 테스트와 `CommercePortfolioApiTest` 1개 테스트가 실패 없이 통과했다. 대표 결과물의 surface가 두 축으로 동시에 고정됐다는 뜻이다.

여기서 새로 보인 건 포트폴리오의 깊이였다. 더 많은 키워드보다, 같은 도메인 안에서 더 많은 상태 전이를 실제로 설명 가능한가가 더 중요했다.

## Phase 2. checkout과 payment를 invariant와 idempotency로 묶었다

surface가 커졌다고 좋은 커머스 백엔드가 되는 건 아니다. 진짜 전환점은 주문과 결제 규칙이 어디에서 강제되는가다. [`OrderService.checkout()`](../spring/src/main/java/com/webpong/study2/app/order/application/OrderService.java)는 cart 상태를 읽어 재고를 reserve하고, `order_items`와 `inventory_reservations`를 함께 남긴다.

```java
for (Map.Entry<Long, Integer> entry : cartState.getItems().entrySet()) {
  ProductEntity product = products.get(entry.getKey());
  product.reserve(entry.getValue());
  totalAmount =
      totalAmount.add(product.getPrice().multiply(BigDecimal.valueOf(entry.getValue())));
}
productRepository.flush();
```

결제 쪽에서는 [`PaymentService.confirmMockPayment()`](../spring/src/main/java/com/webpong/study2/app/payment/application/PaymentService.java)가 idempotency key를 먼저 확인하고, 중복 요청이면 replay 응답을 돌려준다. 새 결제라면 order를 `PAID`로 바꾸고 reservation을 confirm하고 outbox row를 만든다.

```java
PaymentEntity existingPayment =
    paymentRepository.findByIdempotencyKey(idempotencyKey).orElse(null);
if (existingPayment != null) {
  OrderEntity existingOrder = orderService.requireOrder(existingPayment.getOrderId());
  return PaymentResponse.replayed(existingPayment, existingOrder.getStatus());
}
```

왜 이 코드가 중요했는가. 여기서 이 프로젝트는 "결제 API가 있다" 수준을 넘어서, 재고 예약, 상태 전이, 중복 결제 방지, 비동기 handoff까지 하나의 규칙 묶음으로 설명할 수 있게 된다. baseline capstone과 가장 크게 갈리는 지점도 바로 여기다.

이 단계의 CLI는 smoke와 Compose로 이어진다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification.md`는 `2026-03-09`에 lint, test, smoke, Compose health 확인이 통과했다고 남긴다. 이 프로젝트가 기능 수만 많은 게 아니라, 다시 띄워 확인할 수 있는 결과물이라는 뜻이다.

여기서 배운 건 invariant의 밀도였다. 좋은 커머스 백엔드는 endpoint 개수보다 언제 reserve하고 언제 replay해야 하는지를 얼마나 분명하게 말하는지로 갈린다.

## Phase 3. Redis와 Kafka를 buzzword가 아니라 검증 가능한 구현으로 닫았다

이 프로젝트를 대표 결과물로 만드는 마지막 요소는 Redis와 Kafka를 어디에만 쓰는지, 그리고 그게 실제 테스트로 증명되는지다. [`OutboxPublisher`](../spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OutboxPublisher.java)는 아직 publish되지 않은 outbox event를 읽어 Kafka로 보낸다.

```java
@Scheduled(fixedDelayString = "${app.messaging.publish-delay-ms}")
public void publishPending() {
  List<OutboxEventEntity> events =
      outboxEventRepository.findTop20ByPublishedAtIsNullOrderByIdAsc();
  for (OutboxEventEntity event : events) {
    kafkaTemplate
        .send(event.getEventType(), event.getAggregateId(), event.getPayload())
        .get(5, TimeUnit.SECONDS);
    event.markPublished();
  }
}
```

그리고 [`CommerceMessagingIntegrationTest`](../spring/src/test/java/com/webpong/study2/app/CommerceMessagingIntegrationTest.java)는 PostgreSQL, Redis, Kafka Testcontainers를 띄워 `order-paid` 이벤트가 실제 notification row로 이어지는지 확인한다. Redis cart는 [`RedisCartStoreTest`](../spring/src/test/java/com/webpong/study2/app/RedisCartStoreTest.java)에서 직렬화/역직렬화를 따로 고정한다.

```java
while (Instant.now().isBefore(deadline)
    && notificationRepository.findByDedupKey("order-paid:" + orderId).isEmpty()) {
  Thread.sleep(200L);
}

assertThat(notificationRepository.findByDedupKey("order-paid:" + orderId)).isPresent();
```

왜 이 코드가 중요했는가. Redis와 Kafka가 README 장식이 아니라 cart state 저장과 order-paid handoff라는 구체적 경계에만 쓰이고, 그 경계가 실제 테스트로 검증되기 때문이다.

마지막 CLI는 이 결과물을 닫는 확인 절차다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 특히 강하다.

- `2026-03-13` 기준 테스트 XML 9개 suite, 총 11개 테스트, 실패 0
- `CommerceMessagingIntegrationTest`: 1개 테스트, 실패 0, 실행 시간 `100.873`초
- `RedisCartStoreTest`: 1개 테스트, 실패 0
- `docs/verification.md` 기준 lint, test, smoke, Compose health 확인 통과

이 버전이 대표 결과물인 이유는 결국 여기 있다. 같은 커머스 도메인을 유지하면서도 auth, order, payment, notification, ops를 더 엄격한 invariant와 검증으로 묶었다. 그렇다고 live Google OAuth, real payment provider, live AWS provisioning을 끝냈다고 과장하지도 않는다. 경계가 분명하기 때문에 인터뷰에서도 설명 가능한 결과물이 된다.
