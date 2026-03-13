# E-async-jobs-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 docs가 idempotency key, outbox handoff, retry 상태를 핵심 개념으로 잡고, `tests/integration/test_async_jobs.py`가 중복 enqueue와 두 번째 drain 필요성을 실제로 검증한다.
- 프로젝트 질문: 알림 작업을 바로 실행하지 않고 뒤로 넘길 때, 어떤 저장과 전달 경계를 드러내야 안전하다고 말할 수 있는가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/E-async-jobs-lab/README.md`
- `labs/E-async-jobs-lab/problem/README.md`
- `labs/E-async-jobs-lab/docs/README.md`
- `labs/E-async-jobs-lab/fastapi/README.md`
- `labs/E-async-jobs-lab/fastapi/Makefile`
- `labs/E-async-jobs-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py`
- `backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py`
- `git log -- backend-fastapi/labs/E-async-jobs-lab`

## 프로젝트 표면 요약
- 문제 요약: 알림이나 후처리처럼 요청-응답 경로에서 바로 끝내기 어려운 작업을 안전하게 뒤로 넘겨야 합니다. 이때 중복 요청, 재시도, 작업 유실을 어떻게 다룰지 명시적인 경계가 필요합니다. 작업 enqueue 요청이 idempotency key를 받아야 합니다. outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 작업 enqueue 요청이 idempotency key를 받아야 합니다. outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다. worker가 재시도 가능한 작업을 처리할 수 있어야 합니다. 작업 상태가 성공, 재시도, 실패를 구분할 수 있어야 합니다.
- 설계 질문: 작업을 바로 실행하지 않고 outbox에 한 번 더 저장하는 이유는 무엇인가 idempotency key는 중복 요청과 어떤 관계가 있는가 retry 가능한 실패와 바로 종료해야 하는 실패는 어떻게 다른가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 요청-응답과 알림 전달을 같은 시점에 끝내지 않는 구조 정리 | README.md, problem/README.md, docs/README.md | worker를 붙이기만 하면 비동기 작업 설명이 끝날 것 | idempotency key, outbox 저장, retry 상태 모델을 성공 기준에 포함 | README의 `make run`, `docker compose up --build` | 문제 정의가 enqueue, outbox, retry 상태를 명시 | problem/README.md 성공 기준 | 비동기 작업의 핵심은 worker 자체보다 handoff boundary를 어디에 두는가다 | route surface와 repository boundary 정리 |
| 2 | Phase 2, route/service/repository 의존성으로 복원 | enqueue와 실제 dispatch를 분리된 API로 고정 | app/api/v1/routes/jobs.py, app/domain/services/jobs.py, app/repositories/jobs_repository.py, app/workers/tasks.py | enqueue endpoint 하나만 있으면 충분할 것 | notification enqueue, outbox drain, job 조회 route를 분리하고 drain에서 Celery task dispatch를 수행 | `make test` | `drain_outbox`가 pending event를 훑어 `deliver_notification.delay`로 넘김 | app/api/v1/routes/jobs.py::drain_outbox | 비동기 작업을 설명하려면 '언제 큐에 넣는가'보다 '언제 outbox를 비우는가'가 더 중요하다 | retry 상태 전이와 중복 요청 흡수 검증 |
| 3 | Phase 3, 테스트가 상태 모델을 굳힘 | 같은 요청 중복 흡수와 두 번째 drain 필요성을 검증 | tests/integration/test_async_jobs.py | 성공 한 번만 보여도 비동기 설명이 충분할 것 | 같은 `Idempotency-Key` 재전송 시 같은 job id 반환, 첫 drain에서 retrying, 두 번째 drain에서 sent가 되도록 테스트화 | `make test` | 첫 drain 후 status=`retrying`, 두 번째 drain 후 status=`sent`, attempt_count=2 | tests/integration/test_async_jobs.py::test_retrying_job_requires_second_drain | retry는 실패의 꼬리가 아니라, 상태 기계에서 처음부터 설명해야 하는 정상 경로다 | 실행/재검증 표면 연결 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | worker와 API가 함께 재실행 가능한 프로젝트임을 확인 | docs/verification-report.md, fastapi/README.md, tools/compose_probe.sh | 단위 테스트만 통과하면 worker 구조도 충분히 설명될 것 | compile, lint, test, smoke, Compose probe를 남기고 API 스키마 자동 초기화 메모를 기록 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/E-async-jobs-lab/fastapi 8003` | 2026-03-09 기준 재검증 통과, API 스키마 자동 초기화 기록 | docs/verification-report.md E-async-jobs-lab 항목 | 비동기 예제도 마지막엔 worker가 붙은 Compose stack 전체로 검증해야 독립성이 생긴다 | 실시간 전달 경계와 비교 |
