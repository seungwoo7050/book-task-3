# B-federation-security-lab Structure Plan

## 한 줄 약속
- 로컬 인증 위에 OIDC와 2FA를 덧씌우되, 단계는 더 잘게 쪼개기

## 독자 질문
- 외부 로그인과 보안 강화 기능을 기존 세션 모델 위에 붙일 때, 어떤 단계부터 추가 복잡성을 드러낼 것인가.
- 외부 공급자 계정과 내부 사용자 계정을 어떻게 연결할 것인가 2FA를 로그인 흐름 어디에 끼워 넣을 것인가 recovery code는 왜 평문으로 두면 안 되는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 외부 공급자 계정과 내부 사용자 계정의 연결 문제로 다시 시작하기
2. OIDC callback을 세션 발급 경계로 세우기
3. 2FA와 recovery code를 별도 단계로 검증하기
4. 2026-03-09 재검증으로 mock 기반 보안 surface를 고정하기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py::google_callback` — provider state, code 교환, 내부 세션 발급이 만나는 지점이다.
- 보조 앵커: `labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py::test_two_factor_setup_and_recovery_code_login` — 2FA 등록, 확인, 재로그인 challenge, recovery code 소진까지 한 흐름으로 묶는다.
- 문서 앵커: `labs/B-federation-security-lab/problem/README.md`, `labs/B-federation-security-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- OIDC 진입과 내부 세션 발급의 차이 보안 강화 흐름의 단계 분리 throttling과 audit log의 역할
- Google OIDC 로그인 흐름 외부 계정과 내부 사용자 계정 연결 TOTP 기반 2단계 인증 테스트는 실제 Google 서비스가 아니라 mock 경로를 사용합니다. 제품 도메인 로직은 넣지 않고 인증 보안 흐름만 분리합니다.

## 끝맺음
- 제외 범위: 실제 Google 서비스와의 end-to-end 통신 검증 제품 도메인별 권한과 리소스 모델 복수 공급자에 대한 공통 추상화 완성
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, PostgreSQL 데이터베이스 이름을 `DATABASE_URL`과 맞춘 뒤 재검증했다.
