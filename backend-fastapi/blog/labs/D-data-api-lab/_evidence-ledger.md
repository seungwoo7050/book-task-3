# D-data-api-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/problem/README.md) 가 데이터 API 성공 기준을 CRUD보다 넓게 정의하고, 통합 테스트가 soft delete, filtering, stale version 409, child resource 생성을 한 흐름으로 직접 고정한다.
- 프로젝트 질문: 데이터 중심 API에서 어떤 규칙을 클라이언트가 알아야 하는 surface로 올릴 것인가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/README.md)
- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/docs/README.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/README.md)
- [`fastapi/Makefile`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/Makefile)
- [`app/api/v1/routes/data_api.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py)
- [`app/domain/services/data_api.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/domain/services/data_api.py)
- [`app/repositories/data_repository.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/repositories/data_repository.py)
- [`app/db/models/data.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/db/models/data.py)
- [`app/bootstrap.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/bootstrap.py)
- [`app/main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/main.py)
- [`tests/conftest.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/conftest.py)
- [`tests/integration/test_data_api.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CRUD보다 넓은 데이터 API 질문인지 먼저 판정한다 | `README.md`, `problem/README.md`, `docs/README.md` | 성공 기준이 생성/조회보다 filtering, sorting, pagination, soft delete, optimistic locking을 먼저 밀어 올린다 | `sed -n '1,220p' backend-fastapi/labs/D-data-api-lab/README.md`<br>`sed -n '1,260p' backend-fastapi/labs/D-data-api-lab/problem/README.md` | 이 랩의 중심은 엔터티 수가 아니라 데이터 계약의 의미다 | 이제 실제 route가 그 계약을 어디까지 surface에 올렸는지 내려가 봐야 한다 |
| 2 | route와 schema가 실제로 무엇을 노출하는지 확인한다 | `data_api.py`, `data_api.py` schema | 프로젝트에는 create/list/update/delete가 있고, task/comment는 child create만 존재한다 | `rg -n '/projects|/tasks|/comments|page_size|include_deleted|version' backend-fastapi/labs/D-data-api-lab/fastapi/app` | 상위 README보다 실제 구현은 프로젝트 lifecycle에 더 무게를 둔다 | 다음은 soft delete와 version conflict가 서비스 계층에서 어떻게 강제되는지 본다 |
| 3 | 목록 의미와 충돌 제어를 서비스 규칙으로 고정한다 | `DataApiService`, `DataRepository`, model | `deleted_at` 기반 soft delete, `VERSION_CONFLICT` 409, title 기준 정렬, total count 계산이 한 경로로 묶인다 | `rg -n 'deleted_at|VERSION_CONFLICT|include_deleted|sort' backend-fastapi/labs/D-data-api-lab/fastapi/app` | 조회 semantics와 수정 충돌이 같은 데이터 계약 안에 있다 | 이제 테스트가 이 규칙을 어떤 요청 순서로 회귀선으로 남기는지 확인한다 |
| 4 | 프로젝트 중심 계약과 child resource 비대칭성을 테스트에서 확인한다 | `test_data_api.py`, `bootstrap.py`, `conftest.py`, `smoke.py` | soft delete 뒤 목록 숨김, `include_deleted` 재노출, stale 409, task/comment 생성, SQLite 기반 격리 DB 재생성이 모두 확인된다 | `sed -n '1,360p' backend-fastapi/labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py` | 이 랩의 학습 루프는 스키마 자동 초기화와 임시 SQLite DB에 강하게 기대고 있다 | 마지막으로 오늘 셸에서 공식 진입점과 보조 재실행이 어떻게 갈리는지 닫는다 |
| 5 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, `health.py`, 현재 셸 환경 | 공식 `make` 진입점은 path/interpreter 문제를 먼저 드러내고, `PYTHONPATH` 보조 재실행은 실제 기능 테스트까지 통과한다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint`는 `health.py` E501, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 통과한다 | 문서는 "기능 계약은 살아 있지만 공식 진입점은 drift가 있다"는 두 사실을 함께 남겨야 한다 |
