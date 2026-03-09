# 디버그 기록 — 어디서 막혔고 어떻게 풀었나

## SQLite in-memory DB 공유 문제

SQLite in-memory 데이터베이스를 `:memory:`로 열면 각 연결이 독립적인 DB를 갖는다. Go의 `database/sql`은 커넥션 풀을 사용하기 때문에, 스키마를 적용한 커넥션과 쿼리를 실행하는 커넥션이 다를 수 있다. 그러면 "테이블이 없다"는 에러가 난다.

해결책은 `cache=shared` 옵션과 고유한 파일 이름을 쓰는 것이다:

```go
sql.Open("sqlite", fmt.Sprintf("file:sql-modeling-%d?mode=memory&cache=shared", time.Now().UnixNano()))
```

`cache=shared`를 쓰면 같은 이름의 in-memory DB를 여러 커넥션이 공유한다. 타임스탬프를 파일 이름에 넣은 건 병렬 테스트 간 DB가 겹치지 않게 하기 위해서다.

## FK constraint가 적용되지 않는 문제

SQLite는 기본적으로 FK constraint가 비활성화돼 있다. `REFERENCES players(id)`를 스키마에 넣어도, 실제로 존재하지 않는 `player_id`를 넣을 수 있다. 이걸 활성화하려면:

```sql
PRAGMA foreign_keys = ON;
```

이 과제에서는 FK 활성화를 별도로 하지는 않았다. SQLite의 이 특성을 알고 있되, 이 단계에서는 스키마 구조 자체를 이해하는 데 집중했다. 실제 PostgreSQL 환경에서는 FK가 기본으로 동작한다.

## ON CONFLICT 구문의 문법

처음에 MySQL 스타일의 `ON DUPLICATE KEY UPDATE`를 쓰다가 SQLite에서 동작하지 않는다는 걸 알았다. SQLite(그리고 PostgreSQL)에서는 `ON CONFLICT ... DO UPDATE SET` 구문을 사용한다:

```sql
ON CONFLICT(player_id, item_id)
DO UPDATE SET quantity = inventory.quantity + excluded.quantity
```

`excluded`는 충돌한 새 값을 참조하는 키워드다. 이건 SQLite/PostgreSQL 특유의 문법으로, 다른 RDBMS에서는 다를 수 있다.

## rows.Close() 호출 타이밍

`ListInventory`에서 `db.QueryContext`를 호출한 뒤 `defer rows.Close()`를 넣는 위치가 중요하다. 에러 체크 전에 `defer`를 걸면 `rows`가 nil일 때 panic이 난다. 에러 체크 후에 `defer`를 거는 게 맞다:

```go
rows, err := db.QueryContext(ctx, ...)
if err != nil {
    return nil, err
}
defer rows.Close()
```

이 순서를 처음에 뒤집었다가 nil rows에서 panic을 만났다.
