# 문제 프레이밍

## 학습 목표

외부 로그인과 2단계 인증을 한 랩 안에서 다루며, "로그인 성공"이 단일 이벤트가 아니라 여러 보안 조건의 결합이라는 점을 이해하는 것이 목표다.

## 왜 중요한가

- 로컬 인증만으로는 외부 공급자 연동과 보안 강화 흐름을 설명하기 어렵다.
- provider identity와 내부 user identity를 어떻게 연결하는지가 실서비스에서 자주 문제가 된다.

## 선수 지식

- 로컬 인증과 세션 발급 개념
- OAuth 2.0 / OIDC 용어
- TOTP와 recovery code가 왜 필요한지에 대한 기본 이해

## 성공 기준

- Google 스타일 로그인 진입과 callback 경로가 설명 가능해야 한다.
- 2FA 활성 사용자에게 pending auth 같은 중간 상태를 둘 수 있어야 한다.
- recovery code, throttling, audit log가 최소 수준으로라도 동작해야 한다.

## 제외 범위

- live Google provider와의 end-to-end 검증
- 제품 도메인별 권한 문제
- 다중 공급자 추상화 완성

이 랩의 핵심은 provider 연동 자체보다, 외부에서 받은 신뢰를 내부 세션 모델로 어떻게 옮길지 설명하는 데 있다.
