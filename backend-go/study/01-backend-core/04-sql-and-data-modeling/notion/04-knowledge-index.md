# 지식 인덱스 — 빠른 참조용

## database/sql 패턴

| 함수 | 용도 | 반환 |
|------|------|------|
| `sql.Open(driver, dsn)` | DB 커넥션 풀 생성 | `*sql.DB, error` |
| `db.ExecContext(ctx, query)` | DDL/DML 실행 | `sql.Result, error` |
| `db.QueryContext(ctx, query, args...)` | 여러 행 조회 | `*sql.Rows, error` |
| `tx.QueryRowContext(ctx, query, args...)` | 한 행 조회 | `*sql.Row` |
| `db.BeginTx(ctx, opts)` | 트랜잭션 시작 | `*sql.Tx, error` |
| `tx.Commit()` | 커밋 | `error` |
| `tx.Rollback()` | 롤백 | `error` |

## SQL 패턴

```sql
-- UPSERT (SQLite/PostgreSQL)
INSERT INTO inventory(player_id, item_id, quantity)
VALUES (?, ?, ?)
ON CONFLICT(player_id, item_id)
DO UPDATE SET quantity = inventory.quantity + excluded.quantity;

-- JOIN 조회
SELECT p.name, i.name, inv.quantity
FROM inventory inv
JOIN players p ON p.id = inv.player_id
JOIN items i ON i.id = inv.item_id
WHERE p.name = ?;
```

## SQLite in-memory 연결

```go
// 각 테스트마다 독립 DB
sql.Open("sqlite", fmt.Sprintf("file:test-%d?mode=memory&cache=shared", time.Now().UnixNano()))
```

## CLI 명령 정리

```bash
# 모듈 초기화
go mod init github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling

# SQLite 드라이버 의존성 추가
go get modernc.org/sqlite

# 실행
cd go
go run ./cmd/schemawalk
# 출력: alice owns 2 x potion

# 테스트
go test ./...
go test -v ./catalog/
```

## 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `modernc.org/sqlite` | v1.38.2 | 순수 Go SQLite 드라이버 (CGO 불필요) |
