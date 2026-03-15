# h-service-boundary-lab-fastapi 문제지

## 왜 중요한가

단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 처음으로 분리한다. 핵심 질문은 "어디서 경계를 끊어야 하며, 서비스가 서로의 DB를 읽지 않고도 동작할 수 있는가"이다.

## 목표

시작 위치의 구현을 완성해 identity-service가 토큰을 발급한다, workspace-service가 그 토큰 claims만으로 workspace를 생성한다, 두 서비스가 각자 자기 DB만 읽고, cross-DB 조회를 하지 않는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/H-service-boundary-lab/fastapi/gateway/app/__init__.py`
- `../labs/H-service-boundary-lab/fastapi/gateway/app/api/__init__.py`
- `../labs/H-service-boundary-lab/fastapi/gateway/app/api/deps.py`
- `../labs/H-service-boundary-lab/fastapi/gateway/app/api/v1/__init__.py`
- `../labs/H-service-boundary-lab/fastapi/gateway/tests/conftest.py`
- `../labs/H-service-boundary-lab/fastapi/gateway/tests/integration/test_gateway_health.py`
- `../labs/H-service-boundary-lab/fastapi/compose.yaml`
- `../labs/H-service-boundary-lab/fastapi/gateway/Makefile`

## starter code / 입력 계약

- `../labs/H-service-boundary-lab/fastapi/gateway/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- identity-service가 토큰을 발급한다.
- workspace-service가 그 토큰 claims만으로 workspace를 생성한다.
- 두 서비스가 각자 자기 DB만 읽고, cross-DB 조회를 하지 않는다.

## 제외 범위

- 이벤트 브로커
- edge gateway
- websocket과 실시간 전달

## 성공 체크리스트

- 핵심 흐름은 `get_service_client`와 `get_current_claims`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_live_and_metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/H-service-boundary-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/H-service-boundary-lab/fastapi/gateway test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/H-service-boundary-lab/fastapi/gateway test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/H-service-boundary-lab/fastapi/gateway && python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/H-service-boundary-lab/fastapi test
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`h-service-boundary-lab-fastapi_answer.md`](h-service-boundary-lab-fastapi_answer.md)에서 확인한다.
