# E-event-messaging-lab series map

request-response 밖으로 나가는 사실을 outbox boundary로 먼저 설명하는 시리즈다. 기준 환경은 macOS + VSCode 통합 터미널이다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md): order event 생성과 outbox publish lifecycle이 어떤 순서로 굳어졌는지 따라간다.

## 이 시리즈가 답하는 질문

- 왜 Kafka consumer보다 outbox table이 먼저 등장하는가
- `PENDING -> PUBLISHED` 전이는 무엇을 설명해 주는가
- 아직 남겨 둔 messaging 범위는 무엇인가
