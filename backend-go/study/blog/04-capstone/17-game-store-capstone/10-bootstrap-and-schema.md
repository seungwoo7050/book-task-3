# 17 Game Store Capstone — Bootstrap And Schema

`04-capstone/17-game-store-capstone`는 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다. 이 글에서는 1단계: 인프라 구성 -> 2단계: Go 모듈 초기화 -> 3단계: 스키마 설계 -> 4단계: 패키지 구조 설계 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 인프라 구성
- 2단계: Go 모듈 초기화
- 3단계: 스키마 설계
- 4단계: 패키지 구조 설계

## Day 1
### Session 1

- 당시 목표: 잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 하나의 흐름으로 묶어야 한다.
- 변경 단위: `jackc/pgx/v5`, `google/uuid`
- 처음 가설: 필수 기술을 하나의 단일 백엔드 기준선으로 다시 묶어 capstone으로 삼았다.
- 실제 진행: CockroachDB 단일 노드 (프로젝트 14와 동일 패턴). Go 1.24.0. 의존성: `jackc/pgx/v5` v5.8.0 — CockroachDB 드라이버 `google/uuid` v1.6.0 — 애플리케이션 레벨 UUID 생성 테이블: `players` — balance BIGINT, version BIGINT, CHECK (balance >= 0) `catalog_items` — sku UNIQUE, price CHECK (price > 0) `purchases` — FK to players, catalog_items `inventories` — UNIQUE (player_id, item_id), qty CHECK (qty >= 0) `idempotency_keys` — key TEXT PK, request_hash, response_json JSONB `outbox` — aggregate_id, event_type, payload_json, published_at nullable

CLI:

```bash
cd 17-game-store-capstone/go
docker compose up -d
make wait-db

go mod init github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone
go get github.com/jackc/pgx/v5
go get github.com/google/uuid
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/schema.sql`

```sql
CREATE TABLE IF NOT EXISTS players (
    id         UUID PRIMARY KEY,
    name       TEXT NOT NULL,
    balance    BIGINT NOT NULL CHECK (balance >= 0),
    version    BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS catalog_items (
    id         UUID PRIMARY KEY,
    sku        TEXT NOT NULL UNIQUE,
    name       TEXT NOT NULL,
    price      BIGINT NOT NULL CHECK (price > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS purchases (
    id         UUID PRIMARY KEY,
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.

보조 코드: `solution/go/internal/config/config.go`

```go
type Config struct {
	Addr            string
	DatabaseURL     string
	RelayInterval   time.Duration
	RelayBatchSize  int
	RateLimitRPS    int
	ShutdownTimeout time.Duration
}

func Load() (Config, error) {
	cfg := Config{
		Addr:            getEnv("ADDR", ":8080"),
		DatabaseURL:     getEnv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/game_store?sslmode=disable"),
		RelayInterval:   time.Second,
		RelayBatchSize:  50,
		RateLimitRPS:    30,
		ShutdownTimeout: 10 * time.Second,
	}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 04-capstone/17-game-store-capstone/go
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
go test ./...
make repro
```

검증 신호:

- 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 2026-03-08 기준 `go test ./...`가 통과했다.
- 2026-03-08 기준 `make repro`가 통과했다.

다음:

- 다음 글에서는 `20-purchase-flow-and-tx-core.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/schema.sql` 같은 결정적인 코드와 `cd 04-capstone/17-game-store-capstone/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
