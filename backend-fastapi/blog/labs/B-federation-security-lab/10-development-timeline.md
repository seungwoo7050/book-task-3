# B-federation-security-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: A-auth-lab에서 로컬 인증을 끝낸 뒤, 외부 로그인을 어떻게 덧붙이는지 확인한다. 처음엔 "Google OAuth를 그대로 붙이면 되는 거 아닌가"라고 생각했다.
- 진행: `problem/README.md`를 먼저 읽었다. 외부 로그인뿐 아니라 2FA, recovery code, 감사 로그까지 같은 랩에 들어 있다. 단순 OAuth 연동이 아니라 "계정 진입 경로를 단단하게 만드는" 전체 보안 강화 흐름이다.
- 이슈: 처음엔 Google 로그인 = 새 계정 생성이라고 단순하게 봤는데, 기존 로컬 계정과 같은 이메일을 쓰는 Google 사용자가 들어오면 어떻게 해야 하나? 새 계정을 또 만들면 한 사람이 두 계정을 갖게 된다.
- 판단: 이 문제를 먼저 풀어야 Google 로그인의 실제 구조를 잡을 수 있다.

CLI:

```bash
$ cd labs/B-federation-security-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: `sync_google_user`를 구현하면서 외부 계정과 내부 계정의 연결 로직을 설계한다.
- 진행: 첫 번째 시도는 단순했다. external identity 테이블에서 google subject로 먼저 찾고, 없으면 새 유저를 만드는 것. 그런데 이렇게 하면 "이미 로컬 가입된 이메일"을 가진 Google 계정이 들어올 때 중복이 생긴다.
- 조치: email_verified인 Google 계정이라면 기존 이메일 사용자를 찾아 연결하는 중간 단계를 넣었다.

```python
user = self.user_repository.get_by_external_identity("google", subject)
if user is None:
    if email_verified:
        user = self.user_repository.get_by_email(email)
    if user is None:
        handle_seed = str(profile.get("preferred_username") or email.split("@")[0])
```

처음엔 `email_verified` 체크 없이 이메일만으로 연결하려 했는데, 그러면 email_verified=False인 외부 계정이 다른 사람의 로컬 계정을 탈취할 수 있다. 이 검사 하나가 보안상 결정적이다.

- 이슈: Google 로그인 테스트를 어떻게 쓸지 고민했다. 실제 Google 서버를 호출할 수는 없다.
- 판단: `monkeypatch`로 OIDC 서비스의 `exchange_code_for_tokens`, `validate_id_token`, `fetch_userinfo`를 모두 교체하기로 했다. 테스트가 확인하는 건 Google의 실제 응답이 아니라, 우리 코드가 프로필을 받아서 세션을 만드는 흐름이니까.
- 검증: mock callback으로 로그인하면 쿠키 세 개(`access_token`, `refresh_token`, `csrf_token`)가 발급되고, `/auth/me`로 사용자 정보를 확인할 수 있다.

CLI:

```bash
$ pytest tests/integration/test_google_callback.py -q
```

```
1 passed
```

### Session 3

- 목표: 2FA를 추가한다. 처음엔 "로그인 성공 후 TOTP 코드를 한 번 더 확인하면 끝"이라고 생각했다.
- 진행: `TwoFactorService`를 만들면서 TOTP secret 생성과 provisioning URI 발급을 먼저 구현했다. pyotp를 직접 감싸는 얇은 레이어다.
- 이슈: 2FA가 켜진 사용자가 Google 로그인으로 들어오면 어떤 시점에서 challenge를 걸어야 하나? 처음엔 callback에서 바로 TOTP를 물어보려 했는데, callback 시점엔 아직 완전한 세션이 아니다.
- 판단: callback에서 2FA가 필요한 사용자에게는 `pending_auth_token`을 발급하고, 2FA 검증이 끝난 뒤에야 진짜 세션(cookie)을 만들기로 했다. 두 단계를 명확히 분리하는 게 핵심이다.

```python
def start_pending_second_factor(self, *, user: User, ip_address, user_agent) -> str:
    self.auth_repository.store_audit_event(
        event_type="auth.login.challenge_required",
        user_id=user.id,
        details={"provider": "google"},
        ip_address=ip_address,
        user_agent=user_agent,
    )
    self.session.commit()
    return build_pending_auth_token(user.id, self.settings)
```

이 시점에서 "challenge_required" 이벤트를 감사 로그에 남기는 것도 같이 넣었다. 나중에 보면 누가 2FA challenge를 받았는지 추적할 수 있다.

- 진행: recovery code 생성도 같이 구현했다. 처음엔 단순 UUID를 쓰려 했는데, 사용자가 직접 적어 둬야 하는 코드이므로 읽기 쉬운 `XXXX-XXXX` 포맷으로 바꿨다.

```python
def generate_recovery_codes(self, count: int = 8) -> list[str]:
    alphabet = string.ascii_uppercase + string.digits
    codes: list[str] = []
    for _ in range(count):
        left = "".join(secrets.choice(alphabet) for _ in range(4))
        right = "".join(secrets.choice(alphabet) for _ in range(4))
        codes.append(f"{left}-{right}")
    return codes
```

- 다음: 2FA 확인 후 recovery code로 로그인하는 전체 흐름을 테스트로 고정해야 한다.

### Session 4

- 목표: 2FA setup → confirm → 재로그인 시 challenge → recovery code 로그인까지 전체 흐름을 테스트로 묶는다.
- 진행: `test_two_factor.py`를 작성했다. Google 로그인으로 먼저 세션을 만들고, 2FA setup → confirm을 거친 뒤, 다시 Google 로그인을 시도한다.
- 이슈: 2FA confirm 후 다시 Google 로그인을 했는데 `/auth/me`가 200을 돌려보냈다. 왜? 이전 세션 쿠키가 아직 살아 있어서 challenge를 건너뛴 것이다.
- 조치: 재로그인 테스트에서 이전 쿠키가 있어도 2FA 사용자는 `pending_auth_token`만 받고, 완전한 세션은 2FA 검증 후에야 발급되도록 흐름을 확인했다. 테스트에서 `assert client.get("/api/v1/auth/me").status_code == 401`로 이 경계를 고정시켰다.

```python
_complete_google_login(client)
assert client.get("/api/v1/auth/me").status_code == 401  # pending challenge

challenge_csrf = client.cookies["csrf_token"]
verify_response = client.post(
    "/api/v1/auth/2fa/verify",
    json={"recovery_code": recovery_codes[0]},
    headers={"X-CSRF-Token": challenge_csrf},
)
assert verify_response.status_code == 200
assert client.get("/api/v1/auth/me").status_code == 200  # now authenticated
```

나중에 보니 이 테스트가 이 랩에서 가장 중요한 경계를 잡는다. "Google 로그인 성공"과 "완전한 세션 획득"은 2FA 사용자에게는 별개의 단계다.

- 검증: Google callback + 2FA setup + recovery code 로그인까지 전체가 하나의 테스트에서 확인된다.

CLI:

```bash
$ pytest tests/integration/test_two_factor.py -q
```

```
1 passed
```

```bash
$ pytest tests/integration/ -q
```

```
2 passed
```

### Session 5

- 목표: 전체 검증 루프를 돌리고 Compose 환경에서 서비스가 뜨는지 확인한다.
- 이슈: compose 실행 중 PostgreSQL 데이터베이스 이름이 `DATABASE_URL` 환경변수와 맞지 않는 문제가 있었다. compose.yaml의 `POSTGRES_DB`와 `.env`의 `DATABASE_URL`이 가리키는 DB 이름을 맞춘 뒤 해결됐다.
- 검증: compile, lint, test, smoke, Compose live/ready probe 모두 통과.
- 다음: 이 랩은 인증 방식 강화까지만 잡고, "누가 무엇을 할 수 있는가"라는 권한 문제는 C-authorization-lab으로 넘긴다.

CLI:

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
2 passed
```

```bash
$ make smoke
$ docker compose up --build
```
