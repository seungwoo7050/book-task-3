# B-federation-security-lab 문제 정의

로컬 계정 인증 이후에 federation, 2FA, audit 같은 인증 강화 요소가 설계를 어떻게 바꾸는지 보여주는 Spring 랩을 만든다.

## 성공 기준

- Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다.
- TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다.
- audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다.

## 이번 단계에서 다루지 않는 것

- 실제 Google Console 연동
- production-grade TOTP secret 관리
- Redis-backed hard rate limiting enforcement

이 디렉터리는 구현 설명이 아니라 canonical problem statement와 제약 조건을 남기는 곳이다.
