# References

## 1. Legacy Outbox Notes

- Title: legacy `outbox-pattern.md`
- Source workspace path (not included in this public repo): legacy/03-platform-engineering/07-event-pipeline/docs/outbox-pattern.md
- Checked date: 2026-03-07
- Why: outbox 과제의 핵심 trade-off를 다시 확인했다.
- Learned: 핵심은 Kafka 사용법 자체보다 dual-write를 피하는 사고방식이다.
- Effect: docs에서 broker 세부 설정보다 outbox/relay/consumer 경계를 먼저 설명했다.

## 2. Legacy Consumer Notes

- Title: legacy `consumer.md`
- Source workspace path (not included in this public repo): legacy/03-platform-engineering/07-event-pipeline/docs/consumer.md
- Checked date: 2026-03-07
- Why: at-least-once와 idempotency 설명을 보강하기 위해 확인했다.
- Learned: consumer 설계는 “중복이 올 수 있다”는 가정을 기본값으로 잡아야 한다.
- Effect: verification 문서에도 consumer idempotency 테스트를 강조했다.

