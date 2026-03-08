# Core Concepts

## 핵심 개념

- outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.
- relay는 outbox row를 브로커로 밀어내는 별도 프로세스다.
- consumer는 at-least-once 환경을 가정하고 중복 처리를 견뎌야 한다.
- message key를 aggregate id로 두면 같은 집계 단위의 순서를 지키기 쉽다.

## Trade-offs

- direct publish보다 outbox가 안전하지만 운영 컴포넌트가 하나 더 늘어난다.
- consumer idempotency 저장소가 없으면 중복 허용이 어렵다.

## 실패하기 쉬운 지점

- published 표시 시점이 publish 성공 전에 찍히면 이벤트 유실이 생긴다.
- relay와 consumer를 한 프로세스로 섞으면 책임 분리가 흐려진다.

