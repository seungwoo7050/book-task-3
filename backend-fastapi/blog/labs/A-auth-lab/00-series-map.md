# A-auth-lab

이 글은 회원가입과 로그인만 만드는 대신, 세션을 오래 안전하게 유지하는 규칙까지 어디서부터 설명해야 하는가라는 질문에서 출발한다. 로컬 계정 기반 인증 백엔드를 만든다고 가정하면 이메일 검증, 비밀번호 재설정, 세션 회전, CSRF 보호가 한 번에 엮이는데, A 랩은 그 묶음을 처음부터 끝까지 보여 주는 시작점이다.

## 이 글이 붙잡는 질문
로컬 인증 백엔드에서 access token과 refresh token을 왜 나누는지, 이메일 검증과 비밀번호 재설정을 어떤 토큰 흐름으로 설명할지, 그리고 cookie 기반 세션에서 CSRF를 어디서 차단할지를 하나의 이야기로 묶을 수 있는가가 이 글의 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README, docs, auth route, 통합 테스트, compose probe가 모두 같은 범위를 가리킨다. 그래서 다른 랩을 빌리지 않고도 로컬 인증의 상태 전이와 실패 지점을 독립적으로 따라갈 수 있다.

## 이번 글에서 따라갈 흐름
1. 회원가입과 로그인보다 넓은 인증 생애주기를 먼저 세운다.
2. refresh rotation과 token family를 세션 경계의 중심으로 올린다.
3. 재사용 공격과 계정 회복 시나리오를 테스트로 고정한다.
4. 재검증 기록으로 live/ready 표면까지 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py::refresh_token`
- 테스트/런타임: `labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py::test_local_login_refresh_rotation_and_logout`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/A-auth-lab/fastapi 8000`

## 이 글을 다 읽고 나면
- 로컬 인증 흐름에서 토큰이 어떻게 상태 전이를 만든다.
- 계정 회복 토큰을 로그인 토큰과 분리하는 이유가 선명해진다.
- Mailpit 같은 로컬 도구가 왜 개발 속도를 높이면서도 운영 대체재는 아닌지 감이 잡힌다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다.
- 다음으로 이어 볼 대상: B-federation-security-lab
