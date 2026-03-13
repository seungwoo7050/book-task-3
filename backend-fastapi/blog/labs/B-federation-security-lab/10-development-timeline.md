# B-federation-security-lab: 로컬 인증 위에 OIDC와 2FA를 덧씌우되, 단계는 더 잘게 쪼개기

이 글은 `labs/B-federation-security-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py::google_callback`, `labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py::test_two_factor_setup_and_recovery_code_login`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

B 랩은 A 랩 위에 기능을 덧붙이는 글처럼 보이기 쉽지만, 소스를 보면 관점이 조금 다르다. problem/README.md는 Google 스타일 로그인, TOTP, recovery code, audit log를 한꺼번에 내세우지만, docs/README.md는 외부 계정과 내부 계정 연결, 2FA 삽입 위치, recovery code 평문 금지처럼 전혀 다른 질문을 먼저 던진다. 즉 이 프로젝트는 기능 추가가 아니라 인증 상태 기계를 한 단계 더 잘게 쪼개는 실험이다.

## 1. 외부 공급자 계정과 내부 사용자 계정의 연결 문제로 다시 시작하기
처음에는 공급자 계정과 내부 사용자 계정을 어떻게 붙일지가 중심이었다. README.md와 problem/README.md는 모두 'Google 로그인 추가'보다 'provider-linked identity 관리'를 먼저 적는다. 그래서 chronology의 출발점도 route 수를 늘리는 게 아니라, 어떤 데이터가 공급자에서 오고 어떤 상태가 우리 서비스에서 생성되는지 구분하는 일로 보는 편이 자연스럽다.

## 2. OIDC callback을 세션 발급 경계로 세우기
그 전환점이 google_callback이다. 이 함수는 query의 code, state를 받고, cookie에 저장된 signed state가 없으면 즉시 실패한다. 즉 callback은 외부 공급자 응답을 그대로 통과시키는 곳이 아니라, state cookie와 code verifier를 확인해 내부 세션으로 번역하는 경계다.

```python
def google_callback(
    request: Request,
    code: str,
    state: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    oidc_service: Annotated[GoogleOIDCService, Depends(get_google_oidc_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> JSONResponse:
    signed_state = request.cookies.get(settings.oauth_state_cookie_name)
    if not signed_state:
        raise AppError(
            code="OAUTH_STATE_REQUIRED",
```

눈여겨볼 부분은 provider state 확인, code 교환, 내부 세션 발급이 한 callback 안에서 이어진다는 점이다.

## 3. 2FA와 recovery code를 별도 단계로 검증하기
그 다음부터 인증은 더 이상 한 번에 끝나지 않는다. tests/integration/test_two_factor.py를 보면 Google 로그인 직후 2FA setup과 confirm을 마친 뒤, 다시 로그인했을 때 곧바로 me가 통과하지 않는다. 대신 recovery code나 TOTP code를 한 번 더 통과해야 authenticated가 된다. 이 테스트가 중요한 이유는, 2FA를 '로그인 성공 뒤 부가 기능'이 아니라 '인증을 한 번 더 완결시키는 후속 단계'로 고정하기 때문이다.

```python
def test_two_factor_setup_and_recovery_code_login(client: TestClient, monkeypatch) -> None:
    _mock_google(
        monkeypatch, subject="google-subject-2", email="twofa@example.com", name="Two Factor"
    )
    _complete_google_login(client)

    csrf_token = client.cookies["csrf_token"]
    setup_response = client.post("/api/v1/auth/2fa/setup", headers={"X-CSRF-Token": csrf_token})
    assert setup_response.status_code == 200
    secret = setup_response.json()["secret"]

    confirm_response = client.post(
```

테스트는 2FA 등록, 재로그인 challenge, recovery code 소진을 하나의 상태 기계로 묶는다.

## 4. 2026-03-09 재검증으로 mock 기반 보안 surface를 고정하기
마지막 검증은 mock 경계를 분명히 남긴다. 보고서에는 2026-03-09에 compile, lint, test, smoke, Compose probe가 통과했다고 적혀 있고, 실제 Google 통신 대신 monkeypatch 기반 OIDC 경로를 사용한다. 그래서 이 글도 일부러 'Google 연동이 완성됐다'고 쓰지 않고, 'OIDC callback과 내부 세션 발급 경계가 mock 기반으로 재현된다'고 적는 편이 더 사실에 가깝다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/B-federation-security-lab/fastapi 8000
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, PostgreSQL 데이터베이스 이름을 DATABASE_URL과 맞춘 뒤 재검증했다. 실제 Google end-to-end는 범위 밖이므로, 글에서도 mock OIDC 경계를 명시적으로 유지한다.

## 정리
B 랩이 남기는 가장 큰 변화는 인증 성공의 단계를 늘렸다는 점이다. 외부 로그인과 2FA를 붙였지만, 더 중요한 건 각 단계가 내부 상태 기계에서 어디에 놓이는지 분리했다는 사실이다. 다음 C 랩이 인증 자체를 비워 두고 인가 규칙만 다룰 수 있는 것도, 여기까지 오면서 '누가 들어왔는가'와 '들어온 뒤 무엇을 할 수 있는가'가 확실히 갈라졌기 때문이다.
