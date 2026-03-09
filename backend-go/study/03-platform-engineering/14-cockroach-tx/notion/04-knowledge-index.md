# 지식 인덱스 — CockroachDB 트랜잭션에서 다룬 개념들

## Serializable Isolation (직렬화 격리)

가장 강력한 트랜잭션 격리 수준. 모든 트랜잭션이 순차적으로 실행된 것과 같은 결과를 보장. CockroachDB의 기본값. PostgreSQL은 기본이 Read Committed. `sql.LevelSerializable`로 명시적 설정.

## Optimistic Locking (낙관적 잠금)

행을 읽을 때 잠금을 걸지 않고, 쓸 때 `WHERE version = ?`로 변경 여부를 확인. 충돌이 드문 시나리오에서 효율적. `DeductBalance`에서 `RETURNING balance, version`으로 갱신 후 값을 바로 가져옴.

## SQLSTATE 40001

ISO SQL 표준에서 정의한 serialization_failure 코드. CockroachDB가 트랜잭션을 직렬화할 수 없다고 판단했을 때 반환. 애플리케이션이 트랜잭션을 처음부터 재시도해야 함. `txn.IsRetryable`에서 체크.

## Idempotency Key (멱등성 키)

같은 요청을 여러 번 보내도 결과가 한 번만 적용되도록 보장하는 메커니즘. 클라이언트가 UUID를 생성해 `Idempotency-Key` 헤더로 전송. 서버는 키와 응답을 DB에 저장하고, 중복 요청 시 캐시된 응답을 반환. 결제, 송금 등 금융 API의 필수 패턴.

## ON CONFLICT ... DO UPDATE (Upsert)

행이 없으면 INSERT, 있으면 UPDATE하는 SQL 패턴. `UNIQUE` 제약에 걸리면 `DO UPDATE` 절이 실행됨. `EXCLUDED`는 INSERT하려던 값을 참조하는 예약어. `UpsertInventory`에서 사용.

## database/sql + pgx/stdlib

Go 표준 `database/sql` 인터페이스에 `pgx` 드라이버를 등록하는 방식. `import _ "github.com/jackc/pgx/v5/stdlib"`로 blank import. `sql.Open("pgx", dsn)`으로 PostgreSQL/CockroachDB에 연결. 표준 인터페이스를 사용하면 드라이버 교체가 용이하지만, pgx 고유 기능(배치, COPY)은 사용 불가.

## Connection Pool Tuning

`database/sql`의 커넥션 풀 설정: `SetMaxOpenConns` (최대 열린 커넥션), `SetMaxIdleConns` (놀고 있는 커넥션), `SetConnMaxLifetime` (커넥션 최대 수명). CockroachDB에서 `ConnMaxLifetime`은 로드밸런서가 커넥션을 고르게 분배하도록 도움.

## Graceful Shutdown

`signal.NotifyContext`로 OS 시그널(SIGTERM, SIGINT)을 받아 `http.Server.Shutdown(ctx)`으로 진행 중인 요청을 마무리한 후 종료. 컨테이너 환경(Kubernetes 등)에서 필수적인 패턴.

## errors.As

Go 1.13+에서 에러 체인을 따라가며 특정 타입의 에러를 찾는 함수. `txn.IsRetryable`에서 `PgError` 인터페이스를 만족하는 에러를 찾을 때 사용. `errors.Is`가 값 비교라면, `errors.As`는 타입 비교.

## JSONB

PostgreSQL/CockroachDB의 바이너리 JSON 타입. 일반 JSON보다 쿼리 성능이 좋고 인덱싱 가능. `idempotency_keys.response`와 `audit_log.detail`에서 사용. Go에서는 `json.RawMessage`로 매핑.
