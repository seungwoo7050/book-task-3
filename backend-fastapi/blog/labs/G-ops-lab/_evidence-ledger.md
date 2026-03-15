# G-ops-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/problem/README.md) 가 live/ready, metrics, Compose/CI, AWS target shape 문서를 독립된 성공 기준으로 두고, 통합 테스트와 smoke가 그 surface 일부를 직접 고정한다.
- 프로젝트 질문: 작은 백엔드에서도 어떤 운영 질문을 별도 표면으로 드러내야 하는가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/README.md)
- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/docs/README.md)
- [`docs/aws-deployment.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/docs/aws-deployment.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/README.md)
- [`fastapi/Makefile`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/Makefile)
- [`app/api/v1/routes/health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/health.py)
- [`app/api/v1/routes/ops.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py)
- [`app/main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/main.py)
- [`app/runtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/runtime.py)
- [`app/core/logging.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/core/logging.py)
- [`app/api/deps.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/deps.py)
- [`tests/conftest.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/tests/conftest.py)
- [`tests/integration/test_ops.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/tests/integration/test_ops.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 운영성이 구현 부록이 아니라 독립 질문 묶음인지 먼저 판정한다 | `README.md`, `problem/README.md`, `docs/README.md`, `docs/aws-deployment.md` | live/ready, metrics, Compose/CI, target-shape 문서가 함께 성공 기준으로 제시되지만, AWS 문서는 실제 배포 사실이 아님을 명시한다 | `sed -n '1,240p' backend-fastapi/labs/G-ops-lab/README.md`<br>`sed -n '1,320p' backend-fastapi/labs/G-ops-lab/docs/aws-deployment.md` | 이 랩의 중심은 기능보다 운영 표면과 문서 경계다 | 이제 route와 runtime이 그 표면을 실제로 어떻게 분리하는지 내려가 봐야 한다 |
| 2 | live, dependency-ready, config-ready, metrics를 어떤 surface로 나누는지 확인한다 | `health.py`, `ops.py`, `main.py`, `runtime.py` | `health/live`는 process liveness, `health/ready`는 dependency probe, `ops/ready`는 구성 요약, `ops/metrics`는 request counter 노출을 맡는다 | `rg -n 'live|ready|metrics|request_count|middleware' backend-fastapi/labs/G-ops-lab/fastapi/app` | "ready"도 하나의 의미가 아니라 dependency readiness와 config summary로 나뉜다 | 다음은 logging과 in-memory metrics 모델이 어떤 최소 운영 신호를 남기는지 본다 |
| 3 | 최소 metrics와 JSON logging의 현재 한계를 고정한다 | `runtime.py`, `logging.py`, `main.py` middleware | request counter는 인메모리 state라 재시작 시 초기화되고, JSON 로그는 timestamp/level/logger/message만 남긴다 | `rg -n 'request_count|JsonFormatter|increment' backend-fastapi/labs/G-ops-lab/fastapi/app` | full stack이 아니라 "최소 운영 질문에 답하는 표면"만 남긴 구현이다 | 이제 테스트와 smoke가 이 surface를 실제로 고정하는지 본다 |
| 4 | ops surface가 문서가 아니라 회귀선인지 확인한다 | `test_ops.py`, `smoke.py` | 통합 테스트는 live, `ops/ready`, `ops/metrics`를 호출하고, smoke는 `/health/live`를 빠르게 확인한다 | `sed -n '1,320p' backend-fastapi/labs/G-ops-lab/fastapi/tests/integration/test_ops.py` | 운영성도 endpoint가 아니라 자동 검증 표면과 같이 있어야 유지된다 | 마지막으로 오늘 셸에서 공식 진입점과 보조 재실행이 어디서 갈리는지 닫는다 |
| 5 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, `health.py`, 현재 셸 환경 | lint는 E501에서, 기본 `pytest`는 path에서, `make smoke`는 interpreter에서 막히지만, `PYTHONPATH` 보조 재실행은 테스트와 smoke가 통과한다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint`는 `health.py` E501, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 통과한다 | 문서는 ops surface가 살아 있다는 사실과 기본 진입점 drift를 함께 남겨야 한다 |
