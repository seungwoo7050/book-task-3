# workspace-backend-v2-msa-fastapi 문제지

## 왜 중요한가

workspace-backend v1은 인증, 워크스페이스 도메인, 알림 전달을 한 프로세스 안에서 통합했다. v2의 목표는 같은 협업형 도메인을 MSA로 다시 분해해, public API를 유지한 채 내부 경계와 분산 복잡성이 어떻게 바뀌는지 설명 가능한 상태로 만드는 것이다.

## 목표

시작 위치의 구현을 완성해 gateway가 public /api/v1/auth/*, /api/v1/platform/* 경로를 유지해야 한다, identity-service, workspace-service, notification-service는 각자 자기 DB만 읽어야 한다, 댓글 생성은 outbox에 기록되고, 이후 stream consumer와 websocket fan-out으로 이어져야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../capstone/workspace-backend-v2-msa/fastapi/gateway/app/__init__.py`
- `../capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/__init__.py`
- `../capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/deps.py`
- `../capstone/workspace-backend-v2-msa/fastapi/gateway/app/api/v1/__init__.py`
- `../capstone/workspace-backend-v2-msa/fastapi/gateway/tests/conftest.py`
- `../capstone/workspace-backend-v2-msa/fastapi/gateway/tests/integration/test_gateway_health.py`
- `../capstone/workspace-backend-v2-msa/fastapi/compose.yaml`
- `../capstone/workspace-backend-v2-msa/fastapi/gateway/Makefile`

## starter code / 입력 계약

- `../capstone/workspace-backend-v2-msa/fastapi/gateway/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- gateway가 public /api/v1/auth/*, /api/v1/platform/* 경로를 유지해야 한다.
- identity-service, workspace-service, notification-service는 각자 자기 DB만 읽어야 한다.
- 댓글 생성은 outbox에 기록되고, 이후 stream consumer와 websocket fan-out으로 이어져야 한다.
- notification-service가 잠시 내려가도 댓글 생성은 성공하고, 복구 후 consume로 알림이 전달되어야 한다.
- v1과 v2의 차이를 문서와 노트만 읽고 설명할 수 있어야 한다.

## 제외 범위

- Kubernetes, service mesh, service discovery
- 실제 클라우드 배포 자동화와 IaC
- front-end 렌더링과 정적 자산

## 성공 체크리스트

- 핵심 흐름은 `get_service_client`와 `get_current_claims`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_live_and_metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../capstone/workspace-backend-v2-msa/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway && python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend-v2-msa/fastapi test
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`workspace-backend-v2-msa-fastapi_answer.md`](workspace-backend-v2-msa-fastapi_answer.md)에서 확인한다.
