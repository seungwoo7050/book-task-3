# A-auth-lab Structure Plan

## 한 줄 약속
- 로컬 인증을 refresh token family와 CSRF까지 끌고 가기

## 독자 질문
- 회원가입과 로그인만 만드는 대신, 세션 회전과 계정 회복까지 한 묶음으로 어디까지 설명할 것인가.
- access token과 refresh token을 왜 분리하는가 이메일 검증과 비밀번호 재설정을 같은 토큰 계열 문제로 어디까지 묶을 수 있는가 cookie 인증에서 CSRF를 어디에서 차단해야 하는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 로컬 인증을 단순 로그인보다 넓은 문제로 잡기
2. refresh rotation을 세션 경계의 중심으로 올리기
3. 테스트로 공격 시나리오를 문서화하기
4. 재검증으로 live/ready 표면을 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py::refresh_token` — refresh cookie, CSRF, 회전 실패를 한 자리에서 드러내는 진입점이다.
- 보조 앵커: `labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py::test_local_login_refresh_rotation_and_logout` — 토큰 재사용 공격과 family revoke 규칙을 실제 요청 순서로 고정한다.
- 문서 앵커: `labs/A-auth-lab/problem/README.md`, `labs/A-auth-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- 로컬 인증 흐름의 상태 전이와 실패 지점 계정 회복 흐름을 별도 토큰으로 나누는 이유 Mailpit 같은 로컬 개발 도구를 쓰는 이유와 한계
- access token과 refresh token의 책임을 나눠 세션 갱신과 탈취 위험 설명을 분리했습니다. 이메일 검증과 비밀번호 재설정을 모두 "토큰 발급/소비" 문제로 보되, 사용 목적과 만료 조건은 구분했습니다. OAuth와 2FA는 이 랩에 섞지 않고 다음 단계인 B-federation-security-lab로 넘겼습니다.

## 끝맺음
- 제외 범위: Google OAuth 같은 외부 로그인 TOTP 2FA와 recovery code 운영용 메일 인프라와 실제 외부 SMTP 검증
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다.
