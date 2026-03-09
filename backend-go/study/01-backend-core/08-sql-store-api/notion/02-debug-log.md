# 디버그 기록 — SQL과 HTTP 사이에서 생기는 문제들

## rows.Close() 누락

`List`에서 `rows.Close()`를 빼먹으면 커넥션이 반환되지 않는다. SQLite 인메모리 모드에서는 티가 안 나지만, 실제 DB에서는 커넥션 풀이 고갈된다. `defer rows.Close()`는 `QueryContext` 직후에 반드시 작성한다.

```go
rows, err := r.db.QueryContext(ctx, ...)
if err != nil { return nil, err }
defer rows.Close()  // 여기
```

## sql.ErrNoRows와 일반 에러 구분

`QueryRowContext(...).Scan(...)`이 실패하면 두 가지 경우가 있다:
1. 행이 없음 → `sql.ErrNoRows` → 이건 404
2. 실제 DB 에러 → 이건 500

```go
if errors.Is(err, sql.ErrNoRows) {
    return Product{}, ErrNotFound
}
return Product{}, err  // 다른 에러는 그대로 전파
```

이걸 뒤집어서 `err != nil`만 검사하면 "행이 없는 것"과 "DB 장애"를 구분하지 못한다.

## RowsAffected 반환값 신뢰

Optimistic update에서 `result.RowsAffected()`가 0이면 버전 충돌이다. 그런데 SQLite에서는 `RowsAffected`를 항상 정확히 반환하지만, 일부 드라이버에서는 이 값이 지원되지 않을 수 있다. `modernc.org/sqlite`는 정확하게 지원한다.

## CHECK 제약과 에러 메시지

`stock >= 0` CHECK 제약을 걸어놓으면, 음수로 UPDATE하려 할 때 SQLite가 에러를 던진다. 에러 메시지가 드라이버에 따라 다를 수 있어서, 에러 문자열을 파싱하지 않는 게 좋다. 대신 애플리케이션에서 먼저 검증(`stock < quantity → ErrInsufficientStock`)하고, DB 제약은 최종 안전망으로 둔다.

## InMemory SQLite에서 unique 파일명

```go
sql.Open("sqlite", fmt.Sprintf("file:sql-store-api-%d?mode=memory&cache=shared", time.Now().UnixNano()))
```

테스트가 병렬로 실행될 때, 같은 DB 이름을 쓰면 테이블이 충돌한다. `time.Now().UnixNano()`로 고유한 이름을 생성하면 각 테스트가 독립된 DB를 갖는다.

## defer tx.Rollback()의 안전성

```go
tx, err := r.db.BeginTx(ctx, nil)
defer tx.Rollback()
```

Commit 후에 Rollback을 호출하면 어떻게 될까? 아무 일도 일어나지 않는다. 이미 완료된 트랜잭션에 대한 Rollback은 무시된다. 따라서 `defer tx.Rollback()`은 항상 써도 안전하다.

## PATCH와 PUT의 차이

이 프로젝트에서 PATCH를 선택한 이유: 부분 업데이트를 의도했기 때문. 현재 구현은 모든 필드를 보내야 하므로 사실상 PUT에 가깝지만, "상품의 일부를 수정한다"는 시맨틱이 PATCH에 더 맞다.
