# E-async-jobs-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/problem/README.md) 가 idempotency, outbox, retry 상태를 독립된 성공 기준으로 제시하고, 통합 테스트가 중복 enqueue와 두 번째 drain 필요성을 직접 고정한다.
- 프로젝트 질문: 요청-응답 밖으로 작업을 밀어낼 때 어떤 저장과 상태 전이를 먼저 계약으로 드러내야 하는가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/README.md)
- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/docs/README.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/README.md)
- [`fastapi/Makefile`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/Makefile)
- [`app/api/v1/routes/jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py)
- [`app/domain/services/jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py)
- [`app/repositories/jobs_repository.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/repositories/jobs_repository.py)
- [`app/db/models/jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/db/models/jobs.py)
- [`app/schemas/jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/schemas/jobs.py)
- [`app/workers/celery_app.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/workers/celery_app.py)
- [`app/workers/tasks.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/workers/tasks.py)
- [`tests/conftest.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/conftest.py)
- [`tests/integration/test_async_jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 비동기 작업이 worker 소개보다 handoff boundary 문제인지 먼저 판정한다 | `README.md`, `problem/README.md`, `docs/README.md` | 성공 기준이 queue 기술보다 idempotency, outbox, retry 상태를 먼저 요구한다 | `sed -n '1,240p' backend-fastapi/labs/E-async-jobs-lab/README.md`<br>`sed -n '1,260p' backend-fastapi/labs/E-async-jobs-lab/problem/README.md` | 이 랩의 중심은 "나중에 한다"가 아니라 언제 무엇을 저장하는가다 | 이제 route와 service가 그 경계를 실제로 어디에 두는지 내려가 봐야 한다 |
| 2 | enqueue와 drain이 어떤 API 계약으로 분리되는지 확인한다 | `jobs.py`, `jobs.py` schema, worker task | enqueue는 `Idempotency-Key`를 받고, drain은 pending/retrying outbox event를 Celery task로 넘긴 뒤 결과를 기다린다 | `rg -n 'Idempotency-Key|delay\\(|EmailStr|retrying' backend-fastapi/labs/E-async-jobs-lab/fastapi/app` | handoff는 분명하지만 drain endpoint는 아직 동기 대기까지 포함한다 | 다음은 상태 전이와 현재 비어 있는 failure 종착지를 서비스 계층에서 확인한다 |
| 3 | idempotency와 retry 상태를 서비스 규칙으로 고정한다 | `JobsService`, `JobsRepository`, model | 중복 key는 기존 job을 반환하고, 새 job은 outbox event를 함께 만든다. 상태는 `queued -> retrying -> sent`로 읽힌다 | `rg -n 'queued|retrying|sent|failed' backend-fastapi/labs/E-async-jobs-lab/fastapi/app` | retry는 정상 상태 전이지만 `failed`는 현재 코드에 보이지 않는다 | 이제 테스트가 이 상태 전이를 어떻게 학습 가능한 동기 루프로 바꾸는지 확인한다 |
| 4 | eager Celery와 memory broker가 학습 루프를 어떻게 만드는지 확인한다 | `conftest.py`, `test_async_jobs.py`, `smoke.py` | 테스트는 eager Celery, memory broker, 임시 SQLite DB를 써서 두 번 drain하는 흐름을 실제 요청으로 고정한다 | `sed -n '1,260p' backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/conftest.py`<br>`sed -n '1,360p' backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py` | 비동기 경계가 완전히 숨지 않고, 동기 테스트 루프 안에서 관찰 가능하게 접혀 있다 | 마지막으로 오늘 셸에서 공식 진입점과 보조 재실행이 어디서 막히는지 닫는다 |
| 5 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, `schemas/jobs.py`, 현재 셸 환경 | lint는 통과하지만 기본 `pytest`는 path에서, `PYTHONPATH` 보조 재실행은 `email-validator`에서 멈춘다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint` 통과, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 `email-validator` 부재로 실패한다 | 문서는 구현 구조와 현재 런타임 의존성 drift를 함께 남겨야 한다 |
