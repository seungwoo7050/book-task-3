# commerce-backend-v2 series map

baseline capstone을 같은 도메인 위에서 더 깊은 대표 결과물로 끌어올린 과정을 보여 주는 시리즈다. 기준 환경은 macOS + VSCode 통합 터미널이며, `./gradlew`, `make`, Compose, Testcontainers 흐름을 함께 따른다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md): persisted auth, cart/order/payment, outbox/Kafka, Redis 검증이 어떤 순서로 같은 modular monolith 안에 붙었는지 따라간다.

## 이 시리즈가 답하는 질문

- 왜 도메인을 바꾸지 않고 같은 커머스 문제를 더 깊게 풀었는가
- 어떤 invariant가 baseline보다 더 엄격해졌는가
- Redis와 Kafka는 어디에만 쓰이고 어떻게 검증됐는가
