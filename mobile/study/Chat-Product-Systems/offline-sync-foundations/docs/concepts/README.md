# Concepts

- outbox는 optimistic UI의 기록이 아니라 재전송 가능한 mutation log다.
- retry와 DLQ를 분리하면 실패를 숨기지 않고 다룰 수 있다.
- conflict merge rule은 간단할수록 재현 테스트가 쉬워진다.
