# D-data-api-lab development timeline

이 글은 D 랩을 "엔터티가 세 개 있는 CRUD 예제"로 요약하지 않는다. 현재 남아 있는 source of truth를 따라가면, 이 프로젝트의 핵심은 데이터 계약을 어디까지 API 바깥이 아니라 surface 위로 끌어올릴 것인가에 있다. 실제로 눈에 띄는 건 프로젝트 목록의 filter/sort/page semantics, soft delete, version conflict, 그리고 이 규칙을 빠르게 재실행하게 만드는 SQLite 기반 검증 루프다.

## Phase 1. 문제 정의가 CRUD보다 목록 의미를 먼저 밀어 올린다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/problem/README.md) 와 [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/docs/README.md) 를 먼저 보면, 이 랩이 정말로 묻는 건 "프로젝트/태스크/댓글을 만들 수 있는가"보다 "필터링, 정렬, 페이지네이션, 소프트 삭제, optimistic locking을 어떤 계약으로 설명할 것인가"에 가깝다.

이 순서가 중요하다. CRUD 실습이라면 보통 create/read/update/delete 개수를 세기 쉽지만, D 랩은 처음부터 데이터 API의 설명력을 목록 semantics와 충돌 제어에서 찾는다. 그래서 뒤에서 route와 service를 볼 때도, 생성 endpoint 수보다 어떤 query parameter와 version 필드를 밖으로 드러냈는지가 더 중요해진다.

## Phase 2. 실제 route surface는 프로젝트 contract에 가장 많은 무게를 둔다

[`data_api.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py) 를 보면 이 랩의 중심은 프로젝트다. `POST /projects`, `GET /projects`, `PATCH /projects/{project_id}`, `DELETE /projects/{project_id}`가 있고, task/comment는 각각 하위 생성 endpoint만 있다.

```python
@router.get("/projects", response_model=PageResponse)
def list_projects(
    service: Annotated[DataApiService, Depends(get_data_service)],
    status: str | None = None,
    sort: str = "title",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    include_deleted: bool = False,
) -> PageResponse:
```

여기서 이 랩이 무엇을 surface에 올렸는지가 드러난다. `status`, `sort`, `page`, `page_size`, `include_deleted`는 모두 프로젝트 목록 계약의 일부다. 반면 상위 README가 말한 세 엔터티 CRUD와 달리, 실제 구현은 프로젝트 lifecycle을 중심으로 두고 task/comment는 child creation에 더 가깝게 남겨 둔다.

## Phase 3. version conflict와 soft delete는 서비스 계층에서 규칙으로 닫힌다

실제 데이터 규칙은 [`DataApiService`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/domain/services/data_api.py) 와 [`DataRepository`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/repositories/data_repository.py) 에 모여 있다. `update_project()`는 stale version을 `409 VERSION_CONFLICT`로 막고, `delete_project()`는 hard delete가 아니라 `deleted_at`을 찍고 version을 올린다. 목록 조회 쪽에서는 repository가 `include_deleted` 여부에 따라 `deleted_at is NULL` 조건을 붙였다 떼며 total count까지 같이 계산한다.

```python
if project.version != version:
    raise AppError(
        code="VERSION_CONFLICT",
        message="Project version conflict.",
        status_code=409,
    )
```

이 선택 덕분에 낙관적 락은 저장소 내부 비밀 구현이 아니라, 클라이언트가 알아야 하는 API 계약이 된다. soft delete도 마찬가지다. 삭제가 곧 행 제거가 아니라 목록 의미를 바꾸는 작업이 되면서, 조회 semantics와 수정 충돌이 같은 서사 안으로 들어온다.

## Phase 4. 테스트는 프로젝트 중심 계약과 child resource 비대칭성을 함께 고정한다

[`test_data_api.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py) 는 두 가지를 같이 보여 준다. 첫째, active 목록 필터와 soft delete, `include_deleted=true`, `-title` 정렬이 실제 응답에 어떤 차이를 만드는지 확인한다. 둘째, update 뒤 version이 2로 올라가고, stale version 1 patch는 409로 거절되는지 확인한다.

```python
stale = client.patch(
    f"/api/v1/data/projects/{project['id']}",
    json={"version": 1, "status": "archived"},
)
assert stale.status_code == 409
```

테스트 후반부는 그 위에 task/comment 생성을 이어 붙인다. 이 흐름이 중요한 이유는 D 랩이 세 엔터티 모두의 full CRUD를 끝냈다는 증거가 아니라, 프로젝트 계약을 먼저 고정한 뒤 child resource를 최소 생성 흐름으로 연결했다는 증거이기 때문이다. 문서가 이 차이를 숨기면 실제 구현보다 더 완결된 CRUD 시스템처럼 보이게 된다.

## Phase 5. 학습 루프는 앱 시작 시 스키마 초기화와 SQLite override에 기대고 있다

이 랩의 실행 감각은 [`main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/main.py), [`bootstrap.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/bootstrap.py), [`tests/conftest.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/conftest.py) 를 같이 봐야 보인다. 앱은 lifespan에서 `initialize_schema()`를 호출해 바로 테이블을 만들고, 테스트는 매번 임시 SQLite 파일로 `DATABASE_URL`을 바꾼 뒤 `drop_all/create_all`로 격리된 DB를 다시 세운다.

이 선택은 학습 랩으로서는 꽤 실용적이다. 마이그레이션을 먼저 이해하지 않아도 데이터 계약 실험을 바로 반복할 수 있기 때문이다. 동시에 `ready` endpoint는 DB와 optional Redis까지 확인하지만, smoke는 [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/smoke.py) 에서 `live`만 찍는다. 즉 현재 자동 확인 루프는 실행 가능성 확인에 집중하고, 전체 dependency readiness를 끝까지 밀어붙이지는 않는다.

## Phase 6. 오늘 다시 돌린 검증은 코드 자체보다 진입점 drift를 먼저 보여 준다

2026-03-14 현재 셸에서 다시 실행한 명령은 아래와 같다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇게 갈렸다.

- `make lint`: [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/health.py) 의 한 줄짜리 예외 주석이 `E501`로 실패한다.
- `make test`: `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: Homebrew `python3` 기준 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`: `2 passed`까지 통과하지만 `pytest_asyncio` deprecation warning이 남는다.
- `PYTHONPATH=. python -m tests.smoke`: `/api/v1/health/live` 200으로 통과한다.

즉 D 랩은 이전 몇 개 랩과 달리 코드와 테스트 핵심 경로 자체는 현재 셸에서도 살아 있다. 다만 문서에 적힌 기본 `make` 진입점은 import path와 interpreter 선택 때문에 바로 재현되지 않는다. 이 차이를 남겨야만 "실제 데이터 계약은 통과한다"와 "공식 검증 루프는 아직 정리되지 않았다"를 동시에 전달할 수 있다.

## 정리

D-data-api-lab이 실제로 남기는 건 CRUD endpoint 수가 아니다. 프로젝트 목록 semantics, soft delete, version conflict를 클라이언트가 알아야 하는 데이터 계약으로 올리고, task/comment는 그 아래에 최소 child resource 흐름으로 붙인다. 앱 시작 시 스키마 초기화와 SQLite test harness가 이 계약을 반복 가능하게 만들고, 현재 셸의 진입점 drift는 그 반복 가능성이 어디서 끊기는지를 보여 준다. 다음 E 랩이 비동기 작업으로 넘어갈 때도, 먼저 이런 식으로 "무엇이 이미 확정된 데이터 계약인가"를 드러내 두는 게 왜 중요한지 여기서 미리 보게 된다.
