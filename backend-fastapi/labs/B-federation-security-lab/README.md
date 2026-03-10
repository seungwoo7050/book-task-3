# B-federation-security-lab

로컬 인증 이후에 붙는 보안 강화 흐름을 따로 떼어 연습하는 랩입니다. 외부 로그인, 2단계 인증, 회복 코드, 감사 로그를 하나의 보안 랩으로 묶어 "계정 진입 경로를 어떻게 단단하게 만들 것인가"에 집중합니다.

## 이 랩에서 배우는 것

- Google OIDC 로그인 흐름
- 외부 계정과 내부 사용자 계정 연결
- TOTP 기반 2단계 인증
- recovery code 발급과 재생성
- 로그인 throttling과 auth audit log

## 선수 지식

- [A-auth-lab](../A-auth-lab/README.md) 수준의 로컬 인증 개념
- OAuth 2.0 / OIDC 용어
- 세션과 토큰 수명 관리 기본

## 구현 범위

- Google 스타일 authorization-code 로그인
- provider-linked identity 관리
- TOTP 등록과 검증
- recovery code rotation
- 로그인 보안 이벤트 기록

## 일부러 단순화한 점

- 테스트는 실제 Google 서비스가 아니라 mock 경로를 사용합니다.
- 제품 도메인 로직은 넣지 않고 인증 보안 흐름만 분리합니다.

## 실행 방법

1. [problem/README.md](problem/README.md)로 이 랩의 보안 범위를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 Alembic 적용까지 포함된 실행 경로를 확인합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 보안 강화 포인트를 복기합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 로컬 인증과 외부 인증의 경계를 먼저 정리합니다.
2. 2FA와 recovery code가 세션 흐름에 어떻게 끼어드는지 확인합니다.
3. throttling과 audit log가 보안 설명에서 왜 중요한지 문서로 정리합니다.

## 포트폴리오로 확장하려면

- 여러 소셜 로그인 공급자를 한 모델로 통합해 볼 수 있습니다.
- risk-based auth, device trust, 관리자 보안 감사 화면으로 확장할 수 있습니다.
- 보안 포트폴리오에서는 "무엇을 막는 설계인지"를 기능 목록보다 먼저 설명하는 편이 좋습니다.
