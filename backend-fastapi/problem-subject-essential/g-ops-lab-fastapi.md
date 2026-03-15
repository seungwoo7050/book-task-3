# g-ops-lab-fastapi 문제지

## 왜 중요한가

기능은 단순해도, 백엔드가 어떻게 살아 있는지 확인하고 어떻게 배포 가정을 설명할지 정리해야 합니다. health check, readiness, metrics, CI, 배포 문서는 개발용 API와 별개의 운영성 문제입니다.

## 목표

시작 위치의 구현을 완성해 live / ready health endpoint가 구분되어야 합니다, 요청 수 같은 최소 metrics surface가 있어야 합니다, 로컬 Compose 부팅과 CI 명령이 정리되어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/G-ops-lab/fastapi/app/__init__.py`
- `../labs/G-ops-lab/fastapi/app/api/__init__.py`
- `../labs/G-ops-lab/fastapi/app/api/deps.py`
- `../labs/G-ops-lab/fastapi/app/api/v1/__init__.py`
- `../labs/G-ops-lab/fastapi/tests/conftest.py`
- `../labs/G-ops-lab/fastapi/tests/integration/test_ops.py`
- `../labs/G-ops-lab/fastapi/compose.yaml`
- `../labs/G-ops-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/G-ops-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- live / ready health endpoint가 구분되어야 합니다.
- 요청 수 같은 최소 metrics surface가 있어야 합니다.
- 로컬 Compose 부팅과 CI 명령이 정리되어야 합니다.
- AWS target shape가 실제 배포 완료처럼 과장되지 않고 문서로 설명되어야 합니다.

## 제외 범위

- 풀 observability stack 구축
- IaC로 실제 인프라를 생성하는 자동화
- 장시간 부하 테스트와 장애 주입 실험

## 성공 체크리스트

- 핵심 흐름은 `get_metrics_registry`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_live_ready_and_metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/G-ops-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`g-ops-lab-fastapi_answer.md`](g-ops-lab-fastapi_answer.md)에서 확인한다.
