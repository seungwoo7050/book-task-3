# commerce-backend-v2 시리즈 지도

`commerce-backend-v2`는 이 트랙의 대표 결과물이다. baseline capstone과 같은 커머스 도메인을 유지한 채, persisted auth, cart/checkout foundation, payment idempotency, outbox/Kafka notification, ops surface를 더 깊게 구현했다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면, 이 프로젝트의 차별점은 기술 개수보다 각 기술이 어떤 경계를 닫는지 끝까지 설명할 수 있다는 데 있다.

## 이 프로젝트가 푸는 문제

- baseline보다 깊은 auth, order, payment, notification 흐름을 같은 도메인에서 만든다.
- Redis와 Kafka를 buzzword가 아니라 cart/throttling/outbox handoff에만 붙인다.
- Testcontainers와 Compose까지 포함한 검증 표면을 남긴다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/architecture-overview.md`
- `docs/domain-model-and-state-transitions.md`
- `docs/verification.md`
- `AuthService`, `CartService`, `OrderService`, `PaymentService`
- `OutboxPublisher`, `OrderPaidEventConsumer`
- `AuthApiTest`, `CommercePortfolioApiTest`, `CommerceMessagingIntegrationTest`
- `2026-03-13` `make test` 재실행

## 읽는 순서

1. `10-from-auth-to-checkout-foundation.md`
2. `20-closing-payment-outbox-and-proof.md`
3. `_evidence-ledger.md`
4. `_structure-outline.md`

## 시리즈의 중심 질문

- baseline 대비 어디가 가장 먼저 깊어졌는가
- persisted auth와 checkout foundation은 어떤 상태 전이를 더 추가했는가
- payment/outbox/Kafka proof는 어떻게 끝까지 닫혔는가
