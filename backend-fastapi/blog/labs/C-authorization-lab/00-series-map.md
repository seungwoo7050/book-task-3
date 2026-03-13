# C-authorization-lab

이 글은 로그인 이후에 남는 문제, 즉 누가 무엇을 할 수 있는가를 인증과 분리해서 읽어 보는 랩이다. 인증이 사용자를 확인하는 일이라면, C 랩은 역할과 소유권, 초대 규칙을 어디까지 별도 정책으로 세울 수 있는지에 집중한다.

## 이 글이 붙잡는 질문
역할, 초대, 소유권, resource scope를 인증 흐름과 분리해도 정책이 흐려지지 않도록 하려면 어떤 규칙을 인가 surface에 올려야 하는가가 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
problem 문서와 docs는 인가 규칙을 별도 주제로 떼어 놓고, policy code와 통합 테스트는 승격과 거절 시나리오를 직접 보여 준다. 그래서 이 글은 "로그인 다음 단계"가 아니라 정책 엔진을 읽는 입구가 된다.

## 이번 글에서 따라갈 흐름
1. 인가 문제를 인증의 부속 기능이 아니라 별도 규칙 집합으로 정의한다.
2. route와 service에서 actor, workspace, role payload가 만나는 지점을 찾는다.
3. viewer 거절과 promote 후 허용을 테스트로 굳힌다.
4. 재검증 기록으로 단일 서비스 안의 정책 surface를 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py::create_invite`
- 테스트/런타임: `labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py::test_invite_accept_promote_and_document_permissions`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/C-authorization-lab/fastapi 8001`

## 이 글을 다 읽고 나면
- actor, workspace, role 조합이 어떻게 권한 판단의 최소 입력이 되는지 보게 된다.
- 초대와 승격이 왜 CRUD가 아니라 상태 전이인지 이해하게 된다.
- 정책을 중앙화했을 때 테스트가 어떤 회귀선을 제공하는지 알게 된다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다.
- 다음으로 이어 볼 대상: D-data-api-lab
