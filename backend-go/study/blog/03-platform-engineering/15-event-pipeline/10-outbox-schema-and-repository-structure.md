# 15 Event Pipeline Structure

## 이 글이 답할 질문

- DB write와 Kafka publish 사이의 정합성 문제를 outbox로 해결해야 한다.
- purchase API와 event delivery를 느슨하게 연결하되, outbox로 원자성을 지키는 구조를 선택했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/15-event-pipeline` 안에서 `10-outbox-schema-and-repository.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 인프라 구성 -> 2단계: 스키마 적용 -> 3단계: Go 모듈 초기화 -> 4단계: Outbox 패키지 구현
- 세션 본문: `cockroachdb/cockroach:v25.3.3, redpandadata/redpanda:v24.3.5, jackc/pgx/v5, segmentio/kafka-go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/outbox/repository.go`
- 코드 앵커 2: `solution/go/schema.sql`
- 코드 설명 초점: 이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.
- 개념 설명: outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.
- 마지막 단락: 다음 글에서는 `20-relay-consumer-and-delivery-boundary.md`에서 이어지는 경계를 다룬다.
