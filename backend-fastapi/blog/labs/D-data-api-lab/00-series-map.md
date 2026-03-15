# D-data-api-lab series map

이 시리즈는 D 랩을 "프로젝트, 태스크, 댓글 CRUD"라는 표면만으로 읽지 않는다. 실제 source of truth를 따라가 보면 이 프로젝트의 중심은 프로젝트 목록 semantics, 소프트 삭제, 버전 충돌, 그리고 테스트 가능한 데이터 계약을 얼마나 단순하게 드러내는가에 있다.

## 이 시리즈가 붙잡는 질문

- 데이터 중심 API에서 무엇을 먼저 계약으로 올려야 하는가. 엔터티 수인가, 아니면 목록 의미와 충돌 규칙인가
- `page`, `page_size`, `sort`, `include_deleted`, `version` 같은 값은 어디까지 API surface에 노출돼야 하는가
- 상위 README가 말하는 세 엔터티 CRUD와 실제 route/service 구현 사이에는 어떤 차이가 남아 있는가
- 앱 시작 시 스키마 초기화와 테스트용 SQLite override는 이 랩의 학습 방식을 어떻게 바꾸는가

## 왜 이 순서로 읽는가

1. `problem/README.md`와 `docs/README.md`로 이 랩이 CRUD 개수보다 목록 조건, 삭제 정책, optimistic locking을 더 먼저 묻는다는 점을 확인한다.
2. `data_api.py` route와 schema를 보며 실제 API surface가 프로젝트 lifecycle과 하위 task/comment 생성으로 어떻게 나뉘는지 본다.
3. `DataApiService`, `DataRepository`, SQLAlchemy model을 따라가며 soft delete와 version conflict가 어디서 강제되는지 확인한다.
4. 통합 테스트와 `bootstrap.py`, `conftest.py`, `smoke.py`를 함께 보며 이 계약이 어떤 SQLite 기반 학습 루프 위에서 검증되는지 확인한다.
5. 마지막에 `make lint`, `make test`, `make smoke`와 보조 재실행 결과를 붙여 현재 셸 기준 재현 가능 상태를 닫는다.

## 근거로 사용한 자료

- `backend-fastapi/labs/D-data-api-lab/README.md`
- `backend-fastapi/labs/D-data-api-lab/problem/README.md`
- `backend-fastapi/labs/D-data-api-lab/docs/README.md`
- `backend-fastapi/labs/D-data-api-lab/fastapi/README.md`
- `backend-fastapi/labs/D-data-api-lab/fastapi/Makefile`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/domain/services/data_api.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/repositories/data_repository.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/db/models/data.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/schemas/data_api.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/bootstrap.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/main.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/tests/conftest.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/health.py) 의 긴 예외 주석 한 줄 때문에 `E501`로 실패했다.
- 같은 날짜 `make test`는 `tests/conftest.py` import 시점에 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 타면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`를 다시 돌리면 `2 passed`까지는 통과한다. 다만 `pytest_asyncio`는 `asyncio_default_fixture_loop_scope` 미설정 deprecation warning을 남긴다.
- `PYTHONPATH=. python -m tests.smoke`는 현재 셸에서 `/api/v1/health/live` 200까지 통과한다.
- 즉 이 랩의 코드와 테스트 계약은 살아 있지만, 공식 `make` 진입점은 여전히 path와 interpreter drift를 안고 있다.

## 현재 구현에서 좁게 남은 부분

- README는 세 엔터티 CRUD를 말하지만, 실제 route surface는 프로젝트 쪽에만 list/update/delete를 두고 task/comment는 생성 endpoint만 둔다.
- 소프트 삭제와 목록 조건도 현재는 프로젝트에만 직접 연결된다.
- `ready` endpoint는 DB와 optional Redis를 확인하지만, smoke test는 `live`만 확인한다.

## 현재 범위 밖

- 인증과 인가
- 전문 검색이나 대규모 인덱싱
- 복잡한 이벤트 소싱이나 CQRS

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - 프로젝트 중심 데이터 계약, child resource 비대칭성, SQLite 기반 검증 루프를 구현 순서로 복원한다.
