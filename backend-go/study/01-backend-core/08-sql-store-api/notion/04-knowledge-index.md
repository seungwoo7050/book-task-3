# 지식 색인 — SQL Store API 핵심 개념

## database/sql

Go 표준 라이브러리의 데이터베이스 인터페이스. 드라이버에 독립적인 API를 제공한다. `sql.Open`으로 커넥션 풀을 생성하고, `ExecContext`(INSERT/UPDATE/DELETE), `QueryContext`(SELECT 다수 행), `QueryRowContext`(SELECT 단일 행)로 쿼리를 실행한다.

## Repository 패턴

데이터 접근 로직을 캡슐화하는 계층. HTTP 핸들러는 SQL을 모르고, Repository는 HTTP를 모른다. 테스트에서는 Repository를 직접 호출하거나, httptest로 API 전체를 테스트할 수 있다.

## Optimistic Concurrency Control

"충돌은 드물다"는 가정하에 락 없이 동시성을 제어하는 방식. 읽을 때 `version`을 가져오고, 쓸 때 `WHERE version = ?`를 넣어 변경 여부를 확인한다. 다른 요청이 먼저 수정했으면 `RowsAffected` = 0이 되어 충돌을 감지한다.

- **장점**: 락을 걸지 않으므로 읽기 성능이 좋다
- **단점**: 충돌 시 재시도가 필요하다
- **적합**: 동시 수정이 드문 리소스 (사용자 프로필 등)
- **부적합**: 핫 리소스 (인기 상품 재고 등)

## Transaction (트랜잭션)

여러 SQL 문을 하나의 원자적 작업으로 묶는 것. `db.BeginTx`로 시작, `tx.Commit`으로 확정, `tx.Rollback`으로 취소. ACID 중 Atomicity를 보장한다.

```go
tx, err := db.BeginTx(ctx, nil)
defer tx.Rollback()
// ... 여러 쿼리 ...
tx.Commit()
```

## Migration

데이터베이스 스키마를 코드로 관리하는 방식. **Up** 마이그레이션은 스키마를 진화시키고, **Down** 마이그레이션은 이전 상태로 되돌린다. 이 프로젝트에서는 Go 상수(`schemaUp`, `schemaDown`)로 관리하지만, 실무에서는 golang-migrate 같은 도구를 사용한다.

## sql.ErrNoRows

`QueryRowContext(...).Scan(...)`에서 행이 없을 때 반환되는 센티널 에러. `errors.Is(err, sql.ErrNoRows)`로 확인한다. 이 에러를 무시하면 "not found"와 "DB 장애"를 구분하지 못한다.

## CHECK 제약 조건

SQL 테이블에서 컬럼 값의 유효 범위를 강제하는 제약. `CHECK (stock >= 0)`은 음수 재고를 DB 레벨에서 차단한다. 애플리케이션 레벨 검증의 보완재이지, 대체재가 아니다.

## AUTOINCREMENT

SQLite에서 `INTEGER PRIMARY KEY AUTOINCREMENT`는 행이 삭제되어도 ID를 재사용하지 않는 것을 보장한다. `AUTOINCREMENT` 없이 `INTEGER PRIMARY KEY`만 쓰면 성능은 좋지만, 삭제된 ID가 재사용될 수 있다.

## modernc.org/sqlite

CGo 없이 순수 Go로 구현된 SQLite 드라이버. C 컴파일러가 필요 없어서 크로스 컴파일이 쉽다. 테스트에서 인메모리 DB를 쓰기 위해 `file:...?mode=memory&cache=shared` URI를 사용한다.

## r.PathValue("id")

Go 1.22에서 추가된 메서드. `http.Request`에서 라우트 패턴의 `{id}` 부분을 추출한다. 이전에는 직접 URL 경로를 파싱하거나 gorilla/mux 같은 외부 라우터를 사용해야 했다.
