# e-async-jobs-lab-fastapi 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 작업 enqueue 요청이 idempotency key를 받아야 합니다, outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다, worker가 재시도 가능한 작업을 처리할 수 있어야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `get_jobs_service` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 작업 enqueue 요청이 idempotency key를 받아야 합니다.
- outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다.
- worker가 재시도 가능한 작업을 처리할 수 있어야 합니다.
- 첫 진입점은 `../labs/E-async-jobs-lab/fastapi/app/__init__.py`이고, 여기서 `get_jobs_service` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../labs/E-async-jobs-lab/fastapi/app/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../labs/E-async-jobs-lab/fastapi/app/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/E-async-jobs-lab/fastapi/app/api/deps.py`: `get_jobs_service`가 핵심 흐름과 상태 전이를 묶는다.
- `../labs/E-async-jobs-lab/fastapi/app/api/v1/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/E-async-jobs-lab/fastapi/app/api/v1/router.py`: endpoint와 route 조합을 묶어 외부 진입 경로를 고정하는 파일이다.
- `../labs/E-async-jobs-lab/fastapi/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py`: `test_idempotent_enqueue_and_outbox_drain`, `test_retrying_job_requires_second_drain`가 통과 조건과 회귀 포인트를 잠근다.
- `../labs/E-async-jobs-lab/fastapi/tests/smoke.py`: `main`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../labs/E-async-jobs-lab/fastapi/app/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `app_env` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `app_env`와 `client`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../labs/E-async-jobs-lab/fastapi/app/__init__.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/__init__.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/deps.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/v1/__init__.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/v1/router.py`
- `../labs/E-async-jobs-lab/fastapi/tests/conftest.py`
- `../labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py`
- `../labs/E-async-jobs-lab/fastapi/tests/smoke.py`
- `../labs/E-async-jobs-lab/fastapi/compose.yaml`
- `../labs/E-async-jobs-lab/fastapi/Makefile`
