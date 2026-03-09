# Retrospective

## What improved

- cache invalidation과 concurrency를 inventory 시나리오로 묶은 판단이 좋았다.
- idempotency key를 같은 랩에 둔 것이 duplicate protection 이야기를 쉽게 만들었다.
- verification report에 test cache 전략을 밝힌 점이 저장소 정직성을 높였다.

## What is still weak

- real Redis cache assertion이 적다.
- distributed lock은 아직 없다.
- reservation logic이 in-process synchronization에 가깝다.

## What to revisit

- Redisson lock을 붙이고 conflict test를 추가할 수 있다.
- idempotency persistence를 더 명확히 분리할 수 있다.
- capstone payment idempotency와 연계 메모를 만들 수 있다.

