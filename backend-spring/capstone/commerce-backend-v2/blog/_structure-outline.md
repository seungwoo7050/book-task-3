# commerce-backend-v2 structure outline

## 중심 질문

- `commerce-backend-v2`가 왜 baseline의 "기능 확장판"이 아니라 더 깊어진 대표 capstone인지
- 그 깊이를 설명할 때 어떤 runtime signal은 살리고, 어떤 미완료 seam은 숨기지 말아야 하는지

## 글 흐름

1. auth가 persisted user/session/role guard로 바뀐 지점부터 시작한다.
2. validation, cart, checkout, payment idempotency가 baseline과 달라진 실제 계약을 보여 준다.
3. Redis/Kafka wiring와 Testcontainers 검증을 설명하되, outbox `published_at` 미반영 결함을 같이 드러낸다.
4. custom health는 공개돼 있지만 actuator는 `403`인 ops 표면 차이로 마무리한다.

## 반드시 남길 증거

- `SecurityConfig`, `JwtAuthenticationFilter`, `AuthService`
- `AdminCategoryController`, `AdminProductController`, `OrderService`, `PaymentService`
- `OutboxPublisher`, `OrderPaidEventConsumer`, `OutboxEventEntity`
- `CommercePortfolioApiTest`, `CommerceMessagingIntegrationTest`
- `2026-03-14` 재실행 lint/test/smoke 결과
- `2026-03-14` Compose HTTP/DB 확인 결과

## 반드시 피할 서술

- "Google OAuth까지 완전 구현됐다"는 식의 과장
- "Kafka outbox가 완전히 닫혔다"는 식의 단정
- "actuator health가 공개 probe endpoint다"라는 오독
- baseline과 같은 문제를 푼 이유를 단순 반복처럼 축소하는 설명

## 톤 체크

- README 확대판이 아니라, 실제로 다시 실행하면서 확인한 chronology가 살아 있어야 한다.
- 이미 답을 다 알고 쓴 홍보문보다, 무엇이 좋아졌고 무엇이 아직 삐걱대는지 함께 읽히는 탐색형 톤을 유지한다.
