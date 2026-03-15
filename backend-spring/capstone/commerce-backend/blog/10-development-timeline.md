# commerce-backend: 커머스 흐름은 이어지지만 auth와 운영 의미는 아직 deliberately thin한 baseline capstone

`commerce-backend`는 이 트랙의 첫 capstone이지만, 다시 읽어 보면 "커머스 서비스를 끝냈다"기보다 "같은 도메인을 한 번 얕게 묶어서 다음 버전과 비교할 기준선을 남겼다"는 표현이 더 맞다. auth는 persisted identity가 아니라 query param contract 수준이고, admin/catalog/cart/order는 같은 앱 안에서 이어지지만 authorization, validation, payment, async integration은 거의 비어 있다.

2026-03-14에는 기존 blog를 입력 근거에서 제외하고, `CommerceAuthController`, `CommerceController`, `CommerceService`, domain entity들, migration, `CommerceApiTest`, 컨테이너 재검증과 수동 HTTP 호출만으로 문서를 다시 썼다. 다시 보니 이 capstone의 핵심 질문은 "무엇이 합쳐졌는가"보다 "무엇을 일부러 아직 얕게 두었는가"였다.

## Phase 1. user journey는 이어지지만 auth는 contract-level fake surface에 머문다

테스트 [`CommerceApiTest`](../spring/src/test/java/com/webpong/study2/app/CommerceApiTest.java)는 로그인부터 주문 조회까지 한 번에 묶는다. 이 흐름 덕분에 capstone다운 통합 surface는 분명히 보인다.

```java
mockMvc
    .perform(post("/api/v1/auth/login").param("email", "buyer@example.com"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.accessToken").exists());
```

하지만 auth 자체를 보면 baseline 성격이 바로 드러난다. [`CommerceAuthController`](../spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceAuthController.java)는 `email` query param 하나만 받아 고정된 `"commerce-access-token"`을 반환하고, `/api/v1/me`도 request param `email`을 그대로 echo하면서 role을 `"CUSTOMER"`로 찍어 준다.

```java
@PostMapping("/auth/login")
public Map<String, String> login(@RequestParam String email) {
  return Map.of("accessToken", "commerce-access-token", "email", email);
}

@GetMapping("/me")
public Map<String, String> me(@RequestParam String email) {
  return Map.of("email", email, "role", "CUSTOMER");
}
```

2026-03-14 수동 호출에서도 이건 그대로 확인됐다. 토큰은 사용자마다 다르지 않았고, `/api/v1/me?email=buyer@example.com`은 인증 없이 바로 `{"role":"CUSTOMER","email":"buyer@example.com"}`를 돌려줬다. 즉 이 capstone은 auth를 연결 부품으로만 두고 있을 뿐, identity enforcement는 아직 아니다.

이 점은 downstream flow에서도 반복된다. `POST /api/v1/cart/items`는 body의 `customerEmail`을 그대로 서비스에 넘기고, `POST /api/v1/orders`도 authenticated principal이 아니라 query param `customerEmail`만 읽는다. 다시 말해 테스트가 login부터 시작한다고 해서, 런타임 contract까지 token-gated identity로 닫히는 것은 아니다. baseline capstone의 user journey는 narrative상 이어지지만, 실제 권한/주체 연결은 아직 얕다.

## Phase 2. catalog, cart, order는 실제로 이어지지만 admin/public 경계와 validation은 비어 있다

커머스 흐름의 핵심은 [`CommerceController`](../spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceController.java)와 [`CommerceService`](../spring/src/main/java/com/webpong/study2/app/commerce/application/CommerceService.java)에 있다. 상품 생성, 상품 조회, cart item 추가, checkout, admin order 조회가 한 서비스 안에서 이어진다.

```java
@PostMapping("/admin/products")
public CommerceService.ProductResponse createProduct(@RequestBody CreateProductRequest request) {
  return commerceService.createProduct(request.name(), request.price(), request.stock());
}

@PostMapping("/orders")
public CommerceService.OrderResponse checkout(@RequestParam @Email String customerEmail) {
  return commerceService.checkout(customerEmail);
}
```

문제는 이 surface에 권한 경계가 거의 없다는 점이다. [`SecurityConfig`](../spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java)는 다른 backend-spring labs처럼 `/api/v1/**` 전체를 `permitAll()` 한다. 그래서 `/api/v1/admin/products`와 `/api/v1/admin/orders`도 인증 없이 호출된다.

validation도 실질적으로 꺼져 있다. request record에는 `@NotBlank`, `@Min`, `@Email`이 달려 있지만 controller의 `@RequestBody`에는 `@Valid`가 없다. 수동 재검증에서 아래 두 요청은 모두 `200`이었다.

```bash
curl -i -X POST http://127.0.0.1:18087/api/v1/admin/products \
  -H 'Content-Type: application/json' \
  -d '{"name":"","price":-1,"stock":0}'

curl -i -X POST http://127.0.0.1:18087/api/v1/cart/items \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"not-an-email","productId":2,"quantity":1}'
```

첫 번째는 invalid product row를 만들었고, 두 번째는 invalid email cart item을 그대로 저장했다. 즉 baseline capstone은 흐름 연결은 보여 주지만, admin/public separation이나 input integrity는 아직 거의 손대지 않았다.

## Phase 3. checkout은 stock decrement와 cart clear를 보여 주지만, payment/idempotency/concurrency는 아직 없다

`CommerceService.checkout()`은 이 capstone에서 가장 "커머스답게" 보이는 부분이다. cart item들을 읽고, 각 상품의 재고를 확인하고, 부족하면 실패시키고, 충분하면 stock을 줄인 뒤 `PLACED` order를 만들고 cart를 비운다.

```java
for (CartItemEntity item : items) {
  CommerceProductEntity product =
      productRepository
          .findById(item.getProductId())
          .orElseThrow(() -> new IllegalArgumentException("Product not found"));
  if (product.getStock() < item.getQuantity()) {
    throw new IllegalArgumentException("Not enough stock");
  }
  product.decrementStock(item.getQuantity());
  totalQuantity += item.getQuantity();
}
orderRepository.save(new OrderEntity(customerEmail, totalQuantity, "PLACED"));
cartItemRepository.deleteByCustomerEmail(customerEmail);
```

수동 재검증에서도 이 흐름은 확인됐다.

- valid product `stock=4` 생성
- cart에 1개 추가
- checkout 성공 -> `{"status":"PLACED","totalQuantity":1}`
- 이후 `GET /api/v1/products`에서 same product stock이 `3`
- 같은 고객으로 다시 checkout -> `400 "Cart is empty"`

이건 baseline capstone으로서는 꽤 중요한 기준선이다. 다만 동시에 무엇이 없는지도 뚜렷하다.

- payment 단계 없음
- idempotency key 없음
- outbox/event emission 없음
- product에 `version` 컬럼과 `@Version` 필드는 있지만 checkout에서 optimistic locking contract로 surface에 드러나지 않음

즉 "주문은 된다"와 "주문이 production-grade checkout이다" 사이에는 아직 큰 거리가 있다. 특히 주문 주체가 auth context가 아니라 request param 문자열에 의해 결정된다는 점까지 감안하면, 이 흐름은 commerce semantics의 첫 골격이지 authenticated commerce contract의 완성형은 아니다.

## Phase 4. 인프라 dependency는 compose에 많지만 runtime path는 그 무게를 아직 거의 쓰지 않는다

`compose.yaml`에는 postgres, redis, mailpit, redpanda가 모두 들어 있다. 하지만 실제 baseline 코드 경로를 보면 redis, mail, kafka/redpanda는 직접 쓰이지 않는다. 2026-03-14 `bootRun`도 이 서비스들을 띄우지 않은 채 잘 올라왔다.

또 compose에는 이전 lab에서 복사된 흔적도 남아 있다. `postgres` 기본 DB 이름이 `${POSTGRES_DB:-a_auth_lab}`로 잡혀 있어 현재 capstone 이름과 맞지 않는다. 즉 이 환경은 "통합형 stack 소개"에는 가깝지만, 도메인에 꼭 맞게 다듬어진 final infra contract는 아니다.

운영 표면도 완성본은 아니다. `GET /actuator/health`는 수동 재검증에서 `503 DOWN`이었고, backend-spring ops lab과 비슷하게 메일/레디스 같은 외부 dependency health가 전체 status에 영향을 주는 상태다. 반면 커머스 API 자체는 정상 동작했다. 이 역시 baseline 성격을 잘 보여 준다. 도메인 flow와 운영 완성도는 아직 함께 올라가지 않았다.

## Phase 5. 이번 Todo는 "통합된다"와 "아직 얕다"를 같이 검증했다

이번 검증은 모두 2026-03-14에 다시 실행했다. 로컬 JRE가 없어서 host `make` 대신 `eclipse-temurin:21-jdk` 컨테이너를 사용했다.

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

세 명령 모두 `BUILD SUCCESSFUL`이었다. 이후 `bootRun`을 18087 포트로 띄워 fake login, unauthenticated `/me`, invalid admin product create, invalid cart item create, valid cart-to-order flow, stock decrement, second checkout failure, admin order list, actuator health 상태를 직접 확인했다.

그래서 지금의 `commerce-backend`를 가장 정확하게 요약하면 이렇다. 이 capstone은 auth, catalog, cart, order를 하나의 baseline commerce flow로 묶는 데는 성공했다. 하지만 그 성공은 deliberately thin하다. fake auth, public admin endpoints, validation 미적용, payment 부재, async 연동 부재, infra copy 흔적이 그대로 남아 있다. 바로 이 얕음 때문에 `commerce-backend-v2`가 왜 필요한지가 소스와 실행 결과에서 자연스럽게 드러난다.
