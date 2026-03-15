# c-authorization-lab-fastapi 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다, 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다, owner와 일반 member의 차이가 실제 리소스 접근에 반영되어야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `get_authorization_service`와 `get_actor_id` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다.
- 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다.
- owner와 일반 member의 차이가 실제 리소스 접근에 반영되어야 합니다.
- 첫 진입점은 `../labs/C-authorization-lab/fastapi/app/__init__.py`이고, 여기서 `get_authorization_service`와 `get_actor_id` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../labs/C-authorization-lab/fastapi/app/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../labs/C-authorization-lab/fastapi/app/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/C-authorization-lab/fastapi/app/api/deps.py`: `get_authorization_service`, `get_actor_id`가 핵심 흐름과 상태 전이를 묶는다.
- `../labs/C-authorization-lab/fastapi/app/api/v1/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/C-authorization-lab/fastapi/app/api/v1/router.py`: endpoint와 route 조합을 묶어 외부 진입 경로를 고정하는 파일이다.
- `../labs/C-authorization-lab/fastapi/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py`: `test_invite_accept_promote_and_document_permissions`, `test_invite_decline_and_outsider_read_forbidden`가 통과 조건과 회귀 포인트를 잠근다.
- `../labs/C-authorization-lab/fastapi/tests/smoke.py`: `main`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../labs/C-authorization-lab/fastapi/app/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `app_env` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && PYTHONPATH=. python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `app_env`와 `client`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && PYTHONPATH=. python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../labs/C-authorization-lab/fastapi/app/__init__.py`
- `../labs/C-authorization-lab/fastapi/app/api/__init__.py`
- `../labs/C-authorization-lab/fastapi/app/api/deps.py`
- `../labs/C-authorization-lab/fastapi/app/api/v1/__init__.py`
- `../labs/C-authorization-lab/fastapi/app/api/v1/router.py`
- `../labs/C-authorization-lab/fastapi/tests/conftest.py`
- `../labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py`
- `../labs/C-authorization-lab/fastapi/tests/smoke.py`
- `../labs/C-authorization-lab/fastapi/compose.yaml`
- `../labs/C-authorization-lab/fastapi/Makefile`
