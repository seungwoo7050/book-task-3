# commerce-backend evidence ledger

- 작성 기준일: 2026-03-14
- 복원 원칙: 기존 blog 본문은 입력 근거에서 제외하고, source, tests, config, 재실행 결과만 사용했다.
- 핵심 근거: `problem/README.md`, `docs/README.md`, `spring/Makefile`, `CommerceAuthController.java`, `CommerceController.java`, `CommerceService.java`, `CommerceProductEntity.java`, `V2__commerce.sql`, `CommerceApiTest.java`, `HealthApiTest.java`, `LabInfoApiSmokeTest.java`, `spring/compose.yaml`

## Phase 1. 통합 user journey와 auth depth 확인

- 목표: 첫 capstone이 실제로 어떤 통합 흐름을 baseline으로 삼는지 확인한다.
- 확인 파일:
  - `spring/src/test/java/com/webpong/study2/app/CommerceApiTest.java`
  - `spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceAuthController.java`
- 확인 결과:
  - 로그인 -> 상품 생성/조회 -> 장바구니 -> 주문 -> 관리자 주문 조회가 한 테스트에 묶여 있다.
  - login은 고정 `commerce-access-token`을 반환한다.
  - `/me`는 인증 없이 query param `email`만 echo한다.
  - cart add와 checkout도 authenticated principal이 아니라 request body/query param의 `customerEmail`을 그대로 사용한다.

## Phase 2. catalog/cart/order와 validation 공백 확인

- 목표: baseline commerce flow가 실제로 어디까지 유효한 contract를 가지는지 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/commerce/api/CommerceController.java`
  - `spring/src/main/java/com/webpong/study2/app/commerce/application/CommerceService.java`
  - `spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java`
- 확인 결과:
  - `/api/v1/admin/**`도 포함해 `/api/v1/**` 전체가 public이다.
  - request DTO validation annotation은 `@Valid` 없이 선언만 돼 있다.
  - invalid product와 invalid cart email이 실제로 `200`으로 저장된다.
- 핵심 앵커:

```java
auth.requestMatchers("/api/v1/**", "/v3/api-docs/**", "/swagger-ui/**")
    .permitAll()
```

## Phase 3. checkout semantics 확인

- 목표: capstone의 실제 도메인 핵심이 어디까지 구현되었는지 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/commerce/application/CommerceService.java`
  - `spring/src/main/java/com/webpong/study2/app/commerce/domain/CommerceProductEntity.java`
- 확인 결과:
  - checkout은 cart item을 읽고 stock을 감소시키고 order를 `PLACED`로 저장한 뒤 cart를 비운다.
  - second checkout은 `Cart is empty`로 실패한다.
  - `commerce_products`에는 `version` 컬럼이 있지만, checkout surface에서 optimistic locking contract는 드러나지 않는다.

## Phase 4. 2026-03-14 재실행 검증

- lint:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL in 3m 31s`

- test:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 결과: `BUILD SUCCESSFUL in 2m 26s`

- smoke:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL in 2m 31s`

- manual boot run:

```bash
docker run --rm -u $(id -u):$(id -g) -p 18087:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

- manual HTTP checks:
  - login -> fixed token response
  - `/api/v1/me?email=buyer@example.com` -> unauthenticated `CUSTOMER` echo
  - invalid admin product create -> `200`, invalid row persisted
  - invalid cart email -> `200`, invalid cart row persisted
  - valid product stock `4` -> checkout after one cart item -> order `PLACED`, product stock `3`
  - second checkout same customer -> `400`, `detail="Cart is empty"`
  - `/api/v1/admin/orders` -> unauthenticated order list access
  - `/actuator/health` -> `503 DOWN`

## 이번 Todo의 결론

- 이 capstone은 통합 commerce flow 기준선으로는 충분하지만, final commerce backend라고 읽으면 안 된다.
- 문서에 반드시 남겨야 할 현재 한계:
  - fake auth and public admin surface
  - login narrative와 실제 downstream identity enforcement의 분리
  - validation 미적용
  - payment/idempotency/async integration 부재
  - compose/runtime에 남은 copy-and-paste infra 흔적
