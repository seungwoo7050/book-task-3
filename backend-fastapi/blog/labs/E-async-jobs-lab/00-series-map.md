# E-async-jobs-lab series map

이 시리즈는 E 랩을 "Celery 붙인 예제"로 읽지 않는다. 실제 source of truth를 따라가 보면 이 프로젝트의 핵심은 요청 시점에 무엇을 저장하고, 언제 outbox를 비우고, 어떤 상태를 재시도로 남길지를 API와 모델에 얼마나 노골적으로 드러내는가에 있다.

## 이 시리즈가 붙잡는 질문

- 비동기 작업에서 200 응답 전에 무엇까지 확정해야 하는가
- `Idempotency-Key`는 중복 요청 방지 이상의 어떤 저장 계약이 되는가
- outbox handoff는 어디서 시작되고, 현재 구현은 왜 `delay(...).get()`으로 다시 동기적으로 닫히는가
- 문제 정의가 말하는 성공/재시도/실패 상태 가운데 실제 코드가 선명하게 드러내는 건 어디까지인가

## 왜 이 순서로 읽는가

1. `problem/README.md`와 `docs/README.md`로 이 랩이 worker 기술보다 handoff boundary와 retry 상태를 더 먼저 묻는다는 점을 확인한다.
2. `jobs.py` route, schema, Celery task를 보며 enqueue, drain, status 조회가 어떻게 나뉘는지 확인한다.
3. `JobsService`, `JobsRepository`, model을 따라가며 idempotency dedupe, outbox event 생성, `queued -> retrying -> sent` 전이를 확인한다.
4. 통합 테스트와 `conftest.py`, `smoke.py`를 함께 보며 eager Celery와 memory broker가 이 비동기 경계를 어떻게 학습 가능한 동기 루프로 바꾸는지 본다.
5. 마지막에 `make lint`, `make test`, `make smoke`와 보조 재실행 결과를 붙여 현재 셸 기준 재현 가능 상태를 닫는다.

## 근거로 사용한 자료

- `backend-fastapi/labs/E-async-jobs-lab/README.md`
- `backend-fastapi/labs/E-async-jobs-lab/problem/README.md`
- `backend-fastapi/labs/E-async-jobs-lab/docs/README.md`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/README.md`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/Makefile`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/repositories/jobs_repository.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/db/models/jobs.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/schemas/jobs.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/workers/celery_app.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/workers/tasks.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/conftest.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 현재 셸에서 통과했다.
- 같은 날짜 `make test`는 `tests/conftest.py` import 시점에 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 타면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`를 다시 돌리면 [`schemas/jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/schemas/jobs.py) 의 `EmailStr`가 기대하는 `email-validator` 부재 때문에 테스트 진입 전에 멈춘다.
- `PYTHONPATH=. python -m tests.smoke`도 같은 `email-validator` import 오류에서 멈춘다.
- 즉 lint 수준 정합성은 좋지만, 현재 셸에서 실제 앱 import를 끝까지 밀어붙이려면 path와 Python dependency가 더 정리돼야 한다.

## 현재 구현에서 좁게 남은 부분

- outbox handoff는 분명하지만, `drain_outbox()`는 [`deliver_notification.delay(event.id).get()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py) 으로 결과를 즉시 기다린다. 즉 현재 API edge는 완전히 fire-and-forget으로 열려 있지 않다.
- 상태 모델은 `queued`, `retrying`, `sent`가 선명하지만, 문제 정의가 말한 terminal `failed` 상태는 코드에 직접 드러나지 않는다.
- 같은 `Idempotency-Key` 재전송은 기존 job을 돌려주지만, payload mismatch 처리 규칙은 현재 surface에 없다.

## 현재 범위 밖

- 대규모 메시징 시스템 비교
- 고급 스케줄링과 운영 대시보드
- 실서비스 수준의 분산 장애 복구 실험

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - enqueue 저장 계약, outbox drain, eager Celery 기반 학습 루프, 현재 verification drift를 구현 순서로 복원한다.
