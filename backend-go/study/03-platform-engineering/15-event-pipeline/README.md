# 15 Event Pipeline

## 한 줄 요약

outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다.

## 이 프로젝트가 푸는 문제

- DB write와 Kafka publish 사이의 정합성 문제를 outbox로 해결해야 한다.
- relay process와 consumer를 따로 구현해야 한다.
- idempotent consumer와 ordering 기준을 설명해야 한다.

## 내가 만든 답

- outbox repository, relay, consumer, CLI entrypoints를 `solution/go`에 구현했다.
- aggregate_id를 기준으로 ordering을 맞추고, consumer는 processed event tracking으로 중복 처리를 막는다.
- runtime repro를 통해 DB, relay, consumer를 한 번에 재현할 수 있게 했다.

## 핵심 설계 선택

- purchase API와 event delivery를 느슨하게 연결하되, outbox로 원자성을 지키는 구조를 선택했다.
- consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.

## 검증

- `make -C problem build`
- `make -C problem test`
- `cd solution/go && make repro`

## 제외 범위

- 실제 대규모 운영 Kafka 설정
- 복잡한 saga orchestration

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/03-platform-engineering/07-event-pipeline (`legacy/03-platform-engineering/07-event-pipeline/README.md`, public repo에는 미포함)
