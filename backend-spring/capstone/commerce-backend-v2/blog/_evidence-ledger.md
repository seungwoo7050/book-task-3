# commerce-backend-v2 evidence ledger

- 복원 원칙: 기존 blog 본문은 입력 근거에서 제외하고, `README/problem/docs`, 실제 소스, 테스트, `2026-03-14` 재실행 결과만 사용했다.
- 날짜 고정: 아래 검증과 수동 확인은 모두 `2026-03-14` 기준이다.
- 작업 환경 메모: 로컬 JRE가 없어 Gradle은 `eclipse-temurin:21-jdk` 컨테이너에서 다시 실행했고, Testcontainers suite는 `TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal`를 넣어야 통과했다.

## 핵심 입력 근거

- 문제/설명
  - `README.md`
  - `problem/README.md`
  - `docs/README.md`
  - `docs/architecture-overview.md`
  - `docs/verification.md`
  - `spring/README.md`
  - `spring/compose.yaml`
  - `spring/.env.example`
- auth/security
  - `spring/src/main/java/com/webpong/study2/app/auth/api/AuthController.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/application/AuthService.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/infrastructure/AdminBootstrapInitializer.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/infrastructure/JwtService.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/infrastructure/OAuthStateStore.java`
  - `spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java`
  - `spring/src/main/java/com/webpong/study2/app/global/security/JwtAuthenticationFilter.java`
  - `spring/src/main/java/com/webpong/study2/app/global/security/AuthenticationFacade.java`
- commerce flow
  - `spring/src/main/java/com/webpong/study2/app/catalog/api/AdminCategoryController.java`
  - `spring/src/main/java/com/webpong/study2/app/catalog/api/AdminProductController.java`
  - `spring/src/main/java/com/webpong/study2/app/cart/api/CartController.java`
  - `spring/src/main/java/com/webpong/study2/app/order/api/OrderController.java`
  - `spring/src/main/java/com/webpong/study2/app/order/api/AdminOrderController.java`
  - `spring/src/main/java/com/webpong/study2/app/order/application/OrderService.java`
  - `spring/src/main/java/com/webpong/study2/app/payment/api/PaymentController.java`
  - `spring/src/main/java/com/webpong/study2/app/payment/application/PaymentService.java`
  - `spring/src/main/java/com/webpong/study2/app/global/error/GlobalExceptionHandler.java`
  - `spring/src/main/resources/db/migration/V2__commerce.sql`
- redis/kafka/ops
  - `spring/src/main/java/com/webpong/study2/app/cart/infrastructure/RedisCartStore.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/infrastructure/RedisAttemptLimiter.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OutboxPublisher.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OrderPaidEventConsumer.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/domain/OutboxEventEntity.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/domain/OutboxEventRepository.java`
  - `spring/src/main/java/com/webpong/study2/app/notification/application/NotificationService.java`
  - `spring/src/main/java/com/webpong/study2/app/global/api/HealthController.java`
  - `spring/src/main/java/com/webpong/study2/app/global/api/LabInfoController.java`
  - `spring/src/main/resources/application.yml`
- 테스트
  - `spring/src/test/java/com/webpong/study2/app/AuthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/CommercePortfolioApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/CommerceMessagingIntegrationTest.java`
  - `spring/src/test/java/com/webpong/study2/app/RedisCartStoreTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`

## 재실행한 검증

### 1. lint

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL`

### 2. test

처음에는 아래 명령이 `CommerceMessagingIntegrationTest`에서 `Could not connect to Ryuk at 172.17.0.1:54155`로 실패했다.

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

host override를 추가한 뒤 전체 suite가 통과했다.

```bash
docker run --rm \
  -e TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal \
  -v "$PWD:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 최종 결과: `BUILD SUCCESSFUL`

### 3. smoke

```bash
docker run --rm \
  -e TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal \
  -v "$PWD:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -w /workspace \
  eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL`

### 4. Compose 런타임

`.env.example`를 기준으로 로컬 `.env`를 만든 뒤 Compose를 다시 올렸다.

```bash
docker compose up --build -d
```

- 결과: `postgres`, `redis`, `mailpit`, `redpanda`, `app` 모두 시작

## 수동 HTTP/DB 확인

- `GET /api/v1/health/live` -> `200`, `status: UP`
- `GET /api/v1/health/ready` -> `200`, `status: UP`
- `GET /actuator/health` -> `403`
- `GET /api/v1/lab/info` -> `200`
- `POST /api/v1/admin/categories` without auth -> `403`
- `POST /api/v1/auth/login` as bootstrap admin -> `200`
- `POST /api/v1/auth/register` as new customer -> `201`
- `POST /api/v1/auth/login` as new customer -> `200`
- `POST /api/v1/auth/refresh` with refresh cookie + csrf -> `200`
- `GET /api/v1/me` with bearer -> `200`
- `POST /api/v1/admin/categories` with customer bearer -> `403`
- invalid `POST /api/v1/admin/products` -> `400`, validation errors 4개 반환
- valid category create -> `201`
- valid product create -> `201`
- `POST /api/v1/cart/items` -> `200`
- `POST /api/v1/orders` -> `200`, `PENDING_PAYMENT`
- first `POST /api/v1/payments/mock/confirm` -> `200`, `replayed: false`
- second same idempotency key -> `200`, `replayed: true`
- product stock `3 -> 2`
- postgres query `notifications` -> `order-paid:1|ORDER_PAID`
- postgres query `outbox_events` -> `commerce.order-paid|pending`

## 이 문서에서 사용한 해석

- `refresh`가 같은 access token 문자열을 다시 돌려준 현상은 `JwtService`가 `jti` 없이 동일 claim set으로 토큰을 서명한다는 소스와 `2026-03-14` 수동 응답을 함께 본 source-based inference다.
- notification row는 생겼지만 outbox row가 `pending`에 남는 현상은 `OutboxPublisher.publishPending()`에 `@Transactional` 또는 explicit save가 없다는 소스와 postgres 조회 결과를 함께 본 source-based inference다.
- `CommerceMessagingIntegrationTest`가 assert하는 것은 notification row 존재까지이며, `publishedAt` persistence 자체는 자동 검증 범위에 들어 있지 않다는 점도 테스트 소스에서 직접 확인했다.
- actuator health가 public probe surface가 아니라는 결론은 `SecurityConfig`의 permit 목록과 실제 `403` 응답을 함께 본 사실 판단이다.
