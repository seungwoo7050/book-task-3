# 디버그 기록 — 분산 DB 트랜잭션의 함정들

## SQLSTATE 40001 — 재시도가 필요한 에러

CockroachDB의 Serializable Isolation에서 트랜잭션 충돌이 발생하면 `40001` (serialization_failure)를 던진다. 이 에러는 애플리케이션 버그가 아니라, DB가 "이 트랜잭션을 다시 해달라"고 요청하는 것이다.

처음에는 Commit 시점에만 이 에러가 발생한다고 생각했지만, 실제로는 `fn(tx)` 실행 중에도 발생할 수 있다. 그래서 `RunInTx`에서 `fn(tx)` 에러와 `tx.Commit()` 에러 모두에 대해 `IsRetryable`을 체크해야 한다.

현재 구현에서는 `fn(tx)` 에러가 retryable이면 재시도하지 않고 바로 반환한다. Commit 에러만 재시도. 이는 의도적인 결정으로, `fn(tx)` 내부에서 40001이 발생하면 이미 트랜잭션이 abort된 상태이므로 Rollback 후 새 트랜잭션을 시작해야 한다.

## 멱등성 키와 재시도의 상호작용

`RunInTx`가 트랜잭션을 재시도하면, `fn(tx)` 안에서 멱등성 키를 먼저 조회한다. 첫 시도에서 INSERT했지만 Commit이 실패하면, 재시도 시 멱등성 키가 존재하지 않는다 (Rollback됐으므로). 그래서 정상적으로 다시 전체 로직이 실행된다.

하지만 주의: 만약 멱등성 키를 트랜잭션 밖에서 관리했다면, 첫 시도 실패 후 두 번째 시도에서 "이미 처리됨"으로 잘못 판단할 수 있다.

## ErrConflict vs 40001

두 가지 다른 충돌이 존재한다:

1. **ErrConflict** (낙관적 잠금): 애플리케이션 레벨에서 version 불일치를 감지. `DeductBalance`에서 `WHERE version = $3`이 매칭되지 않을 때.
2. **40001** (직렬화 실패): DB 레벨에서 트랜잭션 충돌을 감지. CockroachDB가 자체적으로 판단.

ErrConflict는 클라이언트에게 409를 돌려주고, 클라이언트가 재시도 여부를 결정한다. 40001은 `RunInTx`가 자동으로 재시도한다. 이 두 레벨의 재시도를 혼동하면 안 된다.

## `sql.LevelSerializable` 설정

```go
tx, err := db.BeginTx(ctx, &sql.TxOptions{
    Isolation: sql.LevelSerializable,
})
```

CockroachDB는 기본이 Serializable이지만, 명시적으로 설정해야 코드의 의도가 드러난다. PostgreSQL에서 같은 코드를 실행해도 동작하게 된다.

## pgx 드라이버 등록

```go
import _ "github.com/jackc/pgx/v5/stdlib"
```

이 한 줄이 `database/sql`에 `"pgx"` 드라이버를 등록한다. blank import (`_`)라서 직접 사용하는 코드는 없지만 없으면 `sql.Open("pgx", dsn)` 가 실패한다. Go 초심자가 자주 빠뜨리는 부분.

## 커넥션 풀 튜닝

```go
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(5 * time.Minute)
```

CockroachDB에서는 커넥션 수를 노드 수 × vCPU 수의 4배 정도로 잡는 것이 권장 사항. 단일 노드 개발 환경에서 25는 충분하다. `ConnMaxLifetime`은 로드밸런서 뒤에서 커넥션이 한 노드에 고착되는 것을 방지.
