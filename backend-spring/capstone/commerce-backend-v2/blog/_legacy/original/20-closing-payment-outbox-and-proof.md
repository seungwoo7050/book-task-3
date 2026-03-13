# paid order loop를 끝까지 닫는 두 번째 축

`commerce-backend-v2`가 portfolio-grade 결과물로 읽히는 결정적 장면은 payment confirmation이 order status, reservation, outbox, Kafka consumer, notification row까지 이어지는 구간이다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌리면, 이 프로젝트는 "Kafka를 썼다"가 아니라 "결제 성공 사실이 어떤 상태 전이와 어떤 저장소를 거쳐 이동하는가"를 끝까지 증명한다.

## Phase 4

### Session 1

- 당시 목표:
  - mock payment confirmation을 idempotent하게 만들고, 그 결과를 outbox/Kafka/notification까지 이어지게 한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/payment/application/PaymentService.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OutboxPublisher.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OrderPaidEventConsumer.java`
  - `spring/src/test/java/com/webpong/study2/app/CommerceMessagingIntegrationTest.java`
- 처음 가설:
  - 실제 PG 연동이 없어도 idempotent payment, outbox row, scheduled publisher, Kafka consumer를 연결하면 결제 이후 비동기 흐름을 충분히 설명할 수 있다.
- 실제 진행:
  - `PaymentService.confirmMockPayment()`는 `Idempotency-Key`로 기존 payment를 재생하거나, 새 payment를 만들고 order를 `PAID`로 바꾼다.
  - payment 성공 시 reservation을 confirm하고 audit event와 outbox event를 저장한다.
  - `OutboxPublisher`는 pending event를 topic으로 보내고, `OrderPaidEventConsumer`는 notification row를 적재한다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 `make test`가 `BUILD SUCCESSFUL in 2m 1s`로 끝났다.
- 같은 실행에서 XML 리포트 9개, `failures=0`이 확인됐다.

핵심 코드:

```java
PaymentEntity existingPayment =
    paymentRepository.findByIdempotencyKey(idempotencyKey).orElse(null);
if (existingPayment != null) {
  OrderEntity existingOrder = orderService.requireOrder(existingPayment.getOrderId());
  return PaymentResponse.replayed(existingPayment, existingOrder.getStatus());
}
```

왜 이 코드가 중요했는가:

- 결제 시스템에서 가장 먼저 닫아야 하는 질문은 "다시 눌렀을 때 어떻게 되는가"다. idempotency가 먼저 있어야 outbox와 Kafka도 안정적으로 설명된다.

새로 배운 것:

- 비동기 시스템의 안정성은 브로커보다 먼저, 동기 경로에서 중복 결제를 어떻게 흡수하느냐에 달려 있다.

다음:

- payment 이후 이벤트 handoff와 consumer proof를 실제 테스트로 닫는다.

## 최종 증명 흐름

`CommercePortfolioApiTest`는 admin category/product 생성, customer cart 추가, checkout, mock payment confirmation, replayed payment, admin fulfill, notification 저장까지 사용자 시나리오를 한 번에 복원한다. 여기에 `CommerceMessagingIntegrationTest`가 PostgreSQL, Redis, Kafka Testcontainers를 붙여 `order-paid` 이벤트가 실제로 publish/consume되는지까지 검증한다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `CommerceMessagingIntegrationTest`는 PostgreSQL, Redis, Kafka 컨테이너를 띄운 뒤 `outboxPublisher.publishPending()`를 호출하고 `notificationRepository.findByDedupKey("order-paid:" + orderId)`가 채워질 때까지 기다린다.
- `docs/verification.md`에는 `2026-03-09` 기준 `make lint`, `make test`, `make smoke`, Compose health 확인 통과가 남아 있다.

핵심 코드:

```java
kafkaTemplate
    .send(event.getEventType(), event.getAggregateId(), event.getPayload())
    .get(5, TimeUnit.SECONDS);
event.markPublished();
```

왜 이 코드가 중요했는가:

- outbox publisher가 pending row를 실제 Kafka handoff로 바꾸는 순간이 여기다. `markPublished()`가 send 뒤에만 호출되기 때문에, event lifecycle 설명이 매우 직선적으로 남는다.

핵심 코드:

```java
@KafkaListener(topics = "${app.messaging.order-paid-topic}", groupId = "commerce-backend-v2")
public void consume(String payload) throws Exception {
  OrderPaidMessage message = objectMapper.readValue(payload, OrderPaidMessage.class);
  if (!messagingProperties.orderPaidTopic().equals(message.topic())) {
    return;
  }
  notificationService.recordOrderPaid(message.userId(), message.orderId(), message.amount());
}
```

왜 이 코드가 중요했는가:

- consumer가 topic 검증과 notification deduplication 쪽으로 역할을 제한하고 있어서, Kafka를 쓴 이유가 단순 기술 과시가 아니라 order-paid handoff라는 점이 더 잘 보인다.

새로 배운 것:

- portfolio-grade capstone의 차이는 "많이 만들었다"가 아니라, 중요한 상태 전이를 테스트와 저장소 흔적으로 끝까지 따라갈 수 있다는 데 있다.

다음:

- live Google OAuth, real payment gateway, live AWS provisioning은 다음 확장으로 남긴다.
