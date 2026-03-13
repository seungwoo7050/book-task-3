# C-authorization-lab Structure Plan

## 한 줄 약속
- 로그인에서 한 걸음 물러서서, 누가 무엇을 할 수 있는지만 고립시키기

## 독자 질문
- 워크스페이스 초대, 역할 변경, 문서 접근 제어를 인증 메커니즘과 분리해도 설명 가능한가.
- 역할과 소유권은 무엇이 다른가 초대 흐름에서 누가 상태를 바꿀 수 있는가 인가 규칙을 테스트하기 좋은 경계는 어디인가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 로그인 대신 actor와 역할표부터 세우기
2. 초대 lifecycle을 인가 규칙의 중심으로 잡기
3. 권한 상승과 접근 거부를 테스트로 고정하기
4. 2026-03-09 재검증으로 규칙 surface를 다시 확인하기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py::create_invite` — 인가 규칙이 user actor, workspace, role payload를 한 번에 받는 중심 surface다.
- 보조 앵커: `labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py::test_invite_accept_promote_and_document_permissions` — viewer가 문서를 못 만들다가 promote 뒤에 만들 수 있게 되는 핵심 전환을 담는다.
- 문서 앵커: `labs/C-authorization-lab/problem/README.md`, `labs/C-authorization-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- 워크스페이스 역할 표 invitation lifecycle 리소스 접근 제어를 서비스 계층에서 다루는 이유
- workspace membership 모델 invitation 생성, 수락, 거절 흐름 RBAC 역할 경계 인증은 별도 헤더 기반 actor 모델로 단순화합니다. 핵심은 "누가 할 수 있나"이지 "어떻게 로그인했나"가 아닙니다.

## 끝맺음
- 제외 범위: 실제 로그인 시스템과 세션 관리 정책 엔진 같은 고급 외부 권한 시스템 조직 간 멀티테넌시 전체 설계
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다.
