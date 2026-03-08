# Queue Replay Model

- create mutation은 먼저 local task와 queue job을 만든다.
- reconnect 시 pending job을 oldest-first로 flush한다.
- 동일 idempotency key는 서버가 한 번만 수용한다.
- max retry를 넘긴 job은 DLQ로 분리한다.
