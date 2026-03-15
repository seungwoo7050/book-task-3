# A-auth-lab series map

이 시리즈는 로컬 인증을 "로그인 API 하나"로 축소하지 않고, 이메일 검증, 비밀번호 재설정, refresh rotation, cookie 기반 CSRF 방어까지 한 번에 설명할 수 있는 최소 표면으로 다시 읽는다. 질문은 단순하다. 세션을 오래 들고 가는 규칙은 어디서부터 별도 설계가 되는가.

## 이 시리즈가 붙잡는 질문

- access token과 refresh token을 왜 굳이 분리하는가
- 이메일 검증과 비밀번호 재설정을 같은 token 발급/소비 문제로 어디까지 묶을 수 있는가
- cookie 인증에서 CSRF 실패를 어느 진입점에서 끊어야 하는가

## 왜 이 순서로 읽는가

1. `problem/README.md`와 상위 `README.md`로 이 랩의 성공 기준을 먼저 고정한다.
2. `app/api/v1/routes/auth.py`에서 public auth surface가 어디까지 열려 있는지 확인한다.
3. `app/domain/services/auth.py`, `app/db/models/auth.py`, `app/core/security.py`로 token family, reuse detection, CSRF 검증이 실제로 어디에 잠겨 있는지 따라간다.
4. `tests/integration/test_local_auth.py`에서 공격자 시나리오와 recovery 흐름이 어떤 요청 순서로 고정됐는지 본다.
5. 마지막에 `make lint`, `make test`, `make smoke`와 보조 재실행 결과를 붙여 현재 재현 가능 상태를 확인한다.

## 근거로 사용한 자료

- `backend-fastapi/labs/A-auth-lab/README.md`
- `backend-fastapi/labs/A-auth-lab/problem/README.md`
- `backend-fastapi/labs/A-auth-lab/docs/README.md`
- `backend-fastapi/labs/A-auth-lab/fastapi/README.md`
- `backend-fastapi/labs/A-auth-lab/fastapi/Makefile`
- `backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/app/api/deps.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/app/core/security.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/app/domain/services/auth.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/app/db/models/auth.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/health.py) 한 줄 길이 초과(`E501`) 때문에 실패했다.
- 같은 날짜 `make test`는 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 가리키면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`와 `PYTHONPATH=. python -m tests.smoke`도 다시 돌렸고, 둘 다 `argon2-cffi` 미설치 때문에 `ModuleNotFoundError: No module named 'argon2'`에서 멈췄다.
- 즉 구현 표면은 선명하지만, 현재 셸 기준 재검증 진입점은 그대로 통과하지 않는다.

## 현재 범위 밖

- Google OAuth 같은 외부 로그인
- TOTP 2FA와 recovery code
- 실제 외부 SMTP와 운영용 메일 인프라

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - 로컬 인증 surface가 어떻게 token family, CSRF, recovery 흐름까지 확장되는지 구현 순서로 복원한다.
