# 회고 — database/sql로 API를 만들어본 뒤

## 무엇을 만들었나

상품(Product)의 CRUD API. SQLite 인메모리 저장소, migration up/down, optimistic update, transaction rollback까지 포함. 외부 의존성은 `modernc.org/sqlite` 하나. 코드량은 store.go 하나에 약 250줄, main.go 약 25줄.

## 잘된 점

**Repository와 App의 분리**가 깔끔했다. Repository는 SQL만 알고, App은 HTTP만 안다. 이 분리 덕분에 테스트에서 `httptest`로 API를 테스트하면서도 Repository를 직접 테스트할 수 있었다.

**Optimistic update가 제대로 동작한다.** `WHERE version = ?`으로 동시 수정을 감지하고 409를 반환하는 흐름이 간결하면서도 실용적이다. 04에서 SQL 기초를 다져놓은 덕에 이 구현이 자연스러웠다.

**트랜잭션 패턴이 확립됐다.** `BeginTx → defer Rollback → 로직 → Commit` 패턴은 이후 프로젝트에서도 반복적으로 사용할 수 있다.

## 아쉬운 점

**store.go에 Repository, App, 핸들러, 헬퍼가 모두 들어있다.** 06에서는 파일을 역할별로 분리했는데(handlers.go, routes.go, helpers.go), 08에서는 한 파일에 모았다. 규모가 작아서 문제가 안 되지만, 장기적으로는 분리하는 게 낫다.

**ReserveStock이 HTTP 엔드포인트로 노출되지 않는다.** Repository에 메서드는 있고 테스트도 있지만, 실제로 호출할 API 엔드포인트가 없다. `POST /v1/products/{id}/reserve` 같은 걸 추가했으면 완결됐을 것이다.

**에러 응답 포맷이 06과 통일되지 않았다.** 06에서는 `error` 키 아래에 메시지가 있었고, 08에서도 비슷하지만 구조가 미묘하게 다르다. 프로젝트 간 일관성을 위해 공통 에러 포맷을 정의할 필요가 있다.

## 프로젝트 04 → 08 연결

04에서 `ApplySchema`와 `Seed`로 스키마와 초기 데이터를 관리했다. 08에서는 이를 `ApplyUpMigration`/`ApplyDownMigration`으로 발전시켰다. 04의 `Purchase` 함수에서 사용한 트랜잭션 패턴이 08의 `ReserveStock`에서 그대로 재활용됐다.

## 프로젝트 09로의 전달

09(cache-migrations-observability)에서는 마이그레이션 도구를 도입하고, 캐시 레이어를 추가하며, 관측성(로깅/메트릭)을 강화한다. 08에서 수동으로 관리하던 SQL 문자열 마이그레이션이 도구 기반으로 전환되는 셈이다.
