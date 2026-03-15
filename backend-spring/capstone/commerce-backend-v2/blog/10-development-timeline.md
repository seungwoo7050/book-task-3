# commerce-backend-v2: 같은 커머스 도메인을 더 깊게 다시 묶되, 남은 seam도 숨기지 않은 대표 capstone

`commerce-backend-v2`를 읽는 가장 좋은 방법은 "기능이 많다"가 아니라 "baseline에서 얕았던 지점을 어디까지 실제 계약으로 바꿨는가"를 따라가는 것이다. `problem/README.md`와 `docs/architecture-overview.md`는 둘 다 같은 도메인을 유지한 채 modular monolith로 깊이를 올리겠다고 말한다. `2026-03-14`에 소스, 테스트, Compose 런타임을 다시 확인해 보니 그 말은 절반 이상 사실이지만, async handoff와 actuator 표면처럼 README보다 덜 매끈한 부분도 분명히 남아 있었다.

## Step 1. fake query-param auth를 버리고 persisted auth와 role guard를 올렸다

baseline capstone과 가장 먼저 갈라지는 곳은 auth다. `AuthController`와 `AuthService`는 이제 `users`, `user_roles`, `refresh_tokens`, `oauth_accounts`, `audit_events` 테이블을 실제로 사용하고, `AdminBootstrapInitializer`는 부팅 시 admin 계정을 보장한다. `SecurityConfig`는 `/api/v1/admin/**`를 `hasRole("ADMIN")`으로 묶고, `JwtAuthenticationFilter`는 bearer token을 파싱해 현재 user profile을 다시 조회한다.

이 차이는 `2026-03-14` 수동 검증에서 바로 드러났다.

- `POST /api/v1/auth/register` -> `201`
- `POST /api/v1/auth/login` -> `200`, access token + refresh cookie + csrf token 발급
- `POST /api/v1/auth/refresh` -> `200`
- `GET /api/v1/me` with bearer -> `200`
- `POST /api/v1/admin/categories` without auth -> `403`
- `POST /api/v1/admin/categories` with customer token -> `403`

다만 여기서도 과장하면 안 된다. Google OAuth는 live provider가 아니라 `OAuthStateStore`가 `state`와 `nonce`를 메모리에 저장하고 `google/callback` body를 직접 받는 contract-level mock이다. 또 `JwtService.createAccessToken()`은 `jti` 같은 고유 claim 없이 `sub/email/roles/iat/exp`만 넣기 때문에, 같은 초에 refresh를 호출하면 access token 문자열이 login 때와 동일하게 다시 나올 수 있다. 이 부분은 `JwtService` 소스와 `2026-03-14` 수동 refresh 응답이 같은 토큰 문자열을 반환한 결과를 함께 보고 내린 source-based inference다.

## Step 2. catalog, cart, checkout, payment를 실제 validation과 상태 전이로 묶었다

두 번째 차이는 "커머스 기능이 있다"가 아니라, invalid input과 역할 경계가 실제 runtime contract로 바뀌었다는 점이다. `AdminCategoryController`, `AdminProductController`, `CartController`, `PaymentController`는 모두 `@Valid`와 constraint annotation을 달고 있고, `GlobalExceptionHandler`는 validation failure를 `problem+json`으로 정리한다.

`2026-03-14` 재실행 결과는 baseline과 대비되는 신호를 분명하게 보여 줬다.

- admin invalid product create -> `400`
- 오류 body에 `name`, `description`, `price`, `stock` validation error가 모두 포함
- valid category create -> `201`
- valid product create -> `201`
- `GET /api/v1/products` -> 상품 목록 확인
- customer cart add -> `200`, `itemCount: 1`, `totalAmount: 199.99`
- checkout -> `200`, order status `PENDING_PAYMENT`
- payment confirm -> `200`, order status `PAID`
- same `Idempotency-Key` replay -> `200`, `replayed: true`
- checkout 전 stock `3`, 결제 후 stock `2`

여기서 핵심 코드는 `OrderService.checkout()`와 `PaymentService.confirmMockPayment()`다. checkout은 cart state를 읽어 상품 재고를 reserve하고, `order_items`와 `inventory_reservations`를 함께 남긴 뒤 cart를 비운다. payment는 idempotency key로 replay를 먼저 차단하고, 처음 요청일 때만 payment row를 만들고 주문을 `PAID`로 전환한다. baseline에서 비어 있던 "재고 예약", "결제 중복 방지", "주문 상태 전이"가 이제는 실제 서비스 규칙이 됐다는 뜻이다.

## Step 3. Redis와 Kafka는 실제로 붙어 있지만, outbox 완료 표시는 아직 깨져 있다

이 프로젝트를 대표 capstone으로 보게 만드는 마지막 요소는 Redis/Kafka를 README 장식으로만 두지 않았다는 점이다. docker profile이 켜지면 `FeatureProperties`가 `redis-cart-enabled`, `redis-rate-limit-enabled`, `messaging-enabled`를 모두 `true`로 바꾸고, `RedisCartStore`, `RedisAttemptLimiter`, `OutboxPublisher`, `OrderPaidEventConsumer`가 실제 빈으로 올라온다. `CommerceMessagingIntegrationTest`도 PostgreSQL, Redis, Kafka Testcontainers를 함께 띄워 `order-paid` 이후 notification row가 생기는지 확인한다.

자동 검증은 `2026-03-14`에 다시 돌렸다.

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'

docker run --rm \
  -e TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal \
  -v "$PWD:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm \
  -e TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal \
  -v "$PWD:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

세 명령은 모두 통과했다. 다만 중요한 환경 메모가 하나 있다. 처음 `./gradlew test`를 같은 컨테이너 방식으로 실행했을 때 `CommerceMessagingIntegrationTest`가 `Could not connect to Ryuk at 172.17.0.1:54155`로 실패했고, `TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal`를 넣은 뒤에야 통과했다. 즉 코드 자체는 녹색이지만, 이 워크스페이스의 container-in-container 검증은 host override까지 포함해 재현해야 한다.

그리고 `2026-03-14` Compose 런타임에서 더 중요한 실제 결함 하나가 드러났다. 결제 후 notification row는 생성됐지만, 같은 order id에 대한 `outbox_events.published_at`는 여전히 `NULL`이었다.

- notifications query -> `order-paid:1|ORDER_PAID`
- outbox query -> `commerce.order-paid|pending`

이 신호는 `OutboxPublisher.publishPending()`가 `event.markPublished()`만 호출하고 별도의 `save()`나 `@Transactional` 경계를 두지 않는 현재 소스와 맞물린다. 따라서 "메시지는 발행되고 consumer는 동작했지만 published marker는 DB에 남지 않는다"는 해석이 가장 설득력 있다. 이 문장은 소스와 DB 상태를 함께 본 source-based inference다.

여기서 특히 구분해야 할 점이 하나 더 있다. `CommerceMessagingIntegrationTest`가 자동으로 보장하는 것은 `notificationRepository.findByDedupKey("order-paid:" + orderId)`가 eventually 채워진다는 사실까지다. 즉 canonical suite는 "consumer가 order-paid를 받아 notification row를 만든다"는 경계는 잠그지만, `outbox_events.published_at` persistence까지 assert하지는 않는다. 그래서 지금 남아 있는 seam은 green test를 부정하는 반례가 아니라, green test가 아직 닫지 않는 bookkeeping 층이라고 읽는 편이 정확하다.

## Step 4. ops surface는 두 겹으로 나뉜다

마지막으로 ops 표면도 README만 보면 매끈해 보이지만 실제로는 두 층으로 나뉜다. `HealthController`가 제공하는 `/api/v1/health/live`, `/api/v1/health/ready`는 public이고 `2026-03-14` 재실행에서도 둘 다 `200 UP`이었다. `LabInfoController`도 `200`으로 서비스 이름, summary, track을 돌려준다.

그런데 `/actuator/health`는 같은 Compose 런타임에서 `403`이었다. 이유는 `SecurityConfig`가 `/actuator/**`를 permit하지 않기 때문이다. 다시 말해 이 프로젝트의 public probe surface는 actuator가 아니라 custom `/api/v1/health/*` 쪽이다. health/readiness가 "있다"는 README 문장은 맞지만, 그 접근 경로를 막연히 actuator로 상상하면 runtime과 어긋난다.

## 정리

`commerce-backend-v2`는 확실히 baseline보다 깊다. persisted auth, admin guard, validation, checkout/payment state machine, Redis cart, Kafka consumer, Compose-backed runtime까지 실제로 확인된다. 하지만 이 프로젝트를 좋은 capstone으로 만드는 이유는 완벽해서가 아니라, mock Google, mock payment, modular monolith 유지, 그리고 아직 pending에 남는 outbox bookkeeping 같은 현재 한계까지 같이 설명할 수 있기 때문이다. 이 정도면 "portfolio-grade learning artifact"라는 말은 지킬 수 있지만, 아직 "production commerce platform"이라고 단정할 단계는 아니다.
