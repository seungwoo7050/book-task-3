# b-federation-security-lab-fastapi 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다, TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다, recovery code 재생성 및 소진 규칙이 있어야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `get_auth_service`와 `get_google_oidc_service`, `require_csrf` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다.
- TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다.
- recovery code 재생성 및 소진 규칙이 있어야 합니다.
- 첫 진입점은 `../labs/B-federation-security-lab/fastapi/app/__init__.py`이고, 여기서 `get_auth_service`와 `get_google_oidc_service` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../labs/B-federation-security-lab/fastapi/app/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../labs/B-federation-security-lab/fastapi/app/api/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/B-federation-security-lab/fastapi/app/api/deps.py`: `get_auth_service`, `get_google_oidc_service`, `require_csrf`, `get_current_user`가 핵심 흐름과 상태 전이를 묶는다.
- `../labs/B-federation-security-lab/fastapi/app/api/v1/__init__.py`: 패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다.
- `../labs/B-federation-security-lab/fastapi/app/api/v1/router.py`: endpoint와 route 조합을 묶어 외부 진입 경로를 고정하는 파일이다.
- `../labs/B-federation-security-lab/fastapi/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py`: `test_google_callback_creates_user_and_session`가 통과 조건과 회귀 포인트를 잠근다.
- `../labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py`: `_mock_google`, `_complete_google_login`, `test_two_factor_setup_and_recovery_code_login`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../labs/B-federation-security-lab/fastapi/app/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `app_env` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && PYTHONPATH=. python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `app_env`와 `client`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && PYTHONPATH=. python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../labs/B-federation-security-lab/fastapi/app/__init__.py`
- `../labs/B-federation-security-lab/fastapi/app/api/__init__.py`
- `../labs/B-federation-security-lab/fastapi/app/api/deps.py`
- `../labs/B-federation-security-lab/fastapi/app/api/v1/__init__.py`
- `../labs/B-federation-security-lab/fastapi/app/api/v1/router.py`
- `../labs/B-federation-security-lab/fastapi/tests/conftest.py`
- `../labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py`
- `../labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py`
- `../labs/B-federation-security-lab/fastapi/compose.yaml`
- `../labs/B-federation-security-lab/fastapi/Makefile`
