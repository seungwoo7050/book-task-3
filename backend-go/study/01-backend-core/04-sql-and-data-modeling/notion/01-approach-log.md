# 접근 과정 — 스키마 설계부터 트랜잭션까지

## SQLite 드라이버 선택

Go에서 SQLite를 쓰려면 드라이버가 필요하다. 선택지는 크게 두 가지다:
- `mattn/go-sqlite3`: CGO 기반. C 컴파일러가 필요하다.
- `modernc.org/sqlite`: 순수 Go 구현. CGO 없이 동작한다.

`modernc.org/sqlite`를 택했다. 이유는 크로스 컴파일이 필요할 때 CGO 의존성이 걸림돌이 되기 때문이다. `go test ./...`가 어떤 환경에서든 그냥 돌아가길 원했다.

## 스키마 설계

세 테이블을 설계했다:

```sql
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_cents INTEGER NOT NULL CHECK (price_cents > 0)
);

CREATE TABLE inventory (
    player_id INTEGER NOT NULL REFERENCES players(id),
    item_id INTEGER NOT NULL REFERENCES items(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (player_id, item_id)
);
```

`inventory`의 PK가 `(player_id, item_id)`인 이유는 같은 플레이어가 같은 아이템을 두 행으로 가지면 안 되기 때문이다. 대신 `quantity` 컬럼으로 개수를 관리한다.

## JOIN 쿼리

정규화된 세 테이블의 데이터를 "alice는 potion을 2개 가지고 있다"로 보려면 JOIN이 필요하다.

```sql
SELECT p.name, i.name, inv.quantity
FROM inventory inv
JOIN players p ON p.id = inv.player_id
JOIN items i ON i.id = inv.item_id
WHERE p.name = ?
```

파라미터 바인딩(`?`)을 씀으로써 SQL injection을 원천적으로 방지했다. 이건 `database/sql`의 가장 기본적인 보안 관행이다.

## Transaction으로 구매 묶기

`Purchase` 함수는 두 단계로 이루어진다:
1. 아이템 이름으로 ID를 조회
2. inventory에 삽입 또는 수량 증가

이 두 단계 사이에 다른 작업이 끼면 무결성이 깨질 수 있다. 그래서 `db.BeginTx`로 트랜잭션을 시작하고, 성공하면 `tx.Commit()`, 실패하면 `defer tx.Rollback()`으로 정리한다.

`ON CONFLICT ... DO UPDATE` 구문을 사용해서 이미 가지고 있는 아이템이면 수량만 더한다. 이건 "UPSERT" 패턴이라 불리는데, INSERT와 UPDATE를 하나의 SQL로 처리한다.

## 테스트 헬퍼

테스트마다 새 in-memory DB를 만들고 스키마를 적용하고 시드 데이터를 넣는 과정이 반복된다. 이걸 `newTestDB` 헬퍼로 추출했다. `t.Helper()`를 호출해서 테스트 실패 시 에러 위치가 헬퍼 내부가 아닌 실제 테스트 함수를 가리키도록 했다.
