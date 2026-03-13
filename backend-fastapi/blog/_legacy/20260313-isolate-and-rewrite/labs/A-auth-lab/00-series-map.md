# A-auth-lab 시리즈 지도

이 시리즈는 로컬 계정 인증을 어디까지 한 묶음으로 설명해야 하는지, 실제 소스와 테스트를 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 회원가입, 이메일 검증, 로그인, 비밀번호 재설정이 따로 흩어지지 않고 하나의 인증 흐름으로 이어져야 합니다.
- 세션 갱신과 상태 변경 요청 보호도 같은 경계 안에서 설명할 수 있어야 합니다.

## 실제 구현 표면

- `/api/v1/auth/register`, `/verify-email`, `/login`, `/logout`
- `/api/v1/auth/token/refresh`, `/password-reset/request`, `/password-reset/confirm`
- cookie 기반 세션과 `X-CSRF-Token` 검증
- Mailpit을 기준으로 한 메일 토큰 확인 경로

## 대표 검증 엔트리

- `pytest tests/integration/test_local_auth.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/A-auth-lab/README.md)
2. [문제 정의](../../../labs/A-auth-lab/problem/README.md)
3. [실행 진입점](../../../labs/A-auth-lab/fastapi/README.md)
4. [대표 통합 테스트](../../../labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py)
5. [핵심 구현](../../../labs/A-auth-lab/fastapi/app/domain/services/auth.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/A-auth-lab/README.md)
- [problem/README.md](../../../labs/A-auth-lab/problem/README.md)
- [fastapi/README.md](../../../labs/A-auth-lab/fastapi/README.md)
- [tests/integration/test_local_auth.py](../../../labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py)
- [app/domain/services/auth.py](../../../labs/A-auth-lab/fastapi/app/domain/services/auth.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
