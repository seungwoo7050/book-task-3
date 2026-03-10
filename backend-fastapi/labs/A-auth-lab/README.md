# A-auth-lab

로컬 계정 인증 흐름을 처음부터 끝까지 작은 범위로 연습하는 랩입니다. 로그인 한 번만 만드는 것이 아니라, 이메일 검증, 비밀번호 재설정, refresh token rotation, cookie + CSRF 조합까지 한 묶음으로 설명할 수 있게 만드는 것이 목적입니다.

## 이 랩에서 배우는 것

- 로컬 회원가입과 로그인 흐름 설계
- Argon2 기반 비밀번호 해시
- 이메일 검증과 비밀번호 재설정 토큰 처리
- access token과 rotating refresh token의 역할 분리
- cookie 인증과 CSRF 검증을 함께 다루는 방법

## 선수 지식

- FastAPI 라우팅과 dependency 기본
- HTTP cookie와 bearer token의 차이
- 관계형 데이터베이스와 Redis의 기본 개념

## 구현 범위

- 회원가입, 로그인, 로그아웃
- 이메일 검증
- 비밀번호 재설정
- refresh token rotation
- health endpoint

## 일부러 단순화한 점

- 메일 전송은 실 SMTP 대신 Mailpit 중심 로컬 흐름으로 제한합니다.
- 테스트는 빠른 피드백을 위해 더 가벼운 경로를 우선합니다.
- OAuth와 2FA는 다음 랩인 [B-federation-security-lab](../B-federation-security-lab/README.md)로 넘깁니다.

## 실행 방법

1. [problem/README.md](problem/README.md)로 문제 정의를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)를 따라 워크스페이스를 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 설계 의도와 학습 노트를 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 문제 정의를 읽고 인증 범위를 좁힙니다.
2. FastAPI 워크스페이스를 실행해 인증 흐름을 확인합니다.
3. 문서와 노트에서 토큰 수명, 쿠키, CSRF의 역할을 정리합니다.

## 포트폴리오로 확장하려면

- 이메일 템플릿과 실패 재전송 전략을 별도 모듈로 분리해 볼 수 있습니다.
- 로그인 감사 로그나 디바이스별 세션 관리로 확장할 수 있습니다.
- 실서비스형 포트폴리오에서는 이메일 공급자, rate limiting, 관리자용 계정 복구 흐름까지 연결해 설명하면 좋습니다.
