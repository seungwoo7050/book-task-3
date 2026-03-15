# B-federation-security-lab series map

이 시리즈는 외부 로그인과 2단계 인증을 "기능 몇 개 추가"가 아니라, 인증 상태 기계를 한 단계 더 잘게 쪼개는 문제로 다시 읽는다. Google 스타일 로그인, signed OAuth state, pending second factor, recovery code, refresh reuse detection이 한 흐름 안에서 어떻게 만나는지가 중심이다.

## 이 시리즈가 붙잡는 질문

- 외부 공급자 계정과 내부 사용자 계정을 어디서 연결해야 하는가
- OIDC callback이 왜 단순 redirect 완료가 아니라 내부 세션 번역 지점이 되는가
- 2FA는 로그인 이후의 부가 기능이 아니라 어떤 별도 단계로 고정되는가
- recovery code는 왜 평문이 아니라 hash로 저장돼야 하는가

## 왜 이 순서로 읽는가

1. `problem/README.md`와 상위 `README.md`로 이 랩의 성공 기준을 먼저 고정한다.
2. `google/login`과 `google/callback` route를 보며 provider 응답이 내부 인증으로 번역되는 경계를 본다.
3. `sync_google_user`, `ExternalIdentity`, `pending_auth_token` 흐름을 따라가며 외부 identity와 내부 user 연결을 확인한다.
4. `2fa/setup`, `2fa/confirm`, `2fa/verify`와 통합 테스트를 같이 보며 second factor가 어떤 challenge 단계로 삽입되는지 확인한다.
5. 마지막에 `make lint`, `make test`, `make smoke`와 보조 재실행 결과를 붙여 지금 셸 기준 재현 가능 상태를 확인한다.

## 근거로 사용한 자료

- `backend-fastapi/labs/B-federation-security-lab/README.md`
- `backend-fastapi/labs/B-federation-security-lab/problem/README.md`
- `backend-fastapi/labs/B-federation-security-lab/docs/README.md`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/README.md`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/Makefile`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/deps.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/core/security.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/auth.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/google_oidc.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/two_factor.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/db/models/user.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/db/models/auth.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/tests/unit/test_token_rotation.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/health.py) 의 한 줄 길이 초과(`E501`) 때문에 실패했다.
- 같은 날짜 `make test`는 test collection 단계에서 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 타면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`를 다시 돌리면 `itsdangerous` 미설치 때문에 `ModuleNotFoundError: No module named 'itsdangerous'`에서 멈춘다.
- `PYTHONPATH=. python -m tests.smoke`도 같은 이유로 `itsdangerous` import 단계에서 실패한다.
- 즉 OIDC/2FA state machine 자체는 코드와 테스트로 읽히지만, 현재 셸 기준 재검증 진입점은 그대로 통과하지 않는다.

## 현재 범위 밖

- 실제 Google 서비스와의 end-to-end 통신 검증
- 제품 도메인별 권한과 리소스 모델
- 복수 외부 공급자에 대한 공통 추상화 완성

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - OIDC callback이 내부 세션과 2FA challenge로 갈라지는 지점부터 recovery code와 refresh reuse detection까지 구현 순서로 복원한다.
