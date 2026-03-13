# commerce-backend Evidence Ledger

- 복원 기준:
  - `problem/README.md`, `docs/README.md`, `CommerceAuthController`, `CommerceService`, `CommerceController`, `CommerceApiTest`, `2026-03-13` 재실행 CLI, `2026-03-09` 검증 보고를 근거로 chronology를 세웠다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어서 `isolate-and-rewrite` 시 격리 대상은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 이 캡스톤을 "최종 답"이 아니라 v2와 비교할 baseline으로 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 처음 통합 캡스톤은 모든 깊이를 다 넣기보다, 랩들을 하나의 커머스 도메인으로 다시 묶는 기준선을 만드는 편이 낫다.
- 실제 조치:
  - modular monolith baseline, auth/catalog/cart/order surface, 얕게 남긴 영역을 문서에서 먼저 분리했다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - docs가 baseline 역할과 v2의 비교 기준이라는 점을 명시한다.
- 핵심 코드 앵커:
  - `CommerceAuthController`, `CommerceService`, `CommerceApiTest`.
- 새로 배운 것:
  - baseline의 가치는 미완성의 양이 아니라, 무엇을 일부러 남겼는지 분명하게 말할 수 있다는 데 있다.
- 다음:
  - 상품, 장바구니, 주문을 한 서비스로 먼저 묶는다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - auth/catalog/cart/order를 하나의 modular monolith baseline으로 조합한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceAuthController.java`
  - `spring/src/main/java/com/webpong/study2/app/commerce/application/CommerceService.java`
  - `spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceController.java`
  - `spring/src/main/resources/db/migration/V2__commerce.sql`
- 처음 가설:
  - baseline에서는 persisted auth보다 "한 코드베이스에서 상품, 장바구니, 주문이 한 번에 이어진다"는 사실을 먼저 증명하는 편이 낫다.
- 실제 조치:
  - auth는 contract-level login/me endpoint로만 두었다.
  - `CommerceService`는 product 생성/조회, cart item 추가, checkout, admin order listing을 한 서비스에 모았다.
  - checkout은 cart item을 읽어 stock을 줄이고 order를 `PLACED`로 저장한 뒤 cart를 비운다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

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
```

- 새로 배운 것:
  - baseline capstone에서는 깊은 모듈 분리보다 "하나의 checkout이 어떤 aggregate들을 동시에 건드리는가"를 먼저 보여 주는 편이 더 유용하다.
- 다음:
  - end-to-end API 테스트로 baseline의 닫힌 범위와 남긴 공백을 같이 확인한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - 간단한 auth surface부터 product/cart/order까지 한 흐름으로 검증한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/CommerceApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - contract-level login -> admin product -> customer cart -> order -> admin order list 순서만 고정해도 baseline 목적은 충분히 증명된다.
- 실제 조치:
  - `CommerceApiTest`에서 로그인, 상품 생성, 상품 목록, 장바구니 추가, 주문 생성, 주문 목록 조회를 한 흐름으로 묶었다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
  - `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.
- 핵심 코드 앵커:

```java
@PostMapping("/auth/login")
public Map<String, String> login(@RequestParam String email) {
  return Map.of("accessToken", "commerce-access-token", "email", email);
}
```

- 새로 배운 것:
  - baseline에서는 인증이 깊지 않아도 괜찮다. 대신 그 얕음을 숨기지 않고, 왜 v2에서 persisted auth가 필요해지는지 비교 기준으로 남기는 편이 더 중요하다.
- 다음:
  - payment, persisted auth, outbox/Kafka, richer notification은 v2에서 다룬다.
