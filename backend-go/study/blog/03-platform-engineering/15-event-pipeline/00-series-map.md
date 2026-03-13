# 15 Event Pipeline Series Map

`03-platform-engineering/15-event-pipeline`는 outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다.

## 이 시리즈가 복원하는 것

- 시작점: DB write와 Kafka publish 사이의 정합성 문제를 outbox로 해결해야 한다.
- 구현 축: outbox repository, relay, consumer, CLI entrypoints를 `solution/go`에 구현했다.
- 검증 축: 2026-03-08 기준 `make -C problem build`가 통과했다.
- 글 수: 3편

## 읽는 순서

- [10-outbox-schema-and-repository.md](10-outbox-schema-and-repository.md)
- [20-relay-consumer-and-delivery-boundary.md](20-relay-consumer-and-delivery-boundary.md)
- [30-repro-and-e2e-proof.md](30-repro-and-e2e-proof.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
