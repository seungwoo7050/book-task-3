# 타임라인 — CockroachDB 트랜잭션 프로젝트 전체 과정

## 1단계: 인프라 구성

```bash
# Docker Compose로 CockroachDB 단일 노드 실행
cd 14-cockroach-tx/go
docker compose -p cockroach-tx up -d db
```

```yaml
# docker-compose.yml — CockroachDB v25.3.3
cockroachdb/cockroach:v25.3.3
  --start-single-node --insecure
  --sql-addr=0.0.0.0:26258
  --http-addr=0.0.0.0:8080
```

포트 매핑: `26257:26258` (SQL), `8081:8080` (Admin UI)

```bash
# DB 준비 대기
make wait-db
```

## 2단계: 스키마 설계 및 마이그레이션

```bash
# schema.sql 적용
make migrate
# 내부: cockroach sql --insecure < /workspace/schema.sql
```

4개 테이블: `players`, `inventory`, `idempotency_keys`, `audit_log`
핵심 제약: `players.version` (낙관적 잠금), `UNIQUE(player_id, item_name)` (upsert), `REFERENCES players(id)` (FK)

## 3단계: Go 모듈 초기화

```bash
go mod init github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx
go get github.com/jackc/pgx/v5
```

Go 1.24.0 사용. pgx v5.8.0 — CockroachDB/PostgreSQL 드라이버.

## 4단계: 패키지 구조 설계

```
solution/go/
├── cmd/server/main.go     # 진입점
├── handler/purchase.go    # HTTP 핸들러
├── service/purchase.go    # 비즈니스 로직
├── repository/            # 데이터 접근 (4파일)
│   ├── player.go
│   ├── inventory.go
│   ├── idempotency.go
│   └── audit.go
├── txn/retry.go           # 트랜잭션 재시도
├── e2e/                   # 통합 테스트
├── schema.sql
└── docker-compose.yml
```

## 5단계: Repository 구현

```bash
# 각 파일 작성 후 컴파일 확인
go build ./...
```

순서: player.go (GetPlayer, DeductBalance) → inventory.go (UpsertInventory) → audit.go (InsertAuditLog) → idempotency.go (Get/Insert/Exists)

모든 함수가 `(ctx context.Context, tx *sql.Tx, ...)` 시그니처.

## 6단계: 트랜잭션 재시도 헬퍼

```bash
# txn 패키지 단위 테스트
go test ./txn/ -v
```

`PgError` 인터페이스 정의 → `IsRetryable` → `RunInTx` (BEGIN → fn → COMMIT, 40001이면 재시도)

## 7단계: Service 구현

`PurchaseService.Purchase` — `RunInTx` 안에서 6단계 조율:
멱등성 키 확인 → 플레이어 조회 → 잔액 차감 → 인벤토리 upsert → 감사 로그 → 멱등성 키 저장

```bash
go test ./service/ -v
```

## 8단계: HTTP Handler

`PurchaseHandler.ServeHTTP` — `Idempotency-Key` 헤더 검증, JSON 디코딩, ErrConflict → 409 매핑

## 9단계: cmd/server 진입점

```bash
# 로컬 실행
make run
# 또는: DATABASE_URL="postgresql://root@localhost:26257/defaultdb?sslmode=disable" go run ./cmd/server
```

커넥션 풀: `MaxOpenConns=25`, `MaxIdleConns=10`, `ConnMaxLifetime=5m`
Graceful shutdown: SIGTERM/SIGINT → 5초 타임아웃

## 10단계: E2E 테스트

```bash
# CockroachDB 연동 통합 테스트
make e2e
# 내부: RUN_E2E=1 DATABASE_URL=... go test ./e2e -v -count=1
```

`RUN_E2E=1` 환경변수로 게이트. CI에서는 DB가 있을 때만 실행.

## 11단계: 빌드 및 검증

```bash
make build          # bin/server 바이너리 생성
make test           # 단위 테스트
make test-race      # -race 플래그
make smoke          # = make e2e
```

## 소스 코드에서 보이지 않는 것들

| 항목 | 설명 |
|------|------|
| CockroachDB 버전 | v25.3.3 — `--start-single-node --insecure` |
| pgx 버전 선택 | v5.8.0 — `database/sql` 어댑터(`stdlib`) 사용, 네이티브 pgx API 미사용 |
| DSN 형식 | `postgresql://root@localhost:26257/defaultdb?sslmode=disable` |
| Admin UI | `http://localhost:8081` — 트랜잭션 충돌 모니터링 |
| 스키마 리셋 | `make reset-schema` — `DROP SCHEMA public CASCADE` → 재생성 |
| 헬스체크 SQL | `SELECT 1` — CockroachDB 노드 준비 확인 |
| 격리 수준 | `sql.LevelSerializable` — CockroachDB 기본이지만 명시 |
| 재시도 횟수 | 기본 3회, `PurchaseService.MaxRetries`로 변경 가능 |
| E2E 게이트 | `RUN_E2E=1` 없으면 테스트 스킵 — 로컬 개발 편의 |
