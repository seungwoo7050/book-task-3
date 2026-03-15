# B-federation-security-lab development timeline

이 글은 B 랩을 "Google 로그인도 되고 2FA도 되는 auth 예제"처럼 평평하게 요약하지 않는다. 현재 남아 있는 source of truth를 따라가 보면, 이 프로젝트의 핵심은 인증 성공을 더 복잡하게 만드는 데 있다. 외부 provider에서 받은 신호를 내부 user와 어떻게 연결할지, 그 직후 왜 다시 `pending_2fa` 단계로 멈춰야 하는지, recovery code를 왜 평문이 아니라 hash로 저장해야 하는지가 실제 구현의 중심축이다.

## Phase 1. 외부 로그인은 세션 발급 이전에 한 번 더 번역돼야 한다

처음 눈에 들어오는 건 [`google/login`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py) 과 [`google/callback`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py) 이다. route 이름만 보면 소셜 로그인 버튼 두 개처럼 보이는데, 실제로는 여기서 이미 state, nonce, PKCE verifier를 signed cookie로 보관하고 callback에서 다시 검증한다.

[`GoogleOIDCService.build_authorization_request()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/google_oidc.py) 는 state, nonce, code verifier를 만들고 authorization URL로 내보낸다. 이어서 [`sign_oauth_state()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/core/security.py) 가 그 값을 cookie에 서명해 넣고, callback에서는 [`unsign_oauth_state()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/core/security.py) 로 다시 복원한다.

```python
signed_state = request.cookies.get(settings.oauth_state_cookie_name)
if not signed_state:
    raise AppError(
        code="OAUTH_STATE_REQUIRED",
        message="OAuth state cookie is missing.",
        status_code=400,
    )
oauth_state = unsign_oauth_state(signed_state, settings)
if oauth_state["state"] != state:
    raise AppError(
        code="OAUTH_STATE_MISMATCH",
        message="OAuth state value did not match.",
        status_code=400,
    )
```

이 지점에서 이 랩의 관점이 정해진다. 외부 provider callback은 성공 신호를 받아 오는 끝점이 아니라, "이 응답을 내부 인증으로 번역해도 되는가"를 따지는 경계다.

## Phase 2. callback 이후에도 인증은 바로 끝나지 않는다

`google_callback`의 더 흥미로운 부분은 user를 만든 뒤 곧바로 세션을 주지 않을 수도 있다는 점이다. [`sync_google_user()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/auth.py) 는 `ExternalIdentity`를 user에 연결하고 profile을 갱신하지만, user에 `two_factor_enabled`가 켜져 있으면 route는 `authenticated` 대신 `requires_2fa`를 반환한다. 이때 실제 access/refresh cookie 대신 [`pending_auth_token`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/core/security.py) 이 발급된다.

```python
if user.two_factor_enabled:
    pending_token = auth_service.start_pending_second_factor(
        user=user,
        ip_address=client_ip,
        user_agent=user_agent,
    )
    set_pending_auth_cookie(response, pending_token, settings)
    set_csrf_cookie(response, generate_csrf_token(), settings)
    return response
```

이 구조가 중요한 이유는 "외부 로그인이 곧 내부 세션"이라는 단순한 등식을 의도적으로 깨기 때문이다. provider 인증이 끝나도 second factor가 남아 있으면 아직 완전한 로그인으로 간주하지 않는다.

## Phase 3. 2FA는 부가 기능이 아니라 별도 state machine이다

route surface를 더 내려가 보면 이 랩의 auth model이 어디서 확장되는지가 분명해진다. `2fa/setup`, `2fa/confirm`, `2fa/verify`, `2fa/recovery-codes/regenerate`, `2fa/disable`이 모두 따로 열려 있고, service 계층은 `pending_two_factor_secret`, `two_factor_secret`, `two_factor_enabled`, recovery code hash 저장소를 별도로 관리한다.

특히 [`confirm_two_factor_setup()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/domain/services/auth.py) 는 TOTP code를 확인한 뒤 recovery code 8개를 만들고, repository에는 평문이 아니라 `hash_secret(...)` 결과만 저장한다.

```python
recovery_codes = self.two_factor_service.generate_recovery_codes()
self.auth_repository.replace_recovery_codes(
    user_id=user.id,
    code_hashes=[hash_secret(code_value, self.settings) for code_value in recovery_codes],
)
```

여기서 recovery code는 "혹시 잊어버리면 쓰는 문자열"이 아니라, 실제 2FA challenge를 통과하는 두 번째 증명 수단으로 취급된다. `docs/README.md`가 recovery code 평문 보관을 경계하는 이유도 바로 이 구현에서 드러난다.

## Phase 4. 통합 테스트가 challenge와 completion을 분리해서 고정한다

이 랩의 가장 설명력 있는 문서는 테스트다. [`test_google_callback_creates_user_and_session()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py) 는 monkeypatch된 OIDC 응답만으로 user 생성과 기본 세션 발급이 되는지 본다. 반면 [`test_two_factor_setup_and_recovery_code_login()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py) 는 흐름을 일부러 더 길게 만든다.

```python
_complete_google_login(client)
assert client.get("/api/v1/auth/me").status_code == 401

challenge_csrf = client.cookies["csrf_token"]
verify_response = client.post(
    "/api/v1/auth/2fa/verify",
    json={"recovery_code": recovery_codes[0]},
    headers={"X-CSRF-Token": challenge_csrf},
)
assert verify_response.status_code == 200
assert verify_response.json()["status"] == "authenticated"
```

이 테스트는 second factor가 통과되기 전에는 `me`도 열리지 않는다는 걸 고정한다. 2FA를 "나중에 켜도 되는 옵션"이 아니라, 실제 로그인 completion 단계로 취급한 셈이다.

## Phase 5. federated login 위에서도 refresh reuse detection은 계속 살아 있다

B 랩이 외부 로그인과 2FA에 집중한다고 해서 refresh rotation이 사라지는 건 아니다. [`test_refresh_rotation_detects_reuse()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/tests/unit/test_token_rotation.py) 는 OIDC 로그인 이후에도 예전 refresh token 재사용을 감지하면 family 전체를 revoke해야 한다는 규칙을 그대로 확인한다. 즉 이 랩은 A 랩의 rotation rule 위에 federated login과 2FA를 덧씌우는 구조다.

이 덕분에 "외부 로그인 추가"가 기존 보안 규칙을 대체하는 것이 아니라, 기존 세션 규칙 위에 새 단계를 얹는다는 사실이 분명해진다.

같은 구간에서 보이는 또 하나의 축은 남용 제한과 감사 로그다. route에는 `auth:google-login`, `auth:google-callback`, `auth:refresh`, `auth:2fa-verify` 같은 rate-limit prefix가 직접 붙어 있고, service는 `auth.login.challenge_required`, `auth.2fa.enabled`, `auth.2fa.verified`, `auth.refresh.reuse_detected` 같은 이벤트를 audit log로 남긴다. 이 랩은 그래서 인증 기능만 늘리는 예제가 아니라, 보안 이벤트를 나중에 추적 가능한 형태로 남기는 최소 운영 표면까지 함께 다룬다.

## Phase 6. 오늘 다시 돌린 검증은 import와 dependency drift를 먼저 드러냈다

2026-03-14 현재 셸에서 다시 실행한 결과는 문서가 암시하는 상태보다 거칠다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇다.

- `make lint`: [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/health.py) 의 주석 한 줄이 `E501`로 실패한다.
- `make test`: test collection 단계에서 `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: Homebrew `python3` 기준 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`: `itsdangerous` 미설치로 `ModuleNotFoundError: No module named 'itsdangerous'`.
- `PYTHONPATH=. python -m tests.smoke`: 같은 `itsdangerous` import 단계에서 실패.

즉 이 랩은 mock OIDC와 second-factor state machine을 코드와 테스트로는 충분히 설명할 수 있지만, 지금 셸 기준으로는 공식 재검증 진입점이 매끈하게 닫히지 않는다. 이 사실을 빼고 쓰면 문서가 현실보다 더 좋아 보이게 된다.

## 정리

B-federation-security-lab이 실제로 추가한 것은 로그인 수단 하나가 아니다. 이 랩이 늘린 것은 인증 성공까지의 단계 수다. provider callback, external identity linking, pending second factor, hashed recovery code, refresh reuse detection이 서로 다른 책임으로 분리되면서, "누가 들어왔는가"를 판정하는 문제 자체가 더 촘촘해진다. 다음 C 랩이 인가만 따로 떼어 읽힐 수 있는 것도, 여기서 인증 상태 기계가 한 번 더 세분화됐기 때문이다.
