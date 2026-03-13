# B-federation-security-lab 시리즈 지도

이 시리즈는 로컬 인증 위에 외부 로그인과 2단계 인증을 어떻게 덧붙였는지, 실제 테스트와 서비스 코드 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- Google 스타일 로그인처럼 외부 공급자와 내부 사용자 계정 연결을 설명할 수 있어야 합니다.
- 2FA는 로그인 성공 이후에 덧붙는 옵션이 아니라, 별도 challenge 단계와 recovery code 정책을 가진 흐름이어야 합니다.

## 실제 구현 표면

- `/api/v1/auth/google/login`, `/google/callback`
- `/api/v1/auth/2fa/setup`, `/2fa/confirm`, `/2fa/verify`
- provider-linked identity와 recovery code 재발급 로직
- 로그인 보안 이벤트와 refresh rotation 재사용

## 대표 검증 엔트리

- `pytest tests/integration/test_google_callback.py -q`
- `pytest tests/integration/test_two_factor.py -q`
- `make smoke`

## 읽는 순서

1. [프로젝트 README](../../../labs/B-federation-security-lab/README.md)
2. [문제 정의](../../../labs/B-federation-security-lab/problem/README.md)
3. [실행 진입점](../../../labs/B-federation-security-lab/fastapi/README.md)
4. [Google callback 테스트](../../../labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py)
5. [2FA 테스트](../../../labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py)
6. [핵심 구현 1](../../../labs/B-federation-security-lab/fastapi/app/domain/services/auth.py)
7. [핵심 구현 2](../../../labs/B-federation-security-lab/fastapi/app/domain/services/two_factor.py)
8. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/B-federation-security-lab/README.md)
- [problem/README.md](../../../labs/B-federation-security-lab/problem/README.md)
- [fastapi/README.md](../../../labs/B-federation-security-lab/fastapi/README.md)
- [tests/integration/test_google_callback.py](../../../labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py)
- [tests/integration/test_two_factor.py](../../../labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py)
- [app/domain/services/auth.py](../../../labs/B-federation-security-lab/fastapi/app/domain/services/auth.py)
- [app/domain/services/two_factor.py](../../../labs/B-federation-security-lab/fastapi/app/domain/services/two_factor.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
