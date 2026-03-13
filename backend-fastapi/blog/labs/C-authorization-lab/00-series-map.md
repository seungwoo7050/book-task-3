# C-authorization-lab 시리즈 지도

이 시리즈는 인증을 잠시 옆으로 밀어 두고, 워크스페이스와 역할 모델이 실제 서비스 계층에서 어떻게 강제되는지 소스 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 워크스페이스 생성, 초대, 수락, 역할 변경을 서로 다른 권한 규칙으로 설명할 수 있어야 합니다.
- "누가 무엇을 할 수 있는가"를 로그인 메커니즘과 분리해도 테스트 가능한지 확인해야 합니다.

## 실제 구현 표면

- `/api/v1/authorization/users`, `/workspaces`, `/invites`
- 초대 수락과 거절
- `viewer`, `member`, `admin`, `owner` 역할 순서
- 문서 생성과 읽기에서 드러나는 권한 경계

## 대표 검증 엔트리

- `pytest tests/integration/test_authorization_flows.py -q`
- `make smoke`

## 읽는 순서

1. [프로젝트 README](../../../labs/C-authorization-lab/README.md)
2. [문제 정의](../../../labs/C-authorization-lab/problem/README.md)
3. [실행 진입점](../../../labs/C-authorization-lab/fastapi/README.md)
4. [대표 통합 테스트](../../../labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py)
5. [핵심 구현](../../../labs/C-authorization-lab/fastapi/app/domain/services/authorization.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/C-authorization-lab/README.md)
- [problem/README.md](../../../labs/C-authorization-lab/problem/README.md)
- [fastapi/README.md](../../../labs/C-authorization-lab/fastapi/README.md)
- [tests/integration/test_authorization_flows.py](../../../labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py)
- [app/domain/services/authorization.py](../../../labs/C-authorization-lab/fastapi/app/domain/services/authorization.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
