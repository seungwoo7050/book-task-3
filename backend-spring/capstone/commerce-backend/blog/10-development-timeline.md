# commerce-backend: 여러 랩의 학습을 비교 가능한 baseline 커머스로 묶은 과정

`commerce-backend`는 이 트랙의 첫 통합 캡스톤이다. 그래서 목표도 모든 기능을 깊게 구현하는 데 있지 않았다. 앞선 랩에서 배운 인증, 카탈로그, 장바구니, 주문을 하나의 도메인 안에서 다시 조합하고, 다음 버전과 비교할 기준선을 남기는 쪽이 더 중요했다.

구현 순서는 단순하다. `problem/README.md`에서 이 캡스톤의 역할을 baseline으로 고정하고, `CommerceApiTest`로 auth/catalog/cart/order 흐름을 한 번에 묶었다. 그다음 `V2__commerce.sql`, `CommerceService`, `CommerceAuthController`로 modular monolith baseline을 만들고, 마지막에 docs와 검증 기록으로 일부러 남겨 둔 빈칸을 정리했다.

## Phase 1. 기능 깊이보다 통합 surface를 먼저 고정했다

첫 통합 캡스톤에서 제일 중요한 질문은 "무엇을 한 번에 묶을 것인가"다. [`CommerceApiTest`](../spring/src/test/java/com/webpong/study2/app/CommerceApiTest.java)는 로그인 뒤 상품을 만들고, 목록을 보고, 장바구니에 담고, 주문을 만들고, 관리자 주문 목록에서 다시 확인하는 흐름을 한 테스트에 넣는다.

```java
mockMvc.perform(post("/api/v1/auth/login").param("email", "buyer@example.com"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.accessToken").exists());

mockMvc.perform(post("/api/v1/orders").param("customerEmail", "buyer@example.com"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.status").value("PLACED"));
```

왜 이 코드가 중요했는가. 이 시점의 캡스톤은 개별 랩의 내부 구현을 복제하는 게 아니라, 인증에서 주문까지 이어지는 사용자 여정을 하나의 코드베이스 안에서 끊기지 않게 보여 주는 편이 더 중요했기 때문이다.

CLI도 이 단계에서는 단순하다.

```bash
cd spring
make test
```

`2026-03-13` 테스트 XML 기준으로 `CommerceApiTest` 1개 테스트와 `HealthApiTest` 2개 테스트가 모두 통과했다. 통합 흐름과 health surface가 baseline 수준으로 이미 붙어 있다는 뜻이다.

여기서 새로 보인 개념은 첫 통합 캡스톤의 성공 기준이었다. 최종 기능 수보다, 여러 랩의 주제가 도메인 안에서 어떤 순서로 이어지는지를 보여 주는 편이 더 중요했다.

## Phase 2. auth는 얕게 두고 catalog, cart, order를 먼저 연결했다

baseline capstone이라는 정체성은 schema와 서비스 코드에서 더 선명해진다. [`V2__commerce.sql`](../spring/src/main/resources/db/migration/V2__commerce.sql)은 `commerce_products`, `commerce_cart_items`, `commerce_orders` 세 테이블만 두고, auth도 [`CommerceAuthController`](../spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceAuthController.java)에서 contract-level login과 `me` 조회로 가볍게 처리한다.

```java
@PostMapping("/auth/login")
public Map<String, String> login(@RequestParam String email) {
  return Map.of("accessToken", "commerce-access-token", "email", email);
}
```

실제 도메인 흐름은 [`CommerceService.checkout()`](../spring/src/main/java/com/webpong/study2/app/commerce/application/CommerceService.java) 쪽에서 더 잘 보인다.

```java
for (CartItemEntity item : items) {
  CommerceProductEntity product =
      productRepository.findById(item.getProductId())
          .orElseThrow(() -> new IllegalArgumentException("Product not found"));
  if (product.getStock() < item.getQuantity()) {
    throw new IllegalArgumentException("Not enough stock");
  }
  product.decrementStock(item.getQuantity());
  totalQuantity += item.getQuantity();
}
```

왜 이 코드가 중요했는가. 여기서 이 캡스톤의 위치가 결정된다. auth는 아직 얕고 payment도 없지만, 상품 조회에서 주문 생성까지 이어지는 핵심 커머스 흐름은 이미 modular monolith 안에 들어와 있다. baseline의 역할은 바로 이 정도 깊이를 비교 기준으로 남기는 데 있다.

이 단계의 CLI는 smoke와 Compose로 올라간다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification-report.md`는 `2026-03-09`에 lint, test, smoke, Compose health 확인이 모두 통과했다고 남긴다. 이 baseline이 코드 스냅샷이 아니라 다시 띄워 볼 수 있는 워크스페이스라는 뜻이다.

여기서 배운 건 modular monolith baseline의 가치였다. 랩 코드를 그대로 가져오는 대신 같은 문제를 새 도메인 안에서 다시 풀어 보니, 이미 굳은 경계와 아직 비어 있는 경계가 더 쉽게 보였다.

## Phase 3. 의도적으로 얕은 부분이 있어야 v2가 선명해졌다

이 프로젝트를 진짜 이해하려면 무엇이 없는지도 같이 봐야 한다. [`docs/README.md`](../docs/README.md)는 auth가 contract-level 중심이고, payment는 아직 없고, notification/event consumer도 완전히 연결되지 않았다고 분명히 적는다. baseline capstone이기 때문에 가능한 정직함이다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 아래처럼 읽힌다.

- `2026-03-13` 기준 테스트 XML 4개 suite, 총 5개 테스트, 실패 0
- `2026-03-09` 검증 보고서 기준 lint, test, smoke, Compose health 확인 통과
- docs에 auth depth 부족, payment 없음, notification/event consumer 미완이 명시돼 있음

이 버전이 남긴 가장 중요한 배움은 baseline도 결과물이라는 점이다. 일부러 남겨 둔 빈칸이 있어야 다음 버전이 무엇을 더 풀었는지 비교할 수 있다. 그래서 `commerce-backend-v2`는 경쟁작이 아니라, 같은 도메인 위에서 깊이를 올린 다음 단계로 읽힌다.
