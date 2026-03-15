# B-federation-security-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/README.md) 가 OIDC, 2FA, recovery code, audit log를 하나의 독립 문제로 묶고, `google_callback`, `two_factor`, `token_rotation` 테스트가 서로 다른 상태 전이를 따로 고정한다.
- 프로젝트 질문: 외부 로그인과 second factor가 들어오면 "인증 성공"을 어디에서 끝난 것으로 볼 것인가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/docs/README.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/README.md)
- [`app/api/v1/routes/auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py)
- [`app/api/deps.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/deps.py)
- [`app/core/security.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/core/security.py)
- [`app/domain/services/auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/auth.py)
- [`app/domain/services/google_oidc.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/google_oidc.py)
- [`app/domain/services/two_factor.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/two_factor.py)
- [`app/db/models/user.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/db/models/user.py)
- [`app/db/models/auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/db/models/auth.py)
- [`tests/integration/test_google_callback.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py)
- [`tests/integration/test_two_factor.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py)
- [`tests/unit/test_token_rotation.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/unit/test_token_rotation.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 외부 로그인 진입이 무엇을 새로 늘리는지 먼저 판정한다 | `README.md`, `problem/README.md`, `google_oidc.py`, `auth.py` | state, nonce, PKCE verifier를 signed cookie로 보관하고 callback에서 다시 검증한다 | `rg -n 'google/login|google/callback|auth:google' backend-fastapi/labs/B-federation-security-lab/fastapi/app backend-fastapi/labs/B-federation-security-lab/fastapi/tests` | OIDC callback은 redirect 끝점이 아니라 내부 인증으로 번역되는 경계로 읽힌다 | callback 이후에도 인증이 끝나지 않는 이유를 보려면 pending 2FA 단계로 내려가야 한다 |
| 2 | provider 성공 후 왜 바로 세션을 주지 않을 수도 있는지 확인한다 | `auth.py`, `auth.py` service, `core/security.py`, `user.py` | `sync_google_user()`가 `ExternalIdentity`를 연결하고, `two_factor_enabled`면 `requires_2fa`와 `pending_auth_token`을 반환한다 | `rg -n 'requires_2fa|pending_auth|build_pending_auth_token|set_pending_auth_cookie' backend-fastapi/labs/B-federation-security-lab/fastapi/app backend-fastapi/labs/B-federation-security-lab/fastapi/tests` | 외부 로그인 성공과 내부 세션 완료 사이에 별도 challenge 단계가 존재한다 | 이제 2FA가 어떤 자료구조와 검증으로 닫히는지 봐야 한다 |
| 3 | 2FA와 recovery code를 별도 state machine으로 고정한다 | `two_factor.py`, `auth.py` service, `auth_repository.py`, `test_two_factor.py` | setup/confirm/verify가 분리돼 있고, recovery code는 생성 직후 hash로만 저장된다 | `rg -n '2fa/setup|2fa/confirm|2fa/verify|recovery-codes/regenerate|2fa/disable|auth.2fa.' backend-fastapi/labs/B-federation-security-lab/fastapi/app backend-fastapi/labs/B-federation-security-lab/fastapi/tests` | 재로그인 직후 `me`는 401이고, recovery code 검증 뒤에야 `authenticated`가 된다 | federated login 위에서도 기존 refresh rotation 규칙이 유지되는지 확인한다 |
| 4 | 외부 로그인 추가 후에도 session family 규칙과 운영 신호가 남아 있는지 본다 | `auth.py` service, `test_token_rotation.py`, route limiter 설정 | OIDC 로그인 이후에도 예전 refresh token 재사용을 감지하면 family 전체를 revoke하고, 주요 단계마다 audit event와 rate-limit prefix가 따로 있다 | `rg -n 'auth.refresh.reuse_detected|REFRESH_TOKEN_REUSED|family_id|auth:google|auth:2fa|auth.2fa.' backend-fastapi/labs/B-federation-security-lab/fastapi/app backend-fastapi/labs/B-federation-security-lab/fastapi/tests` | 외부 provider가 들어와도 세션 규칙과 최소 운영 신호는 사라지지 않고 위에 얹힌다 | 마지막으로 지금 셸에서 공식 검증 명령이 그대로 통과하는지 확인한다 |
| 5 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, `health.py`, `tests/smoke.py`, 현재 셸 환경 | 공식 `make` 진입점과 `PYTHONPATH` 보조 재실행 모두 즉시 통과하지는 않는다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint`는 `health.py` E501, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 `No module named 'itsdangerous'` | 구현 설명과 현재 재현 환경의 간극을 문서에 함께 남겨야 품질이 맞는다 |
