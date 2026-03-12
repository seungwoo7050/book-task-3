# 타임라인 — Game Store Capstone 전체 과정

## 1단계: 인프라 구성

```bash
cd 17-game-store-capstone/go
docker compose up -d
make wait-db
```

CockroachDB 단일 노드 (프로젝트 14와 동일 패턴).

## 2단계: Go 모듈 초기화

```bash
go mod init github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone
go get github.com/jackc/pgx/v5
go get github.com/google/uuid
```

Go 1.24.0. 의존성:
- `jackc/pgx/v5` v5.8.0 — CockroachDB 드라이버
- `google/uuid` v1.6.0 — 애플리케이션 레벨 UUID 생성

## 3단계: 스키마 설계

```bash
make migrate
# schema.sql 적용: 6개 테이블
```

테이블:
1. `players` — balance BIGINT, version BIGINT, CHECK (balance >= 0)
2. `catalog_items` — sku UNIQUE, price CHECK (price > 0)
3. `purchases` — FK to players, catalog_items
4. `inventories` — UNIQUE (player_id, item_id), qty CHECK (qty >= 0)
5. `idempotency_keys` — key TEXT PK, request_hash, response_json JSONB
6. `outbox` — aggregate_id, event_type, payload_json, published_at nullable

## 4단계: 패키지 구조 설계

```
internal/
├── config/        # 환경 변수 바인딩
├── domain/        # 순수 타입 (6개 struct)
├── repository/    # Store struct, SQL 메서드
├── service/       # PurchaseService, QueryService
├── httpapi/       # Handler + Middleware
├── relay/         # Outbox Relay (인터페이스 기반)
└── txn/           # RunInTx (프로젝트 14 재사용)
```

## 5단계: domain 패키지

```go
// 6개 도메인 타입 정의
type Player struct { ... }
type CatalogItem struct { ... }
type Purchase struct { ... }
type InventoryItem struct { ... }
type IdempotencyRecord struct { ... }
type OutboxEvent struct { ... }
```

외부 의존 없는 순수 타입.

## 6단계: repository 구현

`Store` struct에 전체 SQL 접근 메서드. 모든 쓰기 메서드는 `*sql.Tx` 인자.

```bash
go build ./internal/repository/
```

## 7단계: txn 패키지 (재사용)

프로젝트 14의 `txn/retry.go`를 그대로 복사. `PgError` 인터페이스, `IsRetryable`, `RunInTx`.

```bash
go test ./internal/txn/ -v
```

## 8단계: service 구현

`PurchaseService.Purchase` — 7단계 트랜잭션 로직:
멱등성 키 확인 → 플레이어/아이템 조회 → 잔액 차감 → 구매/인벤토리 → Outbox INSERT → 멱등성 키 INSERT

`QueryService` — 읽기 전용 (GetPurchase, GetPlayerInventory)

```bash
go test ./internal/service/ -v
```

## 9단계: httpapi 구현

4개 엔드포인트 + loggingMiddleware + rateLimitMiddleware.
`decoder.DisallowUnknownFields()` 적용.
에러 → HTTP 상태 코드 매핑.

## 10단계: relay 구현

`OutboxStore` + `Publisher` 인터페이스.
`Relay.PollOnce` 공개 메서드 (테스트용).

```bash
go test ./internal/relay/ -v
```

## 11단계: cmd/api 진입점

```bash
# 로컬 실행
make run
# 또는: go run ./cmd/api

# 빌드
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
```

API + Relay를 같은 프로세스에서 실행 (별도 고루틴).
Graceful shutdown: SIGTERM → Relay 중지 → HTTP 서버 Shutdown.

## 12단계: E2E 테스트

```bash
make e2e
# 구매 → 조회 → 멱등성 → 인벤토리 확인
```

## 13단계: 전체 검증

```bash
make build
make test
go test -race ./...
```

## 소스 코드에서 보이지 않는 것들

| 항목 | 설명 |
|------|------|
| 의존성 수 | 2개만 (pgx, uuid) — 캡스톤임에도 최소 의존 유지 |
| Relay Publisher | 인터페이스만 정의, Kafka 연동은 프로젝트 15에서 별도 |
| Rate Limit 방식 | Fixed-Window (프로젝트 11의 Token Bucket 대신 단순화) |
| 인증 없음 | 의도적 제외 — Out of Scope 명시 |
| 분산 트레이싱 없음 | 의도적 제외 — Out of Scope 명시 |
| `internal/` 사용 | Go 컴파일러가 외부 모듈 접근을 차단 |
| request_hash 구분자 | `playerID + "|" + itemID` — concat 충돌 방지 |
| Balance CHECK 제약 | 애플리케이션 + DB 양쪽에서 검증 (Defense in Depth) |
| UUID 생성 위치 | 애플리케이션 레벨 (DB gen_random_uuid 미사용) |
