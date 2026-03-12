# 문제 정의

구매 이벤트를 DB transaction과 Kafka publish 사이에서 정합성을 잃지 않도록 outbox pattern으로 구현한다.

## 성공 기준

- purchase transaction 안에서 outbox row를 함께 기록한다.
- relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다.
- aggregate_id 기준 ordering을 유지한다.
- consumer가 idempotent하게 이벤트를 처리한다.
- HTTP purchase -> relay -> consumer 흐름이 연결된다.

## 제공 자료와 출처

- legacy `03-platform-engineering/07-event-pipeline` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 세부 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem build`
- `make -C problem test`
- `cd solution/go && make repro`

## 제외 범위

- 복잡한 orchestration
- 대규모 production Kafka tuning
