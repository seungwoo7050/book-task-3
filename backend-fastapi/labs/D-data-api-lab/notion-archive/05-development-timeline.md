# Development Timeline

## Phase 1: 프로젝트 초기 세팅

```bash
mkdir -p labs/D-data-api-lab/fastapi
cd labs/D-data-api-lab/fastapi

# pyproject.toml 작성 후 설치
python3 -m pip install -e ".[dev]"
```

의존성은 C-authorization-lab과 비슷한 구성. 인증 관련 패키지(`PyJWT`, `pyotp`, `itsdangerous`)가 없다.

패키지 구조:
```
app/
  api/v1/routes/
    data_api.py         # CRUD + filter + sort + pagination endpoints
    health.py
  core/
    config.py, errors.py, logging.py
  db/models/
    data.py             # Project, Task, Comment
  domain/services/
    data_api.py         # DataApiService
  repositories/
    data_repository.py  # 쿼리 로직 분리
  schemas/
    data_api.py         # Request/Response Models + PageResponse
  bootstrap.py
  main.py
```

## Phase 2: 데이터 모델 설계

3개 테이블: projects, tasks, comments.

핵심 설계 결정:
- `Project.version` (Integer, default=1): optimistic locking용
- `Project.deleted_at` (DateTime nullable): soft delete용
- `Task.deleted_at`: Task도 soft delete 가능
- `Task.priority` (Integer): 정렬/필터 확장 가능성
- `Comment.body` (Text): 긴 텍스트 허용
- FK에 `ondelete="CASCADE"`: 물리 삭제 시 cascade

```python
class Project(TimestampMixin, Base):
    title: Mapped[str]
    status: Mapped[str]      # "active", "archived" 등
    version: Mapped[int]     # optimistic locking
    deleted_at: Mapped[datetime | None]  # soft delete
```

## Phase 3: Repository - 쿼리 로직 분리

`DataRepository.list_projects`의 구현:

```python
stmt = select(Project)
count_stmt = select(func.count(Project.id))

# 1. status 필터
if status:
    stmt = stmt.where(Project.status == status)
    count_stmt = count_stmt.where(Project.status == status)

# 2. soft delete 필터
if not include_deleted:
    stmt = stmt.where(Project.deleted_at.is_(None))

# 3. 정렬
order = desc(Project.title) if sort == "-title" else asc(Project.title)
stmt = stmt.order_by(order)

# 4. 페이지네이션
stmt = stmt.offset((page - 1) * page_size).limit(page_size)
```

items와 total을 별도 쿼리로 반환. total은 `func.count()`로 전체 조건에 맞는 레코드 수를 계산.

## Phase 4: Service Layer - 비즈니스 규칙

`DataApiService` 핵심 메서드:
- `update_project`: version 비교 → 불일치 시 409 → 일치 시 업데이트 + version 증가
- `delete_project`: `deleted_at = datetime.now(UTC)`, version도 증가
- `create_task`: 대상 프로젝트가 존재하고 soft-deleted가 아닌지 확인
- `create_comment`: 대상 Task가 존재하고 soft-deleted가 아닌지 확인

## Phase 5: API 엔드포인트

```
POST   /api/v1/data/projects                          → 프로젝트 생성
GET    /api/v1/data/projects?status=&sort=&page=&page_size=&include_deleted=  → 목록 조회
PATCH  /api/v1/data/projects/{id}                      → 프로젝트 수정 (version 필수)
DELETE /api/v1/data/projects/{id}                      → soft delete
POST   /api/v1/data/projects/{id}/tasks                → Task 생성
POST   /api/v1/data/tasks/{task_id}/comments           → Comment 생성
```

페이지네이션 쿼리 파라미터 검증:
```python
page: int = Query(default=1, ge=1)
page_size: int = Query(default=20, ge=1, le=100)
```

## Phase 6: Docker Compose 구성

```yaml
services:
  api:    # port 8002:8000
  db:     # PostgreSQL 16, POSTGRES_DB=d_data_api_lab, port 5434:5432
```

Redis 없음. 인증/세션 관리가 없기 때문.

```bash
docker compose up --build -d
curl -s http://localhost:8002/api/v1/health/live
```

## Phase 7: Alembic 마이그레이션

```bash
alembic revision -m "initial data schema"
alembic upgrade head

# 테이블 확인
docker compose exec db psql -U postgres -d d_data_api_lab -c "\\dt"
```

3개 테이블 생성: projects, tasks, comments.

## Phase 8: 테스트 작성 및 실행

두 개의 통합 테스트:

1. **filter-sort-pagination-soft-delete**: 3개 프로젝트 생성 → status=active 필터 → page_size=1로 첫 페이지 → total=2 확인 → Beta soft delete → active 목록에서 제외 확인 → include_deleted=true로 전체 확인

2. **optimistic-locking-task-comment**: 프로젝트 생성(v1) → 수정(v1→v2) → stale update(v1으로 시도→409) → Task 생성 → Comment 생성

```bash
make test
make lint
make smoke
```

## Phase 9: 최종 검증

```bash
make install
make lint
make test
make smoke

docker compose up --build -d
curl -sf http://localhost:8002/api/v1/health/live
docker compose down
```
