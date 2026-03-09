# 문제 정의 — 왜 SQL Store API인가

## 이전 프로젝트와의 간극

05(http-rest-basics)에서는 `sync.Map`에 Task를 저장했고, 06(go-api-standard)에서는 `sync.RWMutex`로 보호한 맵에 Movie를 저장했다. 서버가 꺼지면 데이터도 사라졌다. 04(sql-and-data-modeling)에서는 SQL 스키마를 다뤘지만 HTTP 계층과 연결하지 않았다. 07(auth-session-jwt)에서는 사용자를 하드코딩했기 때문에 실제 저장소가 필요 없었다.

이 네 프로젝트 사이에 비어 있는 조각이 있다: **SQL 저장소를 실제 HTTP API 뒤에 붙이는 경험**. 08은 그 간극을 메운다.

## 핵심 과제

1. **`database/sql` 기반 Repository**: Go의 `database/sql` 패키지로 CRUD를 구현한다. ORM이 아니다.
2. **Migration up/down**: 스키마 생성과 롤백을 코드로 관리한다.
3. **Optimistic Update**: 버전 번호로 동시 수정을 감지한다. `WHERE version = ?` 조건이 핵심.
4. **Transaction Rollback**: 재고 부족 시 트랜잭션을 롤백해 데이터 무결성을 지킨다.

## 왜 ORM이 아닌가

Go 생태계에는 GORM, Ent 같은 ORM이 있지만, `database/sql`을 먼저 익혀야 ORM이 무엇을 숨기고 있는지 파악할 수 있다. SQL 쿼리를 직접 작성하고, `rows.Scan`으로 직접 매핑하고, `tx.Rollback()`을 직접 호출하는 경험이 있어야 ORM의 추상화가 유용한지 위험한지 판단할 수 있다.

## 제약 조건

- 데이터베이스: modernc.org/sqlite (pure Go, 외부 C 라이브러리 불필요)
- 인메모리 모드: 테스트와 개발 모두 `:memory:` 사용
- 외부 마이그레이션 도구(golang-migrate 등) 없이, SQL 문자열 상수로 migration 관리
- Connection pool 튜닝은 범위 밖
