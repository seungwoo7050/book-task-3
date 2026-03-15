# e-async-jobs-lab-fastapi 문제지

## 왜 중요한가

알림이나 후처리처럼 요청-응답 경로에서 바로 끝내기 어려운 작업을 안전하게 뒤로 넘겨야 합니다. 이때 중복 요청, 재시도, 작업 유실을 어떻게 다룰지 명시적인 경계가 필요합니다.

## 목표

시작 위치의 구현을 완성해 작업 enqueue 요청이 idempotency key를 받아야 합니다, outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다, worker가 재시도 가능한 작업을 처리할 수 있어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/E-async-jobs-lab/fastapi/app/__init__.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/__init__.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/deps.py`
- `../labs/E-async-jobs-lab/fastapi/app/api/v1/__init__.py`
- `../labs/E-async-jobs-lab/fastapi/tests/conftest.py`
- `../labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py`
- `../labs/E-async-jobs-lab/fastapi/compose.yaml`
- `../labs/E-async-jobs-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/E-async-jobs-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 작업 enqueue 요청이 idempotency key를 받아야 합니다.
- outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다.
- worker가 재시도 가능한 작업을 처리할 수 있어야 합니다.
- 작업 상태가 성공, 재시도, 실패를 구분할 수 있어야 합니다.

## 제외 범위

- 대규모 메시징 시스템 비교
- 고급 스케줄링과 운영 대시보드
- 실서비스 수준의 분산 장애 복구 실험

## 성공 체크리스트

- 핵심 흐름은 `get_jobs_service`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `app_env`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/E-async-jobs-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`e-async-jobs-lab-fastapi_answer.md`](e-async-jobs-lab-fastapi_answer.md)에서 확인한다.
