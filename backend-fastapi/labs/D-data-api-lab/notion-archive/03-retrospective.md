# Retrospective

## CRUD를 구조적으로 보게 된 것

이 랩 전에는 CRUD를 "4개의 HTTP 메서드를 매핑하는 것"으로만 생각했다. 이 랩을 거치면서 CRUD는 데이터 생명주기의 관리이고, 그 위에 filtering/sorting/pagination은 읽기 모델의 설계이고, optimistic locking은 쓰기 모델의 안전장치라는 구조가 보이기 시작했다.

특히 optimistic locking은 "버전 번호를 비교하는 것"이라는 간단한 메커니즘이지만, 실제로 구현하면 "버전을 언제 증가시킬 것인가", "409를 받은 클라이언트는 어떻게 해야 하는가"라는 후속 질문이 따라온다. 이 후속 질문들이 실무적 감각을 만든다.

## Soft Delete의 양날의 검

soft delete를 도입하면 데이터를 잃지 않는다는 보장이 생기지만, 모든 읽기 쿼리에 `WHERE deleted_at IS NULL` 조건을 빼먹지 않아야 한다는 부담도 생긴다. repository의 `list_projects`에서 `include_deleted` 파라미터를 두어 기본은 숨기고, 필요할 때만 보여주는 방식으로 이 부담을 관리했다.

하지만 cascade soft delete(프로젝트 삭제 시 하위 Task도 soft delete)는 구현하지 않았다. 이것이 실제 서비스에서는 문제가 될 수 있다—프로젝트는 삭제됐는데 그 안의 Task는 여전히 보이는 상태가 되기 때문이다.

## 아직 약한 것들

- **Cursor pagination**: 대규모 데이터에서 OFFSET이 커지면 성능이 급격히 저하된다. 이 랩에서는 다루지 않았지만, 비교 분석이 필요하다.
- **Query complexity**: 현재 필터가 status 하나뿐이다. 다중 필터, 범위 검색, full-text search는 별도 주제다.
- **인증 통합**: 누구든 아무 데이터나 수정할 수 있다. ownership-aware CRUD는 capstone의 영역이다.
- **Batch operations**: 여러 프로젝트를 한 번에 삭제하거나 상태를 변경하는 API는 없다.

## 다시 보고 싶은 것

- cursor pagination과 page pagination의 성능 비교 (PostgreSQL EXPLAIN ANALYZE)
- SQLAlchemy의 `mapper_events`를 활용한 자동 version 증가
- cascade soft delete 전략
