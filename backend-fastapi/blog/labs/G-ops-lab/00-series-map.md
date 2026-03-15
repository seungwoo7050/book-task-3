# G-ops-lab series map

이 시리즈는 G 랩을 "운영 문서가 붙은 마무리 예제"로 읽지 않는다. 실제 source of truth를 따라가 보면 이 프로젝트의 중심은 live, dependency-ready, config-ready, request counter, JSON logging, target-shape 문서를 서로 다른 표면으로 나눠서 과장 없이 설명하는 데 있다.

## 이 시리즈가 붙잡는 질문

- 작은 학습용 백엔드에서도 `alive`, `dependencies ready`, `configuration summary`를 왜 분리해서 보여 줘야 하는가
- 최소 metrics는 어떤 운영 질문까지만 답해야 하고, 어디서부터 full observability stack 이야기가 되는가
- request counter가 인메모리 state에 있을 때 무엇을 보여 주고 무엇을 아직 보여 주지 못하는가
- AWS 문서는 어디까지 사실이고 어디부터 target shape 가정인가

## 왜 이 순서로 읽는가

1. `problem/README.md`, `docs/README.md`, `docs/aws-deployment.md`로 이 랩이 배포 자동화가 아니라 운영 surface와 문서 경계를 먼저 묻는다는 점을 확인한다.
2. `health.py`, `ops.py`, `main.py`, `runtime.py`를 보며 live, dependency-ready, config-ready, metrics가 각각 어떤 표면으로 나뉘는지 확인한다.
3. `logging.py`와 middleware를 보며 JSON 로그와 request counter가 어떤 최소 운영 신호를 남기는지 본다.
4. 통합 테스트와 smoke를 함께 보며 지금 셸에서 어떤 surface가 실제로 재현되고, 공식 `make` 진입점은 어디서 끊기는지 확인한다.
5. 마지막에 현재 검증 결과를 붙여 "구현된 운영 surface"와 "문서로만 남은 deployment shape"를 분리해서 닫는다.

## 근거로 사용한 자료

- `backend-fastapi/labs/G-ops-lab/README.md`
- `backend-fastapi/labs/G-ops-lab/problem/README.md`
- `backend-fastapi/labs/G-ops-lab/docs/README.md`
- `backend-fastapi/labs/G-ops-lab/docs/aws-deployment.md`
- `backend-fastapi/labs/G-ops-lab/fastapi/README.md`
- `backend-fastapi/labs/G-ops-lab/fastapi/Makefile`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/health.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/main.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/runtime.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/core/logging.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/api/deps.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/tests/conftest.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/tests/integration/test_ops.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/health.py) 의 긴 예외 주석 한 줄 때문에 `E501`로 실패했다.
- 같은 날짜 `make test`는 `tests/conftest.py` import 시점에 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 타면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`를 다시 돌리면 통합 테스트 1개가 통과한다. 다만 `pytest_asyncio`는 `asyncio_default_fixture_loop_scope` 미설정 deprecation warning을 남긴다.
- `PYTHONPATH=. python -m tests.smoke`도 `/api/v1/health/live` 200으로 통과한다.
- 즉 ops surface 자체는 현재 셸에서도 살아 있지만, 공식 `make` 진입점은 여전히 import path와 interpreter 선택에 영향을 받는다.

## 현재 구현에서 좁게 남은 부분

- `health/ready`는 실제 DB ping과 optional Redis ping을 확인하지만, `ops/ready`는 dependency probe가 아니라 설정값이 있는지 없는지의 요약을 반환한다.
- request counter는 [`MetricsRegistry`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/runtime.py) 에 인메모리로 유지되므로 프로세스 재시작 시 초기화된다.
- 미들웨어가 `call_next` 전에 카운터를 올리기 때문에, `metrics` 요청 자체도 카운트에 포함된다고 읽을 수 있다. 이는 코드에서의 추론이다.
- AWS 문서는 실제 배포 완료 기록이 아니라 target shape 설명으로만 남아 있다.

## 현재 범위 밖

- 풀 observability stack 구축
- IaC로 실제 인프라를 생성하는 자동화
- 장시간 부하 테스트와 장애 주입 실험

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - live/ready 분리, config-ready 요약, in-memory metrics, target-shape 문서 경계를 구현 순서로 복원한다.
