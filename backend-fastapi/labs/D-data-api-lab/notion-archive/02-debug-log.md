# Debug Log

## Schema Bootstrap 문제

이 랩도 C-authorization-lab과 같은 문제를 겪었다. `main.py` startup에서 `bootstrap.initialize_schema()`를 호출하지 않으면, 첫 API 요청에서 테이블이 없다는 에러가 발생한다. 로컬 SQLite에서는 문제가 잘 드러나지 않지만(파일이 자동 생성되므로), Docker Compose의 PostgreSQL에서는 명시적으로 테이블을 만들어야 한다.

compose.yaml의 startup 명령에 `alembic upgrade head`가 포함되어 있지 않기 때문에, bootstrap이 더 중요하다. 해결: startup에서 `initialize_schema()`를 호출하도록 유지.

## Optimistic Locking: version=1로 두 번 업데이트 시

개발 초기에 `update_project`에서 version 검증 후 `project.version += 1`을 commit 전에 하지 않고 commit 후에 하려 한 적이 있었다. 이 경우 `session.refresh(project)` 시점에 version이 아직 증가하지 않은 상태로 반환된다. 해결: version 증가를 commit 전에 수행.

또한 두 클라이언트가 version=1을 읽고 동시에 업데이트를 시도하면, 첫 번째는 성공하고(version → 2), 두 번째는 version=1로 시도하므로 `project.version != version` 조건에 걸려 409를 반환한다. 이것이 테스트에서 `stale.status_code == 409`로 검증되는 시나리오다.

## Soft Delete된 프로젝트에 Task 생성 시도

`create_task`에서 프로젝트를 조회한 뒤 `project.deleted_at is not None`을 체크하지 않으면, soft delete된 프로젝트에도 Task가 생성될 수 있다. 이것은 "삭제된 프로젝트"의 의미가 코드에서 일관되지 않은 것이다. 서비스 레이어에서 `project is None or project.deleted_at is not None` 두 조건을 모두 확인하도록 수정했다.
