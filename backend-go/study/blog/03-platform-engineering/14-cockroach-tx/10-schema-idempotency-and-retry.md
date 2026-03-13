# 14 Cockroach TX — Schema Idempotency And Retry

`03-platform-engineering/14-cockroach-tx`는 idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다. 이 글에서는 1단계: 인프라 구성 -> 2단계: 스키마 설계 및 마이그레이션 -> 3단계: Go 모듈 초기화 -> 4단계: 패키지 구조 설계 -> 5단계: Repository 구현 -> 6단계: 트랜잭션 재시도 헬퍼 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 인프라 구성
- 2단계: 스키마 설계 및 마이그레이션
- 3단계: Go 모듈 초기화
- 4단계: 패키지 구조 설계
- 5단계: Repository 구현
- 6단계: 트랜잭션 재시도 헬퍼

## Day 1
### Session 1

- 당시 목표: 중복 요청, 동시 요청, CockroachDB retry를 한 purchase 흐름에서 다뤄야 한다.
- 변경 단위: `solution/go/schema.sql`, `solution/go/txn/retry.go`
- 처음 가설: DB가 요구하는 retry와 애플리케이션이 요구하는 idempotency를 한 흐름에서 분리해 보여 준다.
- 실제 진행: 포트 매핑: `26257:26258` (SQL), `8081:8080` (Admin UI) 4개 테이블: `players`, `inventory`, `idempotency_keys`, `audit_log` 핵심 제약: `players.version` (낙관적 잠금), `UNIQUE(player_id, item_name)` (upsert), `REFERENCES players(id)` (FK) Go 1.24.0 사용. pgx v5.8.0 — CockroachDB/PostgreSQL 드라이버. 순서: player.go (GetPlayer, DeductBalance) → inventory.go (UpsertInventory) → audit.go (InsertAuditLog) → idempotency.go (Get/Insert/Exists)

CLI:

```bash
# Docker Compose로 CockroachDB 단일 노드 실행
cd 14-cockroach-tx/go
docker compose -p cockroach-tx up -d db

# DB 준비 대기
make wait-db
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/schema.sql`

```sql
CREATE TABLE IF NOT EXISTS players (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    balance     BIGINT NOT NULL DEFAULT 0,
    version     INT NOT NULL DEFAULT 1,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS inventory (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id   UUID NOT NULL REFERENCES players(id),
    item_name   TEXT NOT NULL,
    quantity    INT NOT NULL DEFAULT 1,
    acquired_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (player_id, item_name)
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다.

보조 코드: `solution/go/txn/retry.go`

```go
type PgError interface {
	error
	SQLState() string
}

func IsRetryable(err error) bool {
	var pgErr PgError
	if errors.As(err, &pgErr) {
		return pgErr.SQLState() == RetryableErrorCode
	}
	return false
}
func RunInTx(ctx context.Context, db *sql.DB, maxRetries int, fn func(tx *sql.Tx) error) error {
	if maxRetries <= 0 {
		maxRetries = 3
	}

	var lastErr error
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 충돌이 나는 환경에서 작업을 어떤 조건으로 다시 감을지 정한 핵심 invariant다. 분산 저장소나 고충돌 환경을 다룬다는 말은 결국 이 재시도 규칙을 어떻게 세웠는가로 좁혀진다.

CLI:

```bash
cd 03-platform-engineering/14-cockroach-tx
make -C problem build
make -C problem test

cd 03-platform-engineering/14-cockroach-tx/solution/go
make repro
```

검증 신호:

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

다음:

- 다음 글에서는 `20-purchase-service-and-http-surface.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/schema.sql` 같은 결정적인 코드와 `cd 03-platform-engineering/14-cockroach-tx` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
