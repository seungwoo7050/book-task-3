# A-auth-lab 문제 정의

frontend 없이도 로컬 계정 인증의 기본 lifecycle을 설명할 수 있는 Spring Boot 랩을 만든다.

## 성공 기준

- 회원가입, 로그인, refresh, logout, `me` 흐름이 현재 scaffold 안에서 동작한다.
- refresh token rotation, 이메일 검증, 비밀번호 재설정, cookie + CSRF 경계를 설명할 수 있다.
- 실행과 검증 명령은 [../spring/README.md](../spring/README.md)에서 바로 따라갈 수 있다.

## 이번 단계에서 다루지 않는 것

- 실제 브라우저 UI
- 외부 OAuth provider
- production-grade persistence와 메일 인프라 전체

이 디렉터리는 구현 코드가 아니라 canonical problem statement와 성공 기준을 다룬다.
