# 15 Event Pipeline — Outbox Schema And Repository

`03-platform-engineering/15-event-pipeline`는 outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다. 이 글에서는 1단계: 인프라 구성 -> 2단계: 스키마 적용 -> 3단계: Go 모듈 초기화 -> 4단계: Outbox 패키지 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 인프라 구성
- 2단계: 스키마 적용
- 3단계: Go 모듈 초기화
- 4단계: Outbox 패키지 구현

## Day 1
### Session 1

- 당시 목표: DB write와 Kafka publish 사이의 정합성 문제를 outbox로 해결해야 한다.
- 변경 단위: `cockroachdb/cockroach:v25.3.3`, `redpandadata/redpanda:v24.3.5`, `jackc/pgx/v5`, `segmentio/kafka-go`
- 처음 가설: purchase API와 event delivery를 느슨하게 연결하되, outbox로 원자성을 지키는 구조를 선택했다.
- 실제 진행: 두 서비스 실행: **CockroachDB**: `cockroachdb/cockroach:v25.3.3`, 포트 26258 (SQL), 8082 (Admin UI) **Redpanda**: `redpandadata/redpanda:v24.3.5`, 포트 9093 (Kafka), 18082 (HTTP Proxy) 2개 테이블: `outbox`: 이벤트 아웃박스 (UUID PK, aggregate_type, event_type, payload JSONB, published_at nullable) `processed_events`: Consumer 멱등성 (event_id UUID PK, processed_at) Partial index: `idx_outbox_unpublished` — `WHERE published_at IS NULL` Go 1.24.0. 주요 의존성: `jackc/pgx/v5` v5.8.0 — CockroachDB 드라이버 `segmentio/kafka-go` v0.4.47 — Kafka 클라이언트 `InsertTx`는 `*sql.Tx`를 받아 트랜잭션 내 INSERT. 나머지는 `*sql.DB`로 독립 실행.

CLI:

```bash
cd 15-event-pipeline/go
docker compose -p event-pipeline up -d

# 준비 대기
make wait-db
# Redpanda는 healthcheck으로 자동 대기
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/outbox/repository.go`

```go
type Repository struct {
	DB *sql.DB
}

// NewRepository는 outbox 저장소를 생성한다.
func NewRepository(db *sql.DB) *Repository {
	return &Repository{DB: db}
}

// InsertTx는 기존 트랜잭션 안에서 outbox 이벤트를 기록한다.
func InsertTx(ctx context.Context, tx *sql.Tx, aggregateType, aggregateID, eventType string, payload interface{}) error {
	payloadJSON, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("marshal payload: %w", err)
	}

	_, err = tx.ExecContext(ctx,
		`INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
```

왜 이 코드가 중요했는가:

이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.

새로 배운 것:

- outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.

보조 코드: `solution/go/schema.sql`

```sql
CREATE TABLE IF NOT EXISTS outbox (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type  TEXT NOT NULL,
    aggregate_id    UUID NOT NULL,
    event_type      TEXT NOT NULL,
    payload         JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at    TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_outbox_unpublished
    ON outbox (created_at)
    WHERE published_at IS NULL;

-- Processed events table for consumer idempotency.
CREATE TABLE IF NOT EXISTS processed_events (
    event_id     UUID PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT now()
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

CLI:

```bash
cd 03-platform-engineering/15-event-pipeline
make -C problem build
make -C problem test

cd 03-platform-engineering/15-event-pipeline/solution/go
make repro
```

검증 신호:

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

다음:

- 다음 글에서는 `20-relay-consumer-and-delivery-boundary.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/outbox/repository.go` 같은 결정적인 코드와 `cd 03-platform-engineering/15-event-pipeline` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
