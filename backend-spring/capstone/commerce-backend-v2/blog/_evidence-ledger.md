# commerce-backend-v2 evidence ledger

- 복원 방식: 세밀한 개발 로그가 부족해 `Phase 1 -> Phase 3`으로 대표 결과물의 진화를 복원했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `docs/architecture-overview.md`, `docs/verification.md`, `spring/Makefile`, `spring/build.gradle.kts`, `AuthApiTest.java`, `CommercePortfolioApiTest.java`, `CommerceMessagingIntegrationTest.java`, `RedisCartStoreTest.java`, `OrderService.java`, `PaymentService.java`, `OutboxPublisher.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: baseline capstone이 남긴 얕은 부분을 같은 도메인에서 더 깊게 채운다.
- 변경 단위: `README.md`, `problem/README.md`, `docs/architecture-overview.md`, `AuthApiTest.java`, `CommercePortfolioApiTest.java`
- 처음 가설: 도메인을 바꾸거나 마이크로서비스로 쪼개야 더 강한 포트폴리오가 될 것 같았다.
- 실제 조치: 도메인은 유지하고 modular monolith를 유지한 채, persisted auth와 end-to-end commerce flow를 확장했다.
- CLI:

```bash
cd spring
./gradlew testClasses --no-daemon
make test
```

- 검증 신호: `AuthApiTest` 2개 테스트 통과, `CommercePortfolioApiTest` 1개 테스트 통과
- 핵심 코드 앵커: `AuthApiTest.registerLoginRefreshLogoutFlowWorks()`, `CommercePortfolioApiTest.adminCatalogCustomerCheckoutAndPaymentFlowWorks()`
- 새로 배운 것: 대표 결과물의 깊이는 같은 도메인에서 더 많은 경계와 상태 전이를 설명 가능하게 만드는 데서 나온다.
- 다음: order, payment, outbox를 invariant 중심으로 묶는다.

## Phase 2

- 당시 목표: checkout, payment, notification을 API 연결이 아니라 상태 전이와 idempotency 규칙으로 고정한다.
- 변경 단위: `OrderService.java`, `PaymentService.java`
- 처음 가설: 주문과 결제는 endpoint만 연결되면 포트폴리오 설명으로 충분할 수 있다고 봤다.
- 실제 조치: checkout에서 inventory reservation을 만들고, payment confirm에서 idempotency key, `PAID` 전이, outbox row 생성을 묶었다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `docs/verification.md` 기준 `2026-03-09` lint/test/smoke/Compose health 통과, `LabInfoApiSmokeTest` 1개 테스트 통과
- 핵심 코드 앵커: `OrderService.checkout()`, `PaymentService.confirmMockPayment()`
- 새로 배운 것: portfolio-grade commerce backend의 핵심은 기능 수보다 invariant와 replay 규칙을 어디서 강제하는가다.
- 다음: Redis, Kafka, Testcontainers를 실제 검증과 연결한다.

## Phase 3

- 당시 목표: Redis cart, outbox publisher, Kafka consumer를 buzzword가 아니라 검증 가능한 구현으로 닫는다.
- 변경 단위: `OutboxPublisher.java`, `CommerceMessagingIntegrationTest.java`, `RedisCartStoreTest.java`, `build.gradle.kts`, `docs/verification.md`
- 처음 가설: Redis와 Kafka는 README에 등장만 해도 충분히 강한 인상을 줄 수 있다고 생각했다.
- 실제 조치: `OutboxPublisher`를 scheduled publisher로 두고, Testcontainers로 order-paid event 소비를 검증했다. Redis cart는 직렬화/역직렬화 단위 테스트로 고정했다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 9개 suite, 총 11개 테스트, 실패 0
- 핵심 코드 앵커: `OutboxPublisher.publishPending()`, `CommerceMessagingIntegrationTest.orderPaidEventIsPublishedAndConsumed()`, `RedisCartStoreTest.cartPayloadCanBeSerializedAndReloaded()`
- 새로 배운 것: Redis와 Kafka는 어느 경계에만 쓰였고 그 경계가 테스트로 증명됐을 때만 설득력이 생긴다.
- 다음: live provider, real payment provider, live AWS provisioning은 여전히 다음 단계로 남는다.
