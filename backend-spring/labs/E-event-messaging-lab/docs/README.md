# E-event-messaging-lab Notes

## Implemented now

- outbox table and JPA entity
- order event creation endpoint
- pending-to-published lifecycle demonstration
- Redpanda-backed Compose stack

## Important simplifications

- no long-running publisher worker is attached yet
- Kafka delivery is represented by state transition rather than a real topic consumer contract
- DLQ and retry policy are conceptual only

## Next improvements

- add scheduled publisher job
- publish real Kafka records and consume them in tests
- store delivery failure metadata for replay decisions
