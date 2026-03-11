# 보안 정책

`v3-oss-hardening`은 학습 우선 self-hosted 후보 버전이다. production-ready 보안 보증을 제공하지는 않지만, 아래 범위는 현재 구현에 포함된다.

## 현재 포함된 보안 범위

- 이메일/비밀번호 인증
- `argon2` 비밀번호 해싱
- `HttpOnly` 쿠키 기반 서버 세션
- 역할 기반 route guard: `owner`, `operator`, `viewer`
- login/logout, user/settings 변경, CRUD, job enqueue에 대한 audit log

## 아직 포함되지 않은 범위

- SSO/OAuth
- MFA
- rate limiting
- secret rotation automation
- multi-tenant isolation
- external secret manager integration

## 제보 방법

이 study repository 안에서 보안 이슈를 발견했다면, public issue에 민감한 exploit detail을 그대로 올리지 말고 재현 조건과 영향 범위를 최소한으로 요약해 전달하는 것을 권장한다.

## 안전한 배포를 위한 전제

- 단일 팀 사용만 가정한다.
- private network 또는 로컬 환경에서 사용한다.
- reverse proxy와 TLS termination은 외부에서 구성한다.
- 기본 seed 계정 비밀번호는 부트스트랩 후 즉시 변경한다.
