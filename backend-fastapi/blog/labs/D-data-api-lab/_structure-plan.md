# D-data-api-lab structure plan

## 한 줄 약속

- 데이터 API를 엔터티 개수보다 목록 semantics와 version conflict가 먼저 보이는 계약으로 읽게 만든다.

## 독자 질문

- 왜 이 랩은 세 엔터티 CRUD보다 `page`, `sort`, `include_deleted`, `version`을 먼저 보여 주는가
- 프로젝트 lifecycle과 task/comment child resource 사이의 비대칭성은 무엇을 말해 주는가
- soft delete와 optimistic locking은 왜 같은 문서 안에서 같이 설명되어야 하는가
- 앱 시작 시 스키마 초기화와 테스트용 SQLite override는 이 랩의 학습 루프를 어떻게 바꾸는가
- 현재 문서에 적힌 검증 명령은 지금 셸에서 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- 상위 README의 넓은 설명과 실제 구현의 좁은 route surface 차이도 숨기지 않는다.

## 글 흐름

1. 문제 정의가 CRUD보다 데이터 계약을 먼저 묻는다는 점부터 고정한다.
2. 프로젝트 route contract에서 filter/sort/page/version을 읽는다.
3. service/repository에서 soft delete와 conflict detection을 규칙으로 연결한다.
4. task/comment가 child create 위주로 남아 있는 현재 구현 범위를 테스트와 함께 설명한다.
5. schema auto-init, SQLite test harness, 오늘 다시 돌린 CLI 결과로 현재 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [DataApiService](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/domain/services/data_api.py)
- 보조 코드 앵커: [data_api.py route](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py), [data_repository.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/repositories/data_repository.py)
- 실행 루프 앵커: [bootstrap.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/app/bootstrap.py), [conftest.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/conftest.py), [smoke.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/smoke.py)
- 테스트 앵커: [test_data_api.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 프로젝트 목록 semantics, soft delete, version conflict를 클라이언트가 알아야 하는 데이터 계약으로 선명하게 드러낸다는 점이다.
- 이 랩의 현재 한계는 상위 문서가 암시하는 세 엔터티 full CRUD보다 실제 구현 표면이 더 좁고, 공식 `make` 진입점은 2026-03-14 셸에서 그대로 닫히지 않는다는 점이다.
- 다음 랩인 `E-async-jobs-lab`은 이 데이터 계약 위에서 요청-응답 밖으로 작업을 밀어내는 비교 대상으로 연결한다.
