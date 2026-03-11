# 문서 묶음 안내

이 문서 묶음은 session cookie, bearer JWT, OAuth/OIDC redirect flow를 같은 “인증”으로 뭉개지 않고,
각 제어가 어떤 공격면을 줄이는지 설명하기 위한 개념 지도입니다.

## 먼저 보면 좋은 질문

- OAuth에서 `state`와 PKCE는 각각 어떤 공격을 막는가
- access token TTL, refresh rotation, reuse detection은 왜 따로 설명해야 하는가
- cookie 기반 상태 변경 요청에서 CSRF는 왜 계속 남는가

## 함께 보면 좋은 문서

1. [concepts/session-jwt-oauth-threats.md](concepts/session-jwt-oauth-threats.md)
2. [references/README.md](references/README.md)
3. [공용 가이드](../../../../../guides/security/auth-threat-modeling.md)

