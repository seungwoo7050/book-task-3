# A-auth-lab development timeline

실제 작업 세션 로그를 그대로 갖고 있지는 않아서, 이 글은 현재 남아 있는 source of truth만으로 chronology를 다시 복원한다. 순서는 `problem/README.md`의 성공 기준, `auth.py`의 public surface, `AuthService`와 token model의 상태 전이, 통합 테스트가 고정한 공격 시나리오, 마지막 재실행 CLI 순으로 잡았다. 중요한 건 "처음부터 답을 알고 쓴 정리문"처럼 매끈하게 보이는 것이 아니라, 이 랩이 어디서 단순 로그인 예제를 벗어났는지를 드러내는 일이다.

## Phase 1. 로그인보다 넓은 auth surface를 먼저 세운다

가장 먼저 눈에 들어오는 건 endpoint 배열이다. [`auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py)에는 `register`, `verify-email`, `login`, `password-reset/request`, `password-reset/confirm`, `token/refresh`, `logout`이 모두 들어 있다. `problem/README.md`가 요구한 "회원가입 + 이메일 검증 + 세션 유지 + 상태 변경 보호"가 이 한 파일에서 이미 공개 표면으로 굳어 있는 셈이다.

처음엔 이 랩을 회원가입과 로그인 정도로 읽을 수도 있어 보였다. 그런데 route 목록을 다시 찍어 보니 질문이 바로 넓어진다.

```bash
rg -n '"/register"|"verify-email"|password-reset|"/token/refresh"|"/logout"' \
  backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py
```

이 출력은 A 랩이 "첫 auth API"가 아니라 계정 생애주기를 어디까지 한 프로젝트에 담을지 정하는 랩이라는 걸 먼저 알려 준다. 여기에 [`app/main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/main.py) 의 `app.state.mailbox = []`와 `AuthService._queue_email()`를 같이 보면, 외부 SMTP 없이도 메일 검증과 비밀번호 재설정을 로컬에서 재현할 수 있게 만들려 했다는 방향도 잡힌다.

## Phase 2. refresh token family를 세션의 핵심 규칙으로 올린다

이 랩에서 진짜 전환점은 로그인 성공이 아니라 refresh rotation이다. [`RefreshToken`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/db/models/auth.py) 모델에는 `family_id`, `parent_token_id`, `revoked_at`, `reuse_detected_at`가 따로 있고, [`AuthService.rotate_refresh_token()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/domain/services/auth.py) 는 단순 재발급에서 멈추지 않고 token reuse를 감지하면 family 전체를 revoke한다.

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

이 지점에서 판단이 달라진다. refresh token은 세션 편의 기능이 아니라 탈취 흔적을 드러내는 보안 경계다. `docs/README.md`가 access/refresh 분리를 첫 질문으로 잡는 이유도 여기서 곧바로 설명된다.

## Phase 3. cookie 인증과 CSRF를 별도 실패면으로 분리한다

rotation만 있으면 충분할 것 같았는데, route surface를 다시 읽으면 그렇지 않다. [`/token/refresh`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py) 와 [`/logout`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py) 에는 둘 다 `Depends(require_csrf)`가 붙어 있고, [`validate_csrf()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/core/security.py) 는 cookie와 header를 함께 비교해 실패를 403으로 잘라 낸다.

통합 테스트는 이 분리를 더 또렷하게 고정한다. 정상 클라이언트가 refresh 후 새 CSRF cookie를 받고, 공격자 클라이언트는 예전 refresh token과 임의 header를 들고 들어와 `REFRESH_TOKEN_REUSED`를 받고, header 없이 refresh를 날리면 `CSRF_VALIDATION_FAILED`가 터진다.

```bash
rg -n 'family_id|REFRESH_TOKEN_REUSED|require_csrf|CSRF_VALIDATION_FAILED' \
  backend-fastapi/labs/A-auth-lab/fastapi/app/domain/services/auth.py \
  backend-fastapi/labs/A-auth-lab/fastapi/app/api/deps.py \
  backend-fastapi/labs/A-auth-lab/fastapi/app/core/security.py \
  backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py
```

이 랩이 의미 있는 건 보안 개념을 늘어놓아서가 아니라, reuse detection과 CSRF failure를 서로 다른 실패 코드로 보여 준다는 점이다.

## Phase 4. recovery 흐름을 같은 token 계열 문제로 묶는다

비밀번호 재설정은 별도 기능처럼 보이지만, 실제로는 이메일 검증과 거의 같은 토큰 저장소를 재사용한다. [`EmailToken`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/db/models/auth.py) 모델은 `kind`, `token_hash`, `expires_at`, `used_at`만으로 verify/reset 둘 다 다루고, `AuthService._issue_email_token()`이 `verify_email`과 `password_reset`을 TTL만 바꿔 발급한다. 그러니까 이 랩의 회복 흐름은 새로운 체계를 또 하나 만드는 일이 아니라 "같은 토큰 계열에서 목적과 만료만 분리하는 것"에 가깝다.

테스트의 `test_password_reset_flow()`가 old password 로그인 실패와 new password 로그인 성공을 같이 확인하는 이유도 바로 여기 있다. recovery는 편의 기능이 아니라 세션 경계의 일부다.

## Phase 5. 오늘 다시 돌린 검증은 구현보다 환경의 흔들림을 먼저 드러냈다

문서만 읽으면 이 랩은 이미 닫힌 것처럼 보이는데, 2026-03-14 현재 셸에서 다시 실행해 보니 상태가 다르다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇게 갈린다.

- `make lint`: [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/health.py) 의 주석 한 줄이 `E501`로 실패한다.
- `make test`: `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: `python3`가 Homebrew 경로를 타면서 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`와 `PYTHONPATH=. python -m tests.smoke`: 둘 다 `argon2-cffi` 부재로 `ModuleNotFoundError: No module named 'argon2'`.

즉 이 랩은 설계와 코드 surface 자체는 또렷하지만, "문서에 적힌 명령을 그대로 치면 바로 재현된다"는 상태는 아니다. 예전 verification 기록이 있더라도, 지금 읽는 사람에게 중요한 건 현재 셸에서 어떤 지점이 바로 깨지는지까지 함께 적어 두는 일이다.

## 정리

A-auth-lab은 로컬 인증을 처음 여는 랩이지만, 실제 중심은 로그인 성공이 아니다. 이 랩이 진짜로 고정하는 건 token family, reuse detection, CSRF validation, recovery token이라는 네 가지 세션 규칙이다. 그래서 다음 단계인 B 랩이 OIDC나 2FA를 붙일 수 있는 것도, 이미 여기서 "세션을 오래 안전하게 유지하려면 어디서 경계를 세워야 하는가"가 한 번 정리돼 있기 때문이다.
