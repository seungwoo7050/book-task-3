# E-event-messaging-lab 시리즈 지도

`E-event-messaging-lab`은 이벤트를 "브로커를 쓴다"로 요약하지 않고, 도메인 변경 사실을 어떻게 기록하고 어떤 단계에서 publish로 넘길지 분리해 설명하는 랩이다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면 이 프로젝트의 중심은 Kafka 자체보다 outbox row의 상태 전이에 있다는 점이 더 잘 드러난다.

## 이 프로젝트가 푸는 문제

- order event를 outbox record로 먼저 남긴다.
- 이벤트 생성과 publish를 서로 다른 문제로 분리한다.
- Kafka/Redpanda가 왜 handoff boundary에서 등장하는지 설명한다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `OutboxEventEntity`, `EventMessagingService`, `EventMessagingController`
- `EventMessagingApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈의 중심 질문

- 이벤트를 왜 바로 브로커로 보내지 않고 outbox에 먼저 쓰는가
- `PENDING`과 `PUBLISHED` 상태는 어떤 설명력을 주는가
- 다음 단계에서 worker와 consumer는 어디에 붙는가
