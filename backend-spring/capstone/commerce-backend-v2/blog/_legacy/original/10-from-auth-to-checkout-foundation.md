# baseline을 같은 도메인에서 더 깊게 만드는 첫 번째 축

`commerce-backend-v2`가 baseline과 다른 지점은 단순히 기능이 많다는 데 있지 않다. 같은 커머스 도메인을 유지한 채, auth와 checkout이 어떤 상태 전이와 persistence를 더 갖게 되었는지가 더 중요하다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면, 이 프로젝트의 첫 번째 축은 persisted auth와 checkout foundation이라는 점이 분명히 보인다.

## 구현 순서 요약

- docs가 modular monolith와 core request flow를 먼저 정리한다.
- `AuthService`, `AuthController`, `SecurityConfig`가 persisted auth를 만든다.
- `CartService`와 `OrderService`가 cart/checkout foundation과 inventory reservation을 만든다.
- `AuthApiTest`와 `CommercePortfolioApiTest`가 사용자 흐름을 고정한다.

## Phase 1

### Session 1

- 당시 목표:
  - baseline을 같은 도메인에서 더 깊게 만들되, 구조는 인터뷰에서 설명 가능한 modular monolith로 유지한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/architecture-overview.md`
  - `docs/domain-model-and-state-transitions.md`
  - `docs/verification.md`
- 처음 가설:
  - 도메인을 바꾸지 않고 경계와 상태 전이만 더 촘촘하게 만들면 baseline 대비 개선점이 가장 선명해진다.
- 실제 진행:
  - auth, catalog, cart, order, payment, notification, global 패키지 경계를 문서와 코드에서 맞췄다.
  - request flow를 login -> cart -> checkout -> payment -> outbox -> notification 순으로 정리했다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- architecture 문서가 Redis와 Kafka의 사용 이유를 "implementation detail of justified features"로 제한해 적고 있다.

핵심 코드:

```java
.requestMatchers("/api/v1/admin/**")
.hasRole("ADMIN")
.anyRequest()
.authenticated()
```

왜 이 코드가 중요했는가:

- baseline보다 깊어진 auth의 핵심은 엔드포인트마다 인증/인가 경계가 실제 security config에 들어갔다는 점이다.

새로 배운 것:

- 대표 capstone은 기능 목록보다 "어떤 경계를 코드에서 강제하는가"가 더 중요하다.

다음:

- persisted auth와 cookie/CSRF rotation을 먼저 닫는다.

## Phase 2

### Session 1

- 당시 목표:
  - register/login/refresh/logout/me와 mocked Google linking을 persisted auth로 닫는다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/auth/application/AuthService.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/api/AuthController.java`
  - `spring/src/test/java/com/webpong/study2/app/AuthApiTest.java`
- 처음 가설:
  - refresh token hash 저장, cookie 회전, CSRF 검증, mocked Google callback만 있어도 baseline auth와의 차이는 충분히 설명된다.
- 실제 진행:
  - user, role, refresh token, oauth account, audit event를 모두 persistence로 옮겼다.
  - `AuthController`는 access token은 본문에, refresh token은 cookie에, CSRF는 헤더/쿠키 조합으로 드러냈다.
  - `AuthApiTest`는 register -> login -> me -> refresh -> logout -> refresh rejection과 Google callback linking을 검증한다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 전체 suite가 `BUILD SUCCESSFUL in 2m 1s`로 끝났다.

핵심 코드:

```java
ResponseCookie refreshCookie =
    ResponseCookie.from("refresh_token", refreshToken)
        .httpOnly(true)
        .sameSite("Lax")
        .path("/api/v1/auth")
        .maxAge(clear ? 0 : 60L * 60L * 24L * 14L)
        .build();
```

왜 이 코드가 중요했는가:

- baseline의 auth가 token shape만 돌려줬다면, v2는 refresh token을 cookie 경계 안으로 넣어 브라우저 시나리오까지 설명 가능한 수준으로 올린다.

새로 배운 것:

- persisted auth의 설명력은 JWT 발급 자체보다 refresh token과 CSRF를 어떤 transport 경계로 나누는지에서 나온다.

다음:

- auth 위에 cart와 checkout foundation을 올린다.

## Phase 3

### Session 1

- 당시 목표:
  - cart, checkout, inventory reservation을 auth와 자연스럽게 이어지는 흐름으로 만든다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/cart/application/CartService.java`
  - `spring/src/main/java/com/webpong/study2/app/order/application/OrderService.java`
  - `spring/src/test/java/com/webpong/study2/app/CommercePortfolioApiTest.java`
- 처음 가설:
  - cart state를 interface 뒤에 두고, checkout에서 reservation row와 order item snapshot을 같이 만들면 이후 payment/cancel state transition을 설명하기 쉬워진다.
- 실제 진행:
  - `CartService`는 `CartStore` 뒤에 in-memory/Redis 구현을 숨겼다.
  - `OrderService.checkout()`은 stock reserve, order 생성, order item snapshot, reservation row 저장을 한 트랜잭션으로 묶었다.
  - `CommercePortfolioApiTest`는 admin category/product -> customer cart -> checkout까지 실제 사용자 흐름을 검증한다.

CLI:

```bash
make test
```

검증 신호:

- `CommercePortfolioApiTest`가 cart item count, totalAmount, `PENDING_PAYMENT` order 생성까지 실제로 증명한다.

핵심 코드:

```java
try {
  for (Map.Entry<Long, Integer> entry : cartState.getItems().entrySet()) {
    ProductEntity product = products.get(entry.getKey());
    product.reserve(entry.getValue());
    totalAmount =
        totalAmount.add(product.getPrice().multiply(BigDecimal.valueOf(entry.getValue())));
  }
  productRepository.flush();
} catch (IllegalArgumentException
    | OptimisticLockException
    | OptimisticLockingFailureException exception) {
  throw new ConflictException("Inventory changed during checkout. Retry the request.");
}
```

왜 이 코드가 중요했는가:

- checkout이 단순 order insert가 아니라 stock reservation과 optimistic locking conflict까지 한 번에 처리하는 지점이 여기다. v2의 주문 흐름이 baseline보다 깊어진 핵심이기도 하다.

새로 배운 것:

- checkout은 결제 전 단계지만 이미 inventory consistency 문제를 안고 있다. 그래서 payment보다 먼저 reservation row가 필요해진다.

다음:

- payment idempotency와 outbox/Kafka proof로 order loop를 닫는다.
