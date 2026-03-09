# 타임라인 — 이벤트 파이프라인 프로젝트 전체 과정

## 1단계: 인프라 구성

```bash
cd 15-event-pipeline/go
docker compose -p event-pipeline up -d
```

두 서비스 실행:
- **CockroachDB**: `cockroachdb/cockroach:v25.3.3`, 포트 26258 (SQL), 8082 (Admin UI)
- **Redpanda**: `redpandadata/redpanda:v24.3.5`, 포트 9093 (Kafka), 18082 (HTTP Proxy)

```bash
# 준비 대기
make wait-db
# Redpanda는 healthcheck으로 자동 대기
```

## 2단계: 스키마 적용

```bash
make migrate
```

2개 테이블:
- `outbox`: 이벤트 아웃박스 (UUID PK, aggregate_type, event_type, payload JSONB, published_at nullable)
- `processed_events`: Consumer 멱등성 (event_id UUID PK, processed_at)
- Partial index: `idx_outbox_unpublished` — `WHERE published_at IS NULL`

## 3단계: Go 모듈 초기화

```bash
go mod init github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline
go get github.com/jackc/pgx/v5
go get github.com/segmentio/kafka-go
```

Go 1.24.0. 주요 의존성:
- `jackc/pgx/v5` v5.8.0 — CockroachDB 드라이버
- `segmentio/kafka-go` v0.4.47 — Kafka 클라이언트

## 4단계: Outbox 패키지 구현

```
outbox/
├── model.go         # Event, PurchasePayload 구조체
├── repository.go    # InsertTx, GetUnpublished, MarkPublished, Cleanup
└── repository_test.go
```

`InsertTx`는 `*sql.Tx`를 받아 트랜잭션 내 INSERT. 나머지는 `*sql.DB`로 독립 실행.

```bash
go test ./outbox/ -v
```

## 5단계: Relay 구현

```
relay/
├── relay.go
└── relay_test.go
```

`Relay.Run(ctx)` — ticker 루프, 폴링 → Kafka 발행 → MarkPublished.
설정: `PollInterval` (기본 1초), `BatchSize` (기본 100).
Key = AggregateID, Headers = event_type + event_id + aggregate_type.

```bash
go test ./relay/ -v
```

## 6단계: Consumer 구현

```
consumer/
├── consumer.go
└── consumer_test.go
```

2단계 멱등성: 인메모리 map → DB processed_events.
`FetchMessage` + `CommitMessages` 수동 커밋.
Handler 실패 시 오프셋 미커밋 → 자동 재전달.

```bash
go test ./consumer/ -v
```

## 7단계: CLI 진입점

```
cmd/
├── relay/main.go
└── consumer/main.go
```

각각 독립 프로세스로 실행 가능.

```bash
# Relay 실행
go run ./cmd/relay

# Consumer 실행
go run ./cmd/consumer
```

## 8단계: Kafka 토픽 생성

```bash
# Redpanda rpk CLI로 토픽 생성
docker compose exec kafka rpk topic create game.purchases --partitions 3
```

파티션 3개: Consumer Group 내 최대 3개 Consumer 병렬 처리.

## 9단계: E2E 테스트

```bash
make e2e
# RUN_E2E=1 DATABASE_URL=... KAFKA_BROKERS=... go test ./e2e -v -count=1
```

전체 흐름: 구매 → outbox INSERT → relay 발행 → consumer 처리

## 10단계: 빌드 및 검증

```bash
make build
make test
make test-race
make smoke
```

## 소스 코드에서 보이지 않는 것들

| 항목 | 설명 |
|------|------|
| Redpanda 버전 | v24.3.5 — Kafka 호환, JVM 불필요 |
| Kafka 포트 | 9093 (외부), 29092 (내부 컨테이너 간) |
| 메모리 제한 | Redpanda `--memory=512M` — 개발 환경 최소 설정 |
| Kafka 프로토콜 | segmentio/kafka-go가 사용하므로 Redpanda도 그대로 동작 |
| 토픽명 | `game.purchases` — 네임스페이스(game) + 이벤트(purchases) |
| Consumer Group | `purchase-analytics` |
| Relay 폴링 간격 | 기본 1초 — 프로덕션에서는 100ms~5s 사이로 튜닝 |
| Cleanup 호출 시점 | 코드에 구현됐지만 자동 스케줄링은 별도 구현 필요 |
| partial index 사용 | `WHERE published_at IS NULL` — 미발행 이벤트만 인덱싱 |
