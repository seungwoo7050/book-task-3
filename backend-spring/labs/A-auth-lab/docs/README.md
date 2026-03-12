# A-auth-lab 설계 메모

이 문서는 현재 scaffold가 어디까지 구현되었고, 무엇을 아직 일부러 남겼는지 빠르게 확인하는 용도다.

## 현재 구현 범위

- local account register, login, refresh, logout, `me`
- refresh rotation과 CSRF mismatch 예시 흐름
- Mailpit-ready Compose 환경

## 의도적 단순화

- 사용자와 토큰 persistence는 초기 scaffold 수준으로 가볍게 두었다
- cookie 동작은 브라우저 전체 통합보다 API 경계 설명에 집중했다
- 이메일 검증과 비밀번호 재설정은 full mail lifecycle보다 shape 설명이 우선이다

## 다음 개선 후보

- 사용자, verification token, refresh token family persistence
- 실제 response cookie 기반 동작 검증
- verify/reset endpoint의 구현 확장
