# E-event-messaging-lab structure outline

## 글 목표

- Kafka 시연보다 outbox boundary를 먼저 설명하는 흐름으로 복원한다.
- macOS + VSCode 통합 터미널 기준의 검증 흔적을 유지한다.

## 글 순서

1. outbox lifecycle을 먼저 고정한 단계
2. `PENDING -> PUBLISHED` 전이를 schema와 서비스 코드에 연결한 단계
3. worker와 runtime guarantee를 뒤로 미룬 이유를 닫는 단계

## 반드시 넣을 코드 앵커

- `EventMessagingApiTest.outboxEventLifecycleWorks()`
- `V2__outbox_events.sql`
- `EventMessagingService.publishPending()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- outbox는 메시징 기술이 아니라 persistence boundary다.
- 이벤트 생성과 publish는 분리될 때 설명력이 생긴다.
