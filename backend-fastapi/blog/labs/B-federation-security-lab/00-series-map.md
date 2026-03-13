# B-federation-security-lab

이 글은 로컬 인증이 닫힌 뒤 외부 provider와 2FA가 들어오면 인증 상태 기계가 어떻게 늘어나는가를 따라간다. 목표는 로그인 수단을 하나 더 추가하는 데 있지 않고, callback, second factor, recovery code가 들어와도 auth surface를 설명 가능한 상태로 유지하는 데 있다.

## 이 글이 붙잡는 질문
OIDC callback, 로컬 계정, 2FA 등록과 재로그인 challenge, recovery code 소진까지 포함해도 인증 흐름을 한 덩어리의 상태 기계로 읽어 낼 수 있는가가 이 글이 붙잡는 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs는 provider 연동을 보안 기능과 분리하지 않고 설명하고, route와 통합 테스트는 그 상태 전이를 그대로 검증한다. 덕분에 이 랩은 "소셜 로그인 추가"가 아니라 인증 복잡성이 어떻게 확장되는지 보여 주는 독립 사례가 된다.

## 이번 글에서 따라갈 흐름
1. federated login을 편의 기능이 아니라 상태 기계 확장으로 읽는다.
2. callback에서 provider state, code 교환, 내부 세션 발급이 만나는 지점을 본다.
3. 2FA 등록, 확인, recovery code 흐름을 테스트로 묶는다.
4. 재검증 기록으로 provider mock과 compose surface를 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py::google_callback`
- 테스트/런타임: `labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py::test_two_factor_setup_and_recovery_code_login`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/B-federation-security-lab/fastapi 8000`

## 이 글을 다 읽고 나면
- 외부 provider와 내부 세션이 어떤 경계에서 만나는지 이해하게 된다.
- 2FA secret, challenge, recovery code가 서로 다른 실패 경로를 만든다는 점이 보인다.
- 인증 수단이 늘어날수록 테스트가 왜 더 중요한 문서가 되는지 알게 된다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, PostgreSQL 데이터베이스 이름을 DATABASE_URL과 맞춘 뒤 재검증했다.
- 다음으로 이어 볼 대상: C-authorization-lab
