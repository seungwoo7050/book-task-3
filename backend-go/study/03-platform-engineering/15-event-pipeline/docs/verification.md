# Verification

## Commands

```bash
cd 03-platform-engineering/15-event-pipeline
make -C problem build
make -C problem test

cd 03-platform-engineering/15-event-pipeline/go
make repro
```

## Result

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd go && make repro`가 통과했다.
  - CockroachDB + Redpanda compose 기동
  - `schema.sql` 적용
  - outbox -> relay -> Kafka -> consumer -> `processed_events`까지 DB+broker e2e 검증
  - consumer 재시작 뒤 동일 `event_id` 재전송 시 durable dedupe 검증
