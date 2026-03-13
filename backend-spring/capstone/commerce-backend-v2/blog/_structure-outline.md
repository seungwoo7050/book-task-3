# commerce-backend-v2 structure outline

## 글 목표

- 같은 도메인을 더 깊게 판 대표 capstone의 구현 순서를 복원한다.
- macOS + VSCode 통합 터미널 기준의 `./gradlew`, `make`, Compose, Testcontainers 흐름을 유지한다.

## 글 순서

1. persisted auth와 end-to-end commerce flow를 먼저 고정한 단계
2. checkout, payment, outbox를 invariant 중심으로 묶은 단계
3. Redis, Kafka, Testcontainers 검증으로 대표 결과물로 닫은 단계

## 반드시 넣을 코드 앵커

- `CommercePortfolioApiTest.adminCatalogCustomerCheckoutAndPaymentFlowWorks()`
- `OrderService.checkout()`
- `PaymentService.confirmMockPayment()`
- `OutboxPublisher.publishPending()`

## 반드시 넣을 CLI

```bash
cd spring
./gradlew testClasses --no-daemon
make lint
make test
make smoke
docker compose up --build
```

## 핵심 개념

- 대표 결과물의 깊이는 같은 문제를 더 엄격한 규칙으로 다시 푸는 데서 나온다.
- Redis와 Kafka는 실제 검증과 연결될 때만 설득력이 생긴다.
