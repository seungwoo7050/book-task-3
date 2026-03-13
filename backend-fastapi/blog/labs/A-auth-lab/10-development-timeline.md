# A-auth-lab: 로컬 인증을 refresh token family와 CSRF까지 끌고 가기

이 글은 `labs/A-auth-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py::refresh_token`, `labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py::test_local_login_refresh_rotation_and_logout`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

A 랩의 핵심은 회원가입 API를 많이 만드는 데 있지 않았다. problem/README.md와 docs/README.md를 같이 읽어 보면, 진짜 질문은 access token과 refresh token을 왜 나누는지, 이메일 검증과 비밀번호 재설정을 어디까지 같은 토큰 문제로 설명할 수 있는지, 그리고 cookie 인증에서 CSRF를 어디서 차단할지였다. 그래서 chronology도 자연스럽게 가입 -> 로그인보다 회전 -> 회복 -> 보호 쪽으로 읽어야 맞는다.

## 1. 로컬 인증을 단순 로그인보다 넓은 문제로 잡기
먼저 public auth surface를 넓혔다. app/api/v1/routes/auth.py에는 register, verify_email, login, request_password_reset, confirm_password_reset, refresh_token, logout이 한 파일에 모여 있다. 이 배열만 봐도 이 랩이 단순 로그인 실습이 아니라 계정 생애주기를 처음부터 끝까지 붙잡으려 했다는 걸 알 수 있다. README.md가 access/refresh 책임 분리를 먼저 설명하는 이유도 여기서 이어진다.

## 2. refresh rotation을 세션 경계의 중심으로 올리기
전환점은 refresh rotation이었다. refresh_token route는 refresh cookie가 없으면 바로 401을 내고, 이후 서비스 계층이 token family 재발급과 reuse 탐지를 맡는다. 여기서 중요한 건 세션 갱신을 편의 기능으로 두지 않고, 탈취 여부를 판정하는 보안 경계로 올렸기 때문이다. docs/README.md가 access/refresh 분리를 첫 질문으로 잡는 이유도 이 함수에서 바로 확인된다.

```python
def refresh_token(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    refresh_token = request.cookies.get(settings.refresh_cookie_name)
    if not refresh_token:
        raise AppError(
            code="REFRESH_TOKEN_REQUIRED",
            message="Refresh token cookie is required.",
            status_code=401,
        )
```

여기서 핵심은 refresh cookie, CSRF, 회전 실패가 모두 이 진입점에서 갈라진다는 점이다.

## 3. 테스트로 공격 시나리오를 문서화하기
테스트는 이 경계를 훨씬 선명하게 만든다. tests/integration/test_local_auth.py는 정상적인 refresh뿐 아니라, 옛 refresh를 가진 공격자 클라이언트를 별도로 만들고 REFRESH_TOKEN_REUSED가 터지는지 본다. 이어서 같은 family 전체가 revoke되어 정당한 클라이언트도 재로그인이 필요해지는지 확인한다. 덕분에 글에서도 'rotation이 왜 필요한가'를 추상 설명이 아니라 실제 실패 응답으로 쓸 수 있다.

```python
def test_local_login_refresh_rotation_and_logout(client: TestClient) -> None:
    _register_and_verify(client)

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "player@example.com", "password": "super-secret-1"},
    )
    assert login_response.status_code == 200
    assert client.cookies.get("access_token")
    assert client.cookies.get("refresh_token")
    assert client.cookies.get("csrf_token")
```

테스트는 토큰 재사용 공격과 family revoke 규칙을 실제 요청 순서로 고정한다.

## 4. 재검증으로 live/ready 표면을 닫기
마지막은 CLI로 닫힌다. 검증 보고서에 따르면 2026-03-09에 python3 -m compileall app tests, make lint, make test, make smoke, ./tools/compose_probe.sh labs/A-auth-lab/fastapi 8000이 실제로 다시 실행됐다. 여기서 중요한 건 smoke만이 아니라 live/ready probe까지 따로 남아 있다는 점이다. 독립 프로젝트로 읽히는 이유도 이 진입점 덕분에 가능해졌다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/A-auth-lab/fastapi 8000
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다. 이 랩의 재실행은 GitHub Actions matrix와 같은 make surface를 따랐다.

## 정리
그래서 A 랩의 development timeline은 '가입 API를 만들었다'가 아니라 '세션을 오래 들고 가기 위해 어떤 토큰 규칙과 공격 차단선을 먼저 세웠는가'로 읽어야 한다. 다음 B 랩이 외부 로그인과 2FA를 붙일 수 있었던 것도, 이미 여기서 로컬 인증의 상태 전이가 충분히 분리돼 있었기 때문이다.
