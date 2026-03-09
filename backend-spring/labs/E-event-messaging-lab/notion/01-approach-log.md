# Approach Log

## Options considered

- Kafka API만 바로 쓰는 방식은 빠르지만 DB와 메시지 브로커의 경계가 흐려진다.
- outbox를 먼저 두는 방식은 구현이 더 많지만 트랜잭션 이야기를 할 수 있다.
- DLQ까지 한 번에 넣는 방식은 좋지만 scaffold 범위를 넘어선다.

## Chosen direction

- package structure:
  - outbox entity, event creation, publish-oriented flow 중심
- persistence choice:
  - outbox row를 durable handoff boundary로 둔다
- security boundary:
  - 이 랩은 auth보다 messaging reliability에 집중한다
- integration style:
  - Redpanda-backed Compose stack을 두되, long-running publisher는 후속 개선으로 남긴다
- why this is the right choice:
  - Spring 메시징 패턴의 핵심을 작은 범위에서 설명하기 좋다

## Rejected ideas

- direct publish only 방식은 폐기했다
- full retry/DLQ orchestration을 scaffold 필수로 두는 방식은 폐기했다

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/E-event-messaging-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/E-event-messaging-lab/docs/README.md`

