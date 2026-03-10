# 회고

## 이번 랩에서 얻은 것

외부 로그인, 2FA, recovery code를 "보안 강화 흐름"이라는 하나의 묶음으로 설명할 수 있게 되었다. 특히 pending auth 같은 중간 상태를 도입한 점이 단순 로그인 예제와 차별화된다.

## 아직 약한 부분

- live provider와의 실제 edge case는 검증하지 못했다.
- rate limiter와 audit log는 최소 구현 수준이라 운영 관점의 깊이는 아직 얕다.

## 다시 보면 좋을 주제

- multi-provider 계정 연결 정책
- risk-based auth
- refresh token reuse detection 고도화

## 포트폴리오 확장 아이디어

- GitHub, Apple 같은 추가 공급자를 붙여 비교 실험을 해 본다.
- 보안 이벤트 대시보드와 관리자용 감사 화면을 추가한다.
