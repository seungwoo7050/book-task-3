# Offline Queue And Replay Model

이 과제의 핵심은 오프라인에서도 작업을 잃지 않고, 다시 연결됐을 때 서버 상태와 수렴하는 흐름을 구현하는 것이다.

## Queue Rules

- 모든 mutation은 idempotency key를 가진 outbox job으로 생성한다.
- 성공 시 `synced`, 재시도 가능 실패는 `pending`, 최대 재시도 초과는 `failed`로 둔다.
- `failed`는 DLQ와 같은 의미로 다루고 수동 retry를 제공한다.

## Replay Rules

- websocket은 `lastEventId`부터 다시 연결한다.
- missed event가 replay된 뒤 live stream으로 전환된다.
- outbox flush와 stream replay는 같은 계약을 공유하지만 서로 다른 책임이다.
  - outbox: 내가 보낸 작업 복구
  - replay: 내가 놓친 서버 변경 복구
