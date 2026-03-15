# k-distributed-ops-lab-fastapi 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 gateway와 내부 서비스가 각각 /health/live, /health/ready, /ops/metrics를 제공한다, request id가 로그 문맥과 응답 헤더에 남는다, AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다를 한 흐름으로 설명하고 검증한다. 핵심은 `get_service_client`와 `get_current_claims`, `require_csrf` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- gateway와 내부 서비스가 각각 /health/live, /health/ready, /ops/metrics를 제공한다.
- request id가 로그 문맥과 응답 헤더에 남는다.
- AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다.
- 첫 진입점은 `../labs/K-distributed-ops-lab/fastapi/gateway/app/__init__.py`이고, 여기서 `get_service_client`와 `get_current_claims` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../labs/K-distributed-ops-lab/fastapi/gateway/app/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/deps.py`: `get_service_client`, `get_current_claims`, `require_csrf`가 핵심 흐름과 상태 전이를 묶는다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/router.py`: endpoint와 route 조합을 묶어 외부 진입 경로를 고정하는 파일이다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/integration/test_gateway_health.py`: `test_live_and_metrics`가 통과 조건과 회귀 포인트를 잠근다.
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/smoke.py`: `main`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../labs/K-distributed-ops-lab/fastapi/gateway/app/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `client` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway && python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `client`와 `test_live_and_metrics`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../labs/K-distributed-ops-lab/fastapi/gateway/app/__init__.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/__init__.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/deps.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/__init__.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/router.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/conftest.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/integration/test_gateway_health.py`
- `../labs/K-distributed-ops-lab/fastapi/gateway/tests/smoke.py`
- `../labs/K-distributed-ops-lab/fastapi/compose.yaml`
- `../labs/K-distributed-ops-lab/fastapi/gateway/Makefile`
