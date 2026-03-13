# F-cache-concurrency-lab series map

cache, idempotency, inventory 경합을 한 시나리오로 묶어 읽게 만드는 시리즈다. 기준 환경은 macOS + VSCode 통합 터미널이다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md): reservation 중복 처리, inventory cache, in-process concurrency 제어가 어떤 순서로 붙었는지 따라간다.

## 이 시리즈가 답하는 질문

- 왜 Redis와 distributed lock을 바로 도입하지 않았는가
- idempotency와 cache를 함께 보면 무엇이 보이는가
- 다음 확장 지점은 어디인가
