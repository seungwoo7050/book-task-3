# a-auth-lab-fastapi 문제지

## 왜 중요한가

로컬 계정 기반 인증 백엔드를 만든다고 가정합니다. 사용자는 회원가입하고, 이메일을 검증하고, 로그인하고, 필요하면 비밀번호를 재설정할 수 있어야 합니다. 이때 세션 유지와 상태 변경 요청 보호까지 함께 고려해야 합니다.

## 목표

시작 위치의 구현을 완성해 회원가입과 로그인 흐름이 분리되어 설명 가능해야 합니다, 이메일 검증과 비밀번호 재설정 토큰 발급/소비가 동작해야 합니다, refresh token rotation이 왜 필요한지 코드와 문서로 설명할 수 있어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/A-auth-lab/fastapi/app/__init__.py`
- `../labs/A-auth-lab/fastapi/app/api/__init__.py`
- `../labs/A-auth-lab/fastapi/app/api/deps.py`
- `../labs/A-auth-lab/fastapi/app/api/v1/__init__.py`
- `../labs/A-auth-lab/fastapi/tests/conftest.py`
- `../labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py`
- `../labs/A-auth-lab/fastapi/compose.yaml`
- `../labs/A-auth-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/A-auth-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 회원가입과 로그인 흐름이 분리되어 설명 가능해야 합니다.
- 이메일 검증과 비밀번호 재설정 토큰 발급/소비가 동작해야 합니다.
- refresh token rotation이 왜 필요한지 코드와 문서로 설명할 수 있어야 합니다.
- cookie 인증 요청에 CSRF 방어가 함께 붙어야 합니다.

## 제외 범위

- Google OAuth 같은 외부 로그인
- TOTP 2FA와 recovery code
- 운영용 메일 인프라와 실제 외부 SMTP 검증

## 성공 체크리스트

- 핵심 흐름은 `get_auth_service`와 `get_mailbox`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `app_env`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/A-auth-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`a-auth-lab-fastapi_answer.md`](a-auth-lab-fastapi_answer.md)에서 확인한다.
