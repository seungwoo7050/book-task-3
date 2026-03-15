# d-data-api-lab-fastapi 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다, 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다, 소프트 삭제가 목록 조회에 반영되어야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `get_data_service` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다.
- 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다.
- 소프트 삭제가 목록 조회에 반영되어야 합니다.
- 첫 진입점은 `../labs/D-data-api-lab/fastapi/app/__init__.py`이고, 여기서 `get_data_service` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../labs/D-data-api-lab/fastapi/app/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../labs/D-data-api-lab/fastapi/app/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/D-data-api-lab/fastapi/app/api/deps.py`: `get_data_service`가 핵심 흐름과 상태 전이를 묶는다.
- `../labs/D-data-api-lab/fastapi/app/api/v1/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/D-data-api-lab/fastapi/app/api/v1/router.py`: endpoint와 route 조합을 묶어 외부 진입 경로를 고정하는 파일이다.
- `../labs/D-data-api-lab/fastapi/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py`: `test_filter_sort_pagination_and_soft_delete`, `test_optimistic_locking_and_task_comment_creation`가 통과 조건과 회귀 포인트를 잠근다.
- `../labs/D-data-api-lab/fastapi/tests/smoke.py`: `main`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../labs/D-data-api-lab/fastapi/app/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `app_env` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && PYTHONPATH=. python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `app_env`와 `client`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && PYTHONPATH=. python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../labs/D-data-api-lab/fastapi/app/__init__.py`
- `../labs/D-data-api-lab/fastapi/app/api/__init__.py`
- `../labs/D-data-api-lab/fastapi/app/api/deps.py`
- `../labs/D-data-api-lab/fastapi/app/api/v1/__init__.py`
- `../labs/D-data-api-lab/fastapi/app/api/v1/router.py`
- `../labs/D-data-api-lab/fastapi/tests/conftest.py`
- `../labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py`
- `../labs/D-data-api-lab/fastapi/tests/smoke.py`
- `../labs/D-data-api-lab/fastapi/compose.yaml`
- `../labs/D-data-api-lab/fastapi/Makefile`
