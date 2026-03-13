# baseline의 증명 범위와 일부러 남겨 둔 빈칸

baseline capstone의 가치는 "돌아간다"에서 끝나지 않는다. 어떤 흐름까지는 지금 당장 증명했고, 어떤 축은 다음 버전으로 넘겼는지를 정확히 남겨야 한다. `commerce-backend`는 그 점에서 솔직하다. macOS + VSCode 통합 터미널에서 재실행한 `make test`와 기존 검증 보고를 붙여 보면, 이 프로젝트는 product/cart/order baseline을 끝까지 증명하지만 payment와 richer auth는 의도적으로 비워 둔다.

## Phase 3

### Session 1

- 당시 목표:
  - baseline flow가 end-to-end로 실제 이어지는지 검증한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/CommerceApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - contract-level login -> admin product -> customer cart -> order -> admin order list만 고정해도 baseline 목적은 충분히 설명된다.
- 실제 진행:
  - 로그인으로 access token shape를 만들고, 상품 생성과 목록 조회, 장바구니 추가, 주문 생성, 주문 목록 조회를 한 테스트로 연결했다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
- 같은 재실행에서 `make test`는 `BUILD SUCCESSFUL`로 끝났다.
- `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.

핵심 코드:

```java
mockMvc
    .perform(post("/api/v1/orders").param("customerEmail", "buyer@example.com"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.status").value("PLACED"));
```

왜 이 코드가 중요했는가:

- baseline의 checkout이 실제 사용자 흐름에서 order creation까지 이어진다는 사실을 가장 직접적으로 보여 준다.

새로 배운 것:

- baseline capstone은 성공한 흐름 하나를 끝까지 보여 주는 것만으로도 큰 의미가 있다. 중요한 건 그 성공이 어디서 멈추는지까지 같이 적는 일이다.

## 남겨 둔 빈칸

- persisted auth는 아직 없다.
- payment flow와 idempotency는 아직 없다.
- outbox -> Kafka -> notification 연결은 아직 없다.

CLI:

```bash
make lint
make test
make smoke
```

검증 신호:

- 루트 `docs/verification-report.md`는 이 baseline이 lint/test/smoke/Compose health까지 통과한 상태로 기록돼 있다.

핵심 코드:

```java
return new OrderResponse(
    order.getId(), order.getCustomerEmail(), order.getStatus(), order.getTotalQuantity());
```

왜 이 코드가 중요했는가:

- 응답이 단순한 만큼, baseline이 어디까지 설명하고 어디서 멈추는지도 분명하다. 이 단순함 자체가 v2가 채워야 할 공백의 지도다.

다음:

- persisted auth, inventory reservation, payment idempotency, outbox/Kafka를 `commerce-backend-v2`에서 닫는다.
