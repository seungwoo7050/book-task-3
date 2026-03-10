# 문제 프레이밍

## 학습 목표

로컬 계정 인증을 "회원가입 API 하나"로 축소하지 않고, 이메일 검증, 비밀번호 재설정, refresh token rotation, cookie + CSRF까지 포함한 전체 credential lifecycle로 이해하는 것이 목표다.

## 왜 중요한가

- 대부분의 서비스는 OAuth를 붙이기 전에 로컬 인증의 기본 경계를 먼저 갖춰야 한다.
- 인증 문제를 작은 랩으로 분리해야 이후의 federation, 2FA, RBAC가 덜 혼란스럽다.

## 선수 지식

- FastAPI 라우팅과 dependency 기본
- 비밀번호 해시와 토큰의 역할 차이
- PostgreSQL, Redis, Mailpit 같은 로컬 개발 도구의 기본 개념

## 성공 기준

- signup, login, email verification, password reset, refresh rotation 흐름이 모두 설명 가능해야 한다.
- `make lint`, `make test`, `make smoke`, `docker compose up --build`가 현재 워크스페이스를 검증해야 한다.
- CSRF mismatch, 만료 토큰, 미인증 이메일 같은 실패 경계가 문서와 테스트에 드러나야 한다.

## 제외 범위

- Google OAuth 같은 외부 로그인
- TOTP 2FA와 recovery code
- 실서비스형 SMTP 연동

이 랩의 핵심은 "로컬 인증을 전체 계정 수명주기로 설명할 수 있는가"에 있다. 이후 랩은 이 기반 위에 외부 로그인과 권한 모델을 덧붙인다.
