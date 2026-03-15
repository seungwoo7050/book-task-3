# k-distributed-ops-lab-fastapi 문제지

## 왜 중요한가

MSA 구조를 실행만 하는 것으로 끝내지 않고, 서비스별 health, JSON 로그, 최소 metrics, target shape 문서를 함께 설명해야 한다. 이 랩은 운영성을 별도 학습 주제로 분리한다.

## 목표

시작 위치의 구현을 완성해 gateway와 내부 서비스가 각각 /health/live, /health/ready, /ops/metrics를 제공한다, request id가 로그 문맥과 응답 헤더에 남는다, AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/K-distributed-ops-lab/fastapi/gateway/app/__init__.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/__init__.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/deps.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/__init__.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/conftest.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/integration/test_gateway_health.py`
- `../labs/K-distributed-ops-lab/fastapi/compose.yaml`
- `../labs/K-distributed-ops-lab/fastapi/gateway/Makefile`

## starter code / 입력 계약

- `../labs/K-distributed-ops-lab/fastapi/gateway/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- gateway와 내부 서비스가 각각 /health/live, /health/ready, /ops/metrics를 제공한다.
- request id가 로그 문맥과 응답 헤더에 남는다.
- AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다.

## 제외 범위

- 실제 클라우드 배포 자동화
- trace backend
- log shipping

## 성공 체크리스트

- 핵심 흐름은 `get_service_client`와 `get_current_claims`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_live_and_metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/K-distributed-ops-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway && python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi test
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`k-distributed-ops-lab-fastapi_answer.md`](k-distributed-ops-lab-fastapi_answer.md)에서 확인한다.
