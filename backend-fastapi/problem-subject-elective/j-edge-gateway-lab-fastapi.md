# j-edge-gateway-lab-fastapi 문제지

## 왜 중요한가

서비스가 분리된 뒤에도 외부 클라이언트는 하나의 API만 보고 싶다. 이 랩은 gateway가 public API shape를 유지하고, cookie와 CSRF를 edge에만 두며, 내부 서비스에는 request id와 bearer token만 전달하는 구조를 연습한다.

## 목표

시작 위치의 구현을 완성해 gateway가 /api/v1/auth/*, /api/v1/platform/* 경로를 유지한다, 로그인 후 쿠키가 gateway에서만 설정된다, 내부 호출에 X-Request-ID가 전달된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/J-edge-gateway-lab/fastapi/gateway/app/__init__.py`
- `../labs/J-edge-gateway-lab/fastapi/gateway/app/api/__init__.py`
- `../labs/J-edge-gateway-lab/fastapi/gateway/app/api/deps.py`
- `../labs/J-edge-gateway-lab/fastapi/gateway/app/api/v1/__init__.py`
- `../labs/J-edge-gateway-lab/fastapi/gateway/tests/conftest.py`
- `../labs/J-edge-gateway-lab/fastapi/gateway/tests/integration/test_gateway_health.py`
- `../labs/J-edge-gateway-lab/fastapi/compose.yaml`
- `../labs/J-edge-gateway-lab/fastapi/gateway/Makefile`

## starter code / 입력 계약

- `../labs/J-edge-gateway-lab/fastapi/gateway/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- gateway가 /api/v1/auth/*, /api/v1/platform/* 경로를 유지한다.
- 로그인 후 쿠키가 gateway에서만 설정된다.
- 내부 호출에 X-Request-ID가 전달된다.

## 제외 범위

- circuit breaker
- service discovery
- 고급 edge cache

## 성공 체크리스트

- 핵심 흐름은 `get_service_client`와 `get_current_claims`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_live_and_metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/J-edge-gateway-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/J-edge-gateway-lab/fastapi/gateway test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/J-edge-gateway-lab/fastapi/gateway test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/J-edge-gateway-lab/fastapi/gateway && python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/J-edge-gateway-lab/fastapi test
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`j-edge-gateway-lab-fastapi_answer.md`](j-edge-gateway-lab-fastapi_answer.md)에서 확인한다.
