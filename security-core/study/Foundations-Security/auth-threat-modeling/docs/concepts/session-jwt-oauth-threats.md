# session, JWT, OAuth threat modeling

## 1. Cookie session과 JWT는 공격면이 다르다

- cookie session은 브라우저가 자동 전송하므로 CSRF 방어가 중요합니다.
- bearer JWT는 보통 수동으로 넣기 때문에 CSRF는 줄어들지만, 저장 위치와 검증 누락이 더 중요해집니다.

## 2. OAuth redirect flow는 `state`와 PKCE가 핵심이다

- `state`는 브라우저 기반 redirect에서 request/response를 묶어 CSRF와 mix-up 성격의 혼선을 줄입니다.
- PKCE는 authorization code 탈취 후 재사용을 어렵게 만듭니다.

## 3. JWT validation은 “서명만 보면 끝”이 아니다

issuer, audience, allowed algorithm을 함께 묶어야 토큰을 엉뚱한 용도로 받아들이지 않습니다. 이 프로젝트는 `exp` 자체를
별도 필드로 모델링하지는 않지만, access token TTL을 과도하게 길게 잡은 경우를 별도 finding으로 다룹니다.

## 4. refresh rotation과 reuse detection은 다른 통제다

rotation은 새 refresh token을 발급하는 동작이고, reuse detection은 탈취된 이전 토큰이 다시 쓰였을 때 이를 이상 징후로
판단하는 정책입니다. 둘 중 하나만 있으면 설명이 반쪽짜리가 됩니다.

