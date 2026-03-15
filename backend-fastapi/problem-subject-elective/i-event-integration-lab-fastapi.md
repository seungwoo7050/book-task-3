# i-event-integration-lab-fastapi 문제지

## 왜 중요한가

동기 API와 비동기 알림 전달을 서비스 간 통합으로 확장한다. 댓글 저장과 알림 생성이 같은 시점에 끝나지 않아도 되는 구조를 설명하는 것이 목표다.

## 목표

시작 위치의 구현을 완성해 댓글 생성이 outbox에 기록된다, relay 후 notification-service가 stream을 consume한다, 같은 consume를 두 번 실행해도 알림이 중복 저장되지 않는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/I-event-integration-lab/fastapi/gateway/app/__init__.py`
- `../labs/I-event-integration-lab/fastapi/gateway/app/api/__init__.py`
- `../labs/I-event-integration-lab/fastapi/gateway/app/api/deps.py`
- `../labs/I-event-integration-lab/fastapi/gateway/app/api/v1/__init__.py`
- `../labs/I-event-integration-lab/fastapi/gateway/tests/conftest.py`
- `../labs/I-event-integration-lab/fastapi/gateway/tests/integration/test_gateway_health.py`
- `../labs/I-event-integration-lab/fastapi/compose.yaml`
- `../labs/I-event-integration-lab/fastapi/gateway/Makefile`

## starter code / 입력 계약

- `../labs/I-event-integration-lab/fastapi/gateway/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 댓글 생성이 outbox에 기록된다.
- relay 후 notification-service가 stream을 consume한다.
- 같은 consume를 두 번 실행해도 알림이 중복 저장되지 않는다.

## 제외 범위

- consumer group
- dead-letter queue
- replay UI

## 성공 체크리스트

- 핵심 흐름은 `get_service_client`와 `get_current_claims`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_live_and_metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/I-event-integration-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/I-event-integration-lab/fastapi/gateway test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/I-event-integration-lab/fastapi/gateway test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/I-event-integration-lab/fastapi/gateway && python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/I-event-integration-lab/fastapi test
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`i-event-integration-lab-fastapi_answer.md`](i-event-integration-lab-fastapi_answer.md)에서 확인한다.
