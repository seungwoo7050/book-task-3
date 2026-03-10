# Knowledge Index

## Optimistic Locking (낙관적 잠금)

동시 수정 시 데이터 충돌을 감지하는 패턴이다. 네 대로 잠금(pessimistic locking)이 레코드를 읽을 때 DB 레벨에서 행을 잠그는 것과 달리, optimistic locking은 **수정할 때** 버전을 비교한다.

작동 방식:
1. 레코드를 읽을 때 현재 version(예: 1)을 함께 반환
2. 수정 요청에 그 version을 포함
3. 서비스 레이어에서 DB의 현재 version과 비교
4. 일치하면 수정 + version 증가 → 200
5. 불일치하면 → 409 Conflict

이 랩의 구현:
```python
if project.version != version:
    raise AppError(code="VERSION_CONFLICT", status_code=409)
project.title = new_title
project.version += 1
session.commit()
```

장점: DB 레벨 잠금이 없어 처리량(throughput)이 높다. 대부분의 웹 요청에서 동시 수정은 드물기 때문에 낙관적 접근이 맞다.
단점: 충돌이 잦은 환경에서는 재시도가 반복되어 오히려 비효율적이다.

## Soft Delete (논리 삭제)

레코드를 물리적으로 삭제하지 않고 `deleted_at` 타임스탬프를 기록하는 패턴이다.

장점:
- 데이터 복구 가능
- 감사 추적(audit trail) 유지
- FK 참조 무결성 유지 (cascade delete로 인한 연쇄 삭제 방지)

단점:
- 모든 읽기 쿼리에 `WHERE deleted_at IS NULL` 조건 필요
- 데이터가 실제로 줄지 않아 디스크/성능 부담
- cascade soft delete를 ORM이 자동으로 해주지 않음

이 랩의 구현:
```python
# 삭제
project.deleted_at = datetime.now(UTC)
project.version += 1  # 삭제도 변경이므로 version 증가

# 조회
if not include_deleted:
    stmt = stmt.where(Project.deleted_at.is_(None))
```

## Page-Based Pagination

OFFSET + LIMIT 기반의 목록 분할 방식이다.

```sql
SELECT * FROM projects
WHERE deleted_at IS NULL AND status = 'active'
ORDER BY title ASC
OFFSET 0 LIMIT 20;
```

핵심 반환값: `items` (현재 페이지 데이터) + `total` (전체 카운트). 클라이언트는 `total / page_size`로 총 페이지 수를 계산한다.

한계: OFFSET이 커지면 DB가 앞의 모든 행을 스캔한 뒤 버려야 하므로 성능이 저하된다. 10만 행에서 `OFFSET 99000`은 99000행을 읽고 버린다. 이 문제를 해결하는 것이 cursor-based pagination이지만, 이 랩에서는 개념 이해를 위해 page-based를 먼저 다룬다.

## Aggregate Boundary

함께 일관성 규칙을 지켜야 하는 도메인 객체의 묶음이다. 이 랩에서 Project → Task → Comment가 하나의 aggregate tree다.

규칙:
- Project 없이 Task는 존재할 수 없다 (FK, ondelete=CASCADE)
- Task 없이 Comment는 존재할 수 없다
- soft-deleted Project에 새 Task를 생성할 수 없다 (서비스 레이어 검증)

이 규칙들이 DB 레벨(FK)과 서비스 레벨(비즈니스 로직)에 분산되어 있다는 것 자체가 학습 포인트다.
