# 회고 — CockroachDB와 함께한 트랜잭션 설계

## database/sql 추상화의 가치

이 프로젝트에서 `database/sql` 인터페이스를 유지한 가장 큰 이유는 **드라이버 교체 가능성**이었다. `jackc/pgx/v5/stdlib`은 `database/sql`에 등록되는 어댑터일 뿐, 코드의 나머지 부분은 표준 `*sql.DB`, `*sql.Tx`만 안다.

프로젝트 08에서 `modernc.org/sqlite`를 같은 `database/sql` 인터페이스로 사용했고, 여기서는 CockroachDB를 사용한다. repository 레이어의 SQL 문법 차이(PostgreSQL의 `$1` vs SQLite의 `?`)를 제외하면, 구조는 거의 동일하다.

하지만 `database/sql`의 한계도 있다. `pgx`의 네이티브 인터페이스를 사용하면 배치 쿼리, COPY, 커스텀 타입 등을 더 효율적으로 쓸 수 있다. 이 프로젝트에서는 단순한 CRUD라 표준 인터페이스로 충분했다.

## 트랜잭션 소유권이라는 개념

누가 `BEGIN`하고 누가 `COMMIT`하는가? 이 프로젝트의 답: **아무도 직접 하지 않는다**. `txn.RunInTx`가 트랜잭션 생명주기를 전담한다. repository 함수는 `*sql.Tx`를 받아 쿼리만 실행하고, service는 `RunInTx`의 콜백 안에서 repository를 조합한다.

이 패턴의 장점은 재시도 로직이 한 곳에 집중된다는 것이다. 만약 repository가 자체적으로 트랜잭션을 관리했다면, 재시도를 어디서 해야 할지 애매해진다.

## 멱등성은 생각보다 까다롭다

멱등성 키를 "트랜잭션 안에서" 저장하는 것이 핵심이다. 다른 옵션들과 비교:

1. **트랜잭션 안** (현재 구현): 구매 성공과 멱등성 키 저장이 원자적. Rollback되면 둘 다 사라진다. ✅
2. **트랜잭션 밖 (먼저 저장)**: 키를 먼저 저장하고 구매를 실행하면, 구매 실패 시 키가 남아서 이후 재시도가 "이미 처리됨"으로 잘못 판단. ❌
3. **트랜잭션 밖 (나중에 저장)**: 구매 성공 후 키 저장이 실패하면, 재시도 시 돈이 두 번 빠짐. ❌

결론: 멱등성 키는 비즈니스 로직과 같은 트랜잭션에 있어야 한다.

## PgError 인터페이스 — 의존성 경계 짓기

`txn` 패키지가 `pgx`를 import하지 않고, 인터페이스로 에러 타입을 추상화한 것은 좋은 설계 결정이었다. `errors.As`가 Go의 에러 체인을 따라가며 `SQLState()` 메서드를 가진 에러를 찾아준다. 덕분에 `txn` 패키지를 다른 PostgreSQL 드라이버(예: `lib/pq`)와도 사용할 수 있다.

## Docker Compose로 CockroachDB 로컬 개발

프로덕션에서는 3노드 이상 클러스터를 구성하지만, 로컬 개발에서는 `start-single-node --insecure`로 충분하다. `docker-compose.yml`에 헬스체크를 넣어서 `make wait-db`로 DB가 준비될 때까지 대기. 이 패턴은 CI/CD에서도 유용하다.

## 다음에 다시 만든다면

`RunInTx`에 지수 백오프(exponential backoff)를 추가할 것이다. 현재는 40001을 받으면 즉시 재시도하는데, 경합이 심한 경우 바로 재시도하면 또 충돌할 확률이 높다. `time.Sleep(backoff)` + jitter가 더 효과적.
