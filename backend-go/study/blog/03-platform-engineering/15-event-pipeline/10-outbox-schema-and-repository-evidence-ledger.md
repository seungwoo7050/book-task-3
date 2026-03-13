# 15 Event Pipeline Evidence Ledger

## 10 outbox-schema-and-repository

- 시간 표지: 1단계: 인프라 구성 -> 2단계: 스키마 적용 -> 3단계: Go 모듈 초기화 -> 4단계: Outbox 패키지 구현
- 당시 목표: DB write와 Kafka publish 사이의 정합성 문제를 outbox로 해결해야 한다.
- 변경 단위: `cockroachdb/cockroach:v25.3.3`, `redpandadata/redpanda:v24.3.5`, `jackc/pgx/v5`, `segmentio/kafka-go`
- 처음 가설: purchase API와 event delivery를 느슨하게 연결하되, outbox로 원자성을 지키는 구조를 선택했다.
- 실제 조치: 두 서비스 실행: **CockroachDB**: `cockroachdb/cockroach:v25.3.3`, 포트 26258 (SQL), 8082 (Admin UI) **Redpanda**: `redpandadata/redpanda:v24.3.5`, 포트 9093 (Kafka), 18082 (HTTP Proxy) 2개 테이블: `outbox`: 이벤트 아웃박스 (UUID PK, aggregate_type, event_type, payload JSONB, published_at nullable) `processed_events`: Consumer 멱등성 (event_id UUID PK, processed_at) Partial index: `idx_outbox_unpublished` — `WHERE published_at IS NULL` Go 1.24.0. 주요 의존성: `jackc/pgx/v5` v5.8.0 — CockroachDB 드라이버 `segmentio/kafka-go` v0.4.47 — Kafka 클라이언트 `InsertTx`는 `*sql.Tx`를 받아 트랜잭션 내 INSERT. 나머지는 `*sql.DB`로 독립 실행.

CLI:

```bash
cd 15-event-pipeline/go
docker compose -p event-pipeline up -d

# 준비 대기
make wait-db
# Redpanda는 healthcheck으로 자동 대기
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/outbox/repository.go`
- 새로 배운 것: outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.
- 다음: 다음 글에서는 `20-relay-consumer-and-delivery-boundary.md`에서 이어지는 경계를 다룬다.
