# 접근 기록 — 4개 계층으로 나누어 쌓기

## 계층 설계: handler → service → repository / txn

시작점은 Clean Architecture의 간소화 버전이다. 각 패키지가 하나의 책임만 갖도록 했다.

```
handler/    → HTTP 입출력, 요청 검증, 에러 매핑
service/    → 비즈니스 로직 조율
repository/ → SQL 쿼리, 데이터 접근
txn/        → 트랜잭션 재시도 헬퍼
```

이 구조에서 가장 중요한 결정: **repository 함수들이 `*sql.Tx`를 인자로 받는다**. repository가 트랜잭션을 시작하거나 커밋하지 않는다. 트랜잭션의 생명주기는 `txn.RunInTx`가 관리하고, service가 그 안에서 여러 repository 함수를 조합한다.

## repository: 함수 단위의 SQL 접근

클래스(struct)가 아닌 패키지 수준 함수로 구현했다. `GetPlayer`, `DeductBalance`, `UpsertInventory`, `InsertAuditLog`, `GetIdempotencyKey`, `InsertIdempotencyKey` — 각각 하나의 SQL 문을 실행한다.

### DeductBalance — 낙관적 잠금

```go
UPDATE players SET balance = balance - $1, version = version + 1
WHERE id = $2 AND version = $3
RETURNING balance, version
```

`RETURNING` 절로 갱신된 값을 한 번에 가져온다. 영향받은 행이 없으면(다른 트랜잭션이 먼저 version을 올렸으면) `sql.ErrNoRows` → `ErrConflict`로 변환.

### UpsertInventory — ON CONFLICT

```go
INSERT INTO inventory (player_id, item_name, quantity) VALUES ($1, $2, $3)
ON CONFLICT (player_id, item_name) DO UPDATE SET quantity = inventory.quantity + EXCLUDED.quantity
```

같은 아이템을 또 사면 수량만 늘어난다. `UNIQUE (player_id, item_name)` 제약이 이 upsert를 가능하게 한다.

## txn: 재시도 헬퍼

`RunInTx`는 세 단계다:

1. `db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})`
2. `fn(tx)` 호출
3. `tx.Commit()`

Commit이 실패하고 SQLSTATE가 `40001`이면, 1번부터 다시. 최대 `maxRetries`번.

핵심 결정: `PgError` 인터페이스를 정의해서 `pgx`를 직접 import하지 않았다. `errors.As`로 `SQLState()` 메서드를 가진 에러를 찾는다. 이렇게 하면 `txn` 패키지가 드라이버에 독립적이 된다.

```go
type PgError interface {
    error
    SQLState() string
}
```

## service: 비즈니스 오케스트레이션

`PurchaseService.Purchase`는 `txn.RunInTx` 안에서 6단계를 실행한다:

1. 멱등성 키 확인 → 있으면 캐시된 응답 반환
2. 플레이어 조회 → 잔액 확인
3. 잔액 차감 (낙관적 잠금)
4. 인벤토리 추가 (upsert)
5. 감사 로그 기록
6. 응답 생성 → 멱등성 키 저장

이 전체가 `fn(tx)` 클로저 안에 있으므로, CockroachDB가 40001을 던지면 6단계 모두 처음부터 다시 실행된다. 모든 단계가 SQL 쿼리이므로 side effect가 없다.

## handler: HTTP ↔ Service 브릿지

`PurchaseHandler.ServeHTTP`는:
- `Idempotency-Key` 헤더 필수 검증
- JSON 바디 디코딩 + 필드 검증
- `service.Purchase` 호출
- `ErrConflict` → 409, 그 외 에러 → 500, 성공 → 200

`writeJSON` 헬퍼로 응답 형식을 통일.

## cmd/server: 진입점

`jackc/pgx/v5/stdlib`을 import하면 `database/sql`에 `pgx` 드라이버가 등록된다. `sql.Open("pgx", dsn)`으로 연결. 커넥션 풀 설정: `MaxOpenConns=25`, `MaxIdleConns=10`, `ConnMaxLifetime=5m`.

graceful shutdown은 `SIGTERM`/`SIGINT`를 받으면 5초 타임아웃으로 `srv.Shutdown`.
