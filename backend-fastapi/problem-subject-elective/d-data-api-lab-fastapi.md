# d-data-api-lab-fastapi 문제지

## 왜 중요한가

프로젝트, 태스크, 댓글을 다루는 데이터 중심 API를 만든다고 가정합니다. 단순 CRUD를 넘어서, 목록 조회 조건, 삭제 정책, 동시 수정 충돌 같은 현실적인 데이터 API 문제를 같이 다뤄야 합니다.

## 목표

시작 위치의 구현을 완성해 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다, 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다, 소프트 삭제가 목록 조회에 반영되어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/D-data-api-lab/fastapi/app/__init__.py`
- `../labs/D-data-api-lab/fastapi/app/api/__init__.py`
- `../labs/D-data-api-lab/fastapi/app/api/deps.py`
- `../labs/D-data-api-lab/fastapi/app/api/v1/__init__.py`
- `../labs/D-data-api-lab/fastapi/tests/conftest.py`
- `../labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py`
- `../labs/D-data-api-lab/fastapi/compose.yaml`
- `../labs/D-data-api-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/D-data-api-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다.
- 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다.
- 소프트 삭제가 목록 조회에 반영되어야 합니다.
- 낙관적 락으로 충돌을 감지하는 경로가 있어야 합니다.

## 제외 범위

- 인증과 인가
- 전문 검색이나 대규모 인덱싱
- 복잡한 이벤트 소싱이나 CQRS

## 성공 체크리스트

- 핵심 흐름은 `get_data_service`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `app_env`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/D-data-api-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`d-data-api-lab-fastapi_answer.md`](d-data-api-lab-fastapi_answer.md)에서 확인한다.
