# A-auth-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: "로컬 인증 백엔드"라는 요구를 처음 봤을 때, 단순 로그인/회원가입 API 정도를 떠올렸다. 먼저 `problem/README.md`부터 읽어 실제 범위를 확인한다.
- 진행: 성공 기준을 읽어 보니 refresh token rotation의 이유를 설명할 수 있어야 하고, cookie 인증에 CSRF 방어까지 요구한다. 처음엔 "그냥 JWT 발급하면 되는 거 아닌가"라고 생각했는데, 요구 범위가 훨씬 넓다.
- 이슈: 이메일 검증과 비밀번호 재설정을 별개 기능으로 생각하고 있었는데, 성공 기준을 보니 둘 다 "토큰 발급/소비"라는 같은 구조로 설명해야 한다.
- 판단: 로그인 엔드포인트를 먼저 만들기보다, 토큰 발급/소비라는 공통 기반을 먼저 설계하기로 했다.

CLI:

```bash
$ cd labs/A-auth-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: 등록 → 이메일 검증 → 로그인까지의 최소 경로를 만들고 테스트로 고정한다.
- 진행: `auth.py` 서비스 계층에서 `register_user`를 먼저 잡았다. 처음엔 이메일 중복 검사만 넣었는데, handle 중복도 막아야 한다는 걸 뒤늦게 깨달았다. 사용자 입장에서 email은 private이고 handle이 public identifier가 되니까.
- 이슈: 등록 직후 바로 로그인할 수 있게 했더니, 이메일 검증 없이도 서비스를 쓸 수 있게 되는 문제가 생겼다. `authenticate_user`에서 `email_verified_at`을 검사하지 않고 있었다.
- 조치: 로그인 시점에 `email_verified_at is None`이면 403을 던지도록 분기를 추가했다.

```python
if user.email_verified_at is None:
    raise AppError(
        code="EMAIL_NOT_VERIFIED",
        message="Verify the email address before signing in.",
        status_code=403,
    )
```

처음엔 인증 실패(401)로 돌려보내려고 했는데, "비밀번호를 틀린 것"과 "이메일을 안 한 것"은 다른 문제이므로 403이 맞다고 판단했다.

- 진행: 이메일 토큰 발급을 `register_user` 안에 같이 넣었다. 별도 "이메일 재전송" API를 만들 수도 있지만, 이 랩에서는 등록 시 바로 발급하는 단순한 경로로 충분하다.

```python
token = self._issue_email_token(user_id=user.id, kind="verify_email")
self._queue_email(mailbox=mailbox, to_email=user.email, kind="verify_email", token=token)
```

이 시점에서 `mailbox`가 실제 SMTP가 아니라 앱 상태에 올려 둔 리스트라는 사실이 중요하다. Mailpit을 붙이면 실제 메일 UI까지 볼 수 있지만, 통합 테스트에서는 이 in-memory mailbox로 토큰을 바로 꺼낸다.

- 검증: 등록 후 검증 안 한 채 로그인 시도하면 403, 검증 후 로그인하면 200이 나오는 걸 확인했다.

CLI:

```bash
$ pytest tests/integration/test_local_auth.py::test_local_login_refresh_rotation_and_logout -q
```

```
1 passed
```

### Session 3

- 목표: refresh token rotation을 구현한다. 처음엔 "refresh token을 보내면 새 access token을 주면 끝"이라고 생각했다.
- 이슈: 단순 재발급만 하면 탈취된 refresh token으로 무한히 세션을 연장할 수 있다. 이건 단순 만료 검사만으로는 막을 수 없다.
- 원인 추정: 처음 가설은 "refresh token에 짧은 TTL을 걸면 된다"였는데, TTL이 짧으면 정상 사용자도 자주 재인증해야 하는 문제가 생긴다.
- 판단: 대신 `family_id`로 하나의 로그인 세션에서 나온 토큰 계보를 묶고, 이미 revoke된 토큰이 다시 사용되면 가족 전체를 무효화하기로 했다.

```python
if token.revoked_at is not None:
    if token.reuse_detected_at is None:
        token.reuse_detected_at = now_utc()
    self.auth_repository.revoke_token_family(token.family_id, revoked_at=now_utc())
    raise AppError(
        code="REFRESH_TOKEN_REUSED",
        message="Refresh token reuse was detected. The whole session family was revoked.",
        status_code=401,
    )
```

나중에 보니 이 부분이 이 랩에서 가장 설명 가치가 높은 코드였다. 테스트에서 "공격자가 원본 refresh token을 재사용하면 정상 사용자의 새 토큰까지 전부 죽는다"는 시나리오를 실제로 재현한다.

- 검증: 테스트가 두 가지를 동시에 확인한다. 공격자의 재사용이 401로 막히는 것, 그리고 이미 rotation된 정상 토큰도 같은 family이므로 함께 죽는 것.

```python
reuse_response = attacker.post(
    "/api/v1/auth/token/refresh",
    headers={"X-CSRF-Token": "attacker-csrf"},
)
assert reuse_response.status_code == 401
assert reuse_response.json()["error"]["code"] == "REFRESH_TOKEN_REUSED"

family_revoked = client.post(
    "/api/v1/auth/token/refresh",
    headers={"X-CSRF-Token": rotated_csrf},
)
assert family_revoked.status_code == 401
```

이때까지는 "family 전체가 죽으면 정상 사용자도 재로그인해야 하는 게 맞나?"라는 의문이 있었는데, 토큰 탈취가 의심되는 상황에서는 강제 재인증이 더 안전한 선택이다.

- 다음: CSRF 보호를 cookie 기반 인증에 어떻게 엮을지 정리해야 한다.

CLI:

```bash
$ pytest tests/integration/test_local_auth.py -q
```

```
3 passed
```

### Session 4

- 목표: 비밀번호 재설정을 추가하고, CSRF 없이 refresh를 요청하면 막히는지 확인한다.
- 진행: 비밀번호 재설정은 이메일 검증과 같은 구조인 "토큰 발급 → 소비"인데, `kind`를 `password_reset`으로 바꾸면 된다. 처음엔 별도 테이블을 만들까 했지만, 같은 email_token 모델에 `kind` 필드로 구분하는 게 훨씬 깔끔했다.
- 이슈: `request_password_reset`에서 존재하지 않는 이메일을 넣으면 어떻게 해야 하나? 처음엔 404를 돌려보내려 했는데, 그러면 공격자가 이메일 존재 여부를 확인할 수 있다. 그래서 존재하지 않는 이메일이면 조용히 리턴하되 아무 토큰도 발급하지 않는 쪽으로 갔다.

```python
def request_password_reset(self, *, email: str, mailbox: list[dict[str, str]]) -> None:
    user = self.user_repository.get_by_email(email.strip().lower())
    if user is None:
        return
```

- 진행: CSRF 테스트는 `X-CSRF-Token` 헤더 없이 refresh를 요청하면 403이 나오는지 확인한다. cookie 기반 인증은 브라우저가 자동으로 쿠키를 붙여 보내므로, CSRF 토큰 없이 상태 변경 요청을 허용하면 cross-site 공격에 노출된다.
- 검증: 이전 비밀번호로 로그인하면 401, 새 비밀번호로 로그인하면 200. CSRF 없는 refresh는 403.

CLI:

```bash
$ pytest tests/integration/test_local_auth.py -q
```

```
3 passed
```

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
3 passed
```

### Session 5

- 목표: Compose 환경에서 전체가 부팅되고 health probe까지 응답하는지 확인한다.
- 진행: `docker compose up --build`로 앱, PostgreSQL, Mailpit을 같이 올렸다. `make smoke`는 `/api/v1/health/live`에 GET을 보내서 앱이 살아 있는지 확인한다.
- 이슈: 처음에 Compose 올렸을 때 PostgreSQL 연결 타이밍 문제가 있었다. 앱이 DB보다 먼저 뜨면 lifespan에서 `initialize_schema()`가 실패한다. `depends_on`과 health check를 맞춘 뒤 해결됐다.
- 검증: compile, lint, test, smoke, Compose live/ready probe 모두 통과.
- 다음: 이 랩은 로컬 인증까지만 잡고, OAuth와 2FA는 B-federation-security-lab으로 넘긴다.

CLI:

```bash
$ make smoke
$ docker compose up --build
$ curl http://localhost:8000/api/v1/health/live
```

```json
{"status": "ok"}
```
