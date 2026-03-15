# E-async-jobs-lab structure plan

## 한 줄 약속

- 비동기 작업을 큐 기술 소개가 아니라 idempotency와 outbox handoff가 보이는 상태 계약으로 읽게 만든다.

## 독자 질문

- 왜 이 랩은 worker 설정 자체보다 `Idempotency-Key`와 outbox 저장을 먼저 보여 주는가
- drain endpoint가 `.delay(...).get()`으로 다시 기다리는 현재 구조는 무엇을 보여 주고 무엇을 아직 하지 않는가
- retry는 왜 실패 꼬리표가 아니라 정상 상태 전이로 다뤄져야 하는가
- 문제 정의가 말한 `failed` 상태는 현재 구현에서 어디까지 드러나는가
- 현재 문서에 적힌 검증 명령은 지금 셸에서 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- outbox handoff의 선명함과 현재 구현의 빈 구간을 둘 다 숨기지 않는다.

## 글 흐름

1. 문제 정의가 기술 스택보다 handoff boundary를 먼저 묻는다는 점부터 고정한다.
2. enqueue route와 service에서 idempotency 저장 계약을 읽는다.
3. drain route와 worker task에서 outbox handoff가 어떻게 노출되는지 설명한다.
4. retry 상태, eager Celery 테스트 루프, 아직 비어 있는 `failed` 종착지를 함께 정리한다.
5. 오늘 다시 돌린 CLI 결과로 현재 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [JobsService](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py)
- 보조 코드 앵커: [jobs.py route](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py), [tasks.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/workers/tasks.py), [celery_app.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/workers/celery_app.py)
- 테스트 루프 앵커: [conftest.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/conftest.py), [test_async_jobs.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py), [smoke.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/smoke.py)
- 스키마 앵커: [schemas/jobs.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/schemas/jobs.py)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 enqueue 시점 저장 계약, outbox handoff, retry 상태를 아주 적은 모델로 또렷하게 보여 준다는 점이다.
- 이 랩의 현재 한계는 drain endpoint가 아직 결과를 즉시 기다리고, terminal `failed` 상태가 코드에 없으며, 2026-03-14 셸에서는 `app` path와 `email-validator` 의존성 문제로 검증이 바로 닫히지 않는다는 점이다.
- 다음 랩인 `F-realtime-lab`은 이 handoff 사고방식 위에서 연결 상태를 더 즉시적인 채널로 옮겨 가는 비교 대상으로 연결한다.
