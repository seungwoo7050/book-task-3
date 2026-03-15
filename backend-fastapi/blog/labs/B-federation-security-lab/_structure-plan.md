# B-federation-security-lab structure plan

## 한 줄 약속

- 외부 로그인과 2FA를 "로그인 수단 추가"가 아니라 인증 완료 단계를 늘리는 상태 기계로 읽게 만든다.

## 독자 질문

- OIDC callback이 어떤 근거로 내부 user/session 경계가 되는가
- provider 성공 이후 왜 바로 `authenticated`가 아니라 `requires_2fa`로 멈출 수 있는가
- recovery code는 왜 hash로만 저장돼야 하는가
- 외부 로그인 위에서도 refresh token family 규칙은 그대로 유지되는가
- 현재 문서에 적힌 검증 명령은 지금 셸에서 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- mock 기반 OIDC 경계와 현재 import/dependency drift를 둘 다 숨기지 않는다.

## 글 흐름

1. signed state, nonce, PKCE verifier가 callback 경계를 어떻게 만드는지부터 연다.
2. external identity linking과 pending second factor 단계가 내부 인증 completion을 어떻게 늦추는지 설명한다.
3. TOTP setup/confirm/verify와 hashed recovery code 저장을 하나의 2FA state machine으로 묶는다.
4. federated login 위에서도 refresh reuse detection, rate limit, audit event가 그대로 남는다는 점을 확인한다.
5. 오늘 다시 돌린 CLI 결과로 현재 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [google_callback route](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py)
- 보조 코드 앵커: [GoogleOIDCService](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/google_oidc.py), [AuthService](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/auth.py)
- 보안 앵커: [security.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/core/security.py), [ExternalIdentity model](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/db/models/user.py)
- 테스트 앵커: [test_google_callback.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py), [test_two_factor.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py), [test_token_rotation.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/unit/test_token_rotation.py)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 provider callback, external identity linking, pending 2FA, recovery code, refresh reuse detection이 하나의 auth surface 안에서 연결된다는 점이다.
- 이 랩의 현재 약점은 공식 검증 진입점이 2026-03-14 셸에서는 `app` path, `fastapi`, `itsdangerous` 문제로 바로 닫히지 않는다는 점이다.
- 다음 랩인 `C-authorization-lab`은 여기서 완성된 인증 결과를 전제로 권한과 소유권 규칙만 분리해서 읽는 비교 대상으로 연결한다.
