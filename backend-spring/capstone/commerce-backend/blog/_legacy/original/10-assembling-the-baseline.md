# 얕더라도 끝까지 이어지는 커머스 baseline을 먼저 만든다

`commerce-backend`는 일부 기능이 얕다는 사실을 숨기지 않는다. 오히려 그 얕음을 의도적으로 남겨 두고, 랩에서 배운 조각들이 한 커머스 도메인 안에서 어디서 만나는지 먼저 보여 준다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면 이 baseline이 왜 중요한지 더 잘 보인다. auth가 contract-level이어도, product -> cart -> order가 끊기지 않고 이어지면 v2가 어디서 깊어져야 하는지 비교할 수 있기 때문이다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 baseline capstone의 역할을 먼저 고정한다.
- `CommerceAuthController`가 아주 얕은 auth surface를 만든다.
- `CommerceService`와 `CommerceController`가 product, cart, order를 한 서비스로 묶는다.
- `CommerceApiTest`가 baseline의 닫힌 범위를 끝까지 검증한다.

## Phase 1

### Session 1

- 당시 목표:
  - 이 프로젝트를 최종 답이 아닌 baseline으로 정의한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 첫 통합 캡스톤은 모든 세부 구현을 넣기보다, 도메인 조합이 어떤 모양인지 설명할 수 있는 기준선이 되는 편이 낫다.
- 실제 진행:
  - auth, catalog, cart, order surface를 baseline scope로 고정하고, payment와 완전한 eventing은 다음 버전으로 넘겼다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- docs가 baseline의 역할과 deliberately shallow한 영역을 분리해서 적고 있다.

핵심 코드:

```java
@PostMapping("/auth/login")
public Map<String, String> login(@RequestParam String email) {
  return Map.of("accessToken", "commerce-access-token", "email", email);
}
```

왜 이 코드가 중요했는가:

- baseline auth가 얼마나 얕은지 이 코드 한 줄이 정확히 보여 준다. 여기서 숨기지 않고 드러냈기 때문에, v2에서 persisted auth를 왜 추가했는지도 비교 설명이 가능해진다.

새로 배운 것:

- baseline을 잘 만들려면 약점도 구조적으로 남겨 둬야 한다. 그래야 다음 버전의 개선 축이 흐려지지 않는다.

다음:

- 얕은 auth surface 위에 product, cart, order를 실제로 조합한다.

## Phase 2

### Session 1

- 당시 목표:
  - 커머스 핵심 흐름을 한 서비스 안에서 먼저 연결한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/commerce/application/CommerceService.java`
  - `spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceController.java`
- 처음 가설:
  - baseline에서는 모듈 간 분리를 지나치게 세분화하기보다, 상품 생성/조회와 cart/order 이동이 같은 코드베이스에서 닫히는지를 먼저 보여 주는 편이 낫다.
- 실제 진행:
  - admin product 생성, public product listing, cart item 추가, checkout, admin order listing을 `CommerceService`와 `CommerceController`에 배치했다.
  - checkout에서는 cart item을 읽어 stock을 줄이고 `PLACED` order를 저장한 뒤 cart를 비운다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
OrderEntity order =
    orderRepository.save(new OrderEntity(customerEmail, totalQuantity, "PLACED"));
cartItemRepository.deleteByCustomerEmail(customerEmail);
```

왜 이 코드가 중요했는가:

- baseline의 checkout은 복잡하지 않지만, product stock과 cart cleanup이 한 트랜잭션 흐름 안에서 만난다는 사실을 분명하게 보여 준다.

새로 배운 것:

- 통합 캡스톤의 첫 번째 성과는 고급 기술이 아니라, 서로 다른 aggregate가 한 주문 흐름에서 실제로 만나는 지점을 코드로 드러내는 것이다.

다음:

- 이 baseline이 실제 API 흐름으로 닫히는지 테스트로 확인한다.
