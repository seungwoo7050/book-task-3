# 접근 과정 — SQL 저장소를 HTTP API에 연결하기까지

## 스키마 설계

테이블 하나, 컬럼 네 개:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    version INTEGER NOT NULL DEFAULT 1
);
```

`CHECK (stock >= 0)` 제약은 DB 레벨에서 음수 재고를 방지한다. 애플리케이션 레벨 검증만 믿으면 동시 요청에서 음수가 뚫릴 수 있지만, DB 제약이 최종 방어선이다.

`version` 컬럼은 optimistic concurrency control을 위한 것이다. 처음에 1로 시작하고, UPDATE마다 1씩 증가한다.

## Migration Up/Down

외부 도구 없이 Go 상수로 관리:

```go
const schemaUp = `CREATE TABLE products (...);`
const schemaDown = `DROP TABLE IF EXISTS products;`
```

`ApplyUpMigration`과 `ApplyDownMigration`은 각각 `db.ExecContext`를 호출한다. 단순하지만, 마이그레이션의 핵심 개념을 정확히 보여준다: **up은 구조를 만들고, down은 원래대로 되돌린다**.

## Repository 패턴

`Repository` 구조체가 `*sql.DB`를 감싼다. CRUD 메서드 네 개:

- **Create**: `INSERT INTO products(name, stock)` → `LastInsertId()`로 생성된 ID 반환
- **Get**: `QueryRowContext` + `Scan` → `sql.ErrNoRows`면 `ErrNotFound` 반환
- **List**: `QueryContext` → `rows.Next()`로 순회, `defer rows.Close()` 필수
- **Update**: `WHERE id = ? AND version = ?` → `RowsAffected()` 0이면 `ErrConflict`

## Optimistic Update 상세

PATCH 요청에서 클라이언트가 현재 `version`을 함께 보낸다:

```json
{"name": "super potion", "stock": 15, "version": 1}
```

UPDATE 쿼리의 WHERE 절에 `version = ?`를 넣으면, 다른 요청이 먼저 수정했을 경우 `RowsAffected` = 0이 된다. 이때 409 Conflict를 반환한다. 클라이언트는 최신 데이터를 다시 불러온 뒤 재시도해야 한다.

이 방식은 락(lock)을 걸지 않기 때문에 "optimistic"이다. 충돌이 드문 경우에 성능이 좋고, 충돌이 잦으면 재시도 오버헤드가 커진다.

## Transaction과 Rollback

`ReserveStock`은 재고를 차감하는 메서드다:

```go
tx, err := r.db.BeginTx(ctx, nil)
defer tx.Rollback()

// 1. 현재 재고 확인
// 2. stock < quantity → ErrInsufficientStock 반환 (Rollback 자동 실행)
// 3. 충분하면 UPDATE stock = stock - quantity
// 4. tx.Commit()
```

`defer tx.Rollback()`은 안전장치다. Commit이 성공하면 Rollback은 무의미하다. Commit 전에 에러가 발생하면 defer가 트랜잭션을 되돌린다.

## HTTP 계층 (App)

`App` 구조체가 `Repository`를 받아서 HTTP 핸들러를 노출한다:

| 메서드 | 경로 | 핸들러 | 역할 |
|--------|------|--------|------|
| POST | /v1/products | createProduct | 상품 생성 |
| GET | /v1/products | listProducts | 전체 조회 |
| GET | /v1/products/{id} | showProduct | 단일 조회 |
| PATCH | /v1/products/{id} | updateProduct | 수정 (optimistic) |

에러 매핑:
- `ErrNotFound` → 404
- `ErrConflict` → 409
- 입력 검증 실패 → 422 (name 비어있거나 stock 음수)

## 헬퍼 함수

`writeJSON`과 `writeError` 두 함수로 응답을 통일했다. 06에서도 비슷한 패턴을 사용했지만, 08에서는 같은 패키지 안에 두었다. 별도 패키지로 분리할 규모가 아니었기 때문이다.
