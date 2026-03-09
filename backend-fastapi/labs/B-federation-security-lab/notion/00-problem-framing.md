# Problem Framing

## "로그인 성공"이란, 정확히 무엇인가

A-auth-lab에서는 비밀번호 하나로 로그인이 끝났다. 이메일과 패스워드를 보내면 서버가 토큰을 주고, 그것으로 이야기가 완결된다. 하지만 실제 서비스에서는 이 일직선 모델이 금세 깨진다. 사용자가 Google로 로그인하면 비밀번호는 없고 외부 provider의 증명만 있다. 그때 "이 사람이 우리 시스템의 누구인가?"를 내부 ID로 연결하는 설계가 필요해진다.

이 랩은 바로 그 지점에서 시작한다. Google OIDC로 외부 identity를 받아들이되, 내부 사용자 모델과 분리된 `external_identities` 테이블로 연결하는 federation 설계. 거기에 TOTP 기반 2차 인증을 얹어서 "로그인 성공"이 단일 이벤트가 아니라 여러 보안 조건의 결합임을 코드로 증명하는 것이 목표다.

## 풀어야 할 문제의 경계

핵심 질문은 세 가지다.

첫째, Google이 "이 사람은 pong@example.com이다"라고 말했을 때, 우리 시스템은 그 주장을 어떻게 내부 User 레코드와 매핑하는가? provider_subject와 email 기반 linking이 동시에 작동해야 하고, 같은 이메일로 다른 provider에서 들어올 가능성도 고려해야 한다.

둘째, OIDC callback이 끝난 뒤에도 2FA가 활성화된 사용자라면 세션을 아직 발급하면 안 된다. 중간 상태인 "pending_2fa" 토큰을 만들고, TOTP 검증이 끝나야 진짜 access/refresh 토큰을 내려줘야 한다. 이 중간 상태를 어떻게 설계할 것인가?

셋째, recovery code, rate limiting, audit log를 어디까지 넣어야 학습 가치가 있고, 과도한 복잡성은 피할 수 있는가?

## 제약 조건

이 랩에서 가장 큰 제약은 **Google provider를 실제로 호출하지 않는다**는 점이다. 모든 테스트는 `GoogleOIDCService`의 메서드를 monkeypatch로 대체한다. `exchange_code_for_tokens`, `validate_id_token`, `fetch_userinfo` 세 메서드 모두 가짜 응답을 돌려준다. 이 결정은 학습 저장소가 Google Cloud Console 설정 오류에 의존하지 않게 하기 위한 것이다.

프레임워크는 FastAPI, DB는 PostgreSQL 16, 세션 throttling용으로 Redis 7이 추가된다. A-auth-lab과 달리 로컬 비밀번호 인증은 없다—오직 Google OIDC만 로그인 경로로 존재한다.

## 성공 기준

- `GET /api/v1/auth/google/login` → authorization URL 반환, OAuth state 쿠키 설정
- `GET /api/v1/auth/google/callback` → 사용자 생성/업데이트, 세션 발급 (2FA 미활성 시)
- 2FA 활성 사용자 → callback에서 `requires_2fa` 상태 반환, pending_auth 토큰 발급
- `POST /api/v1/auth/2fa/verify` → TOTP 코드 또는 recovery code로 최종 인증
- rate limiter가 과도한 요청을 429로 차단
- audit log가 login, 2fa.enabled, 2fa.verified, refresh.reuse_detected 등의 이벤트를 기록
- `make test`, `make lint`, `make smoke`, Docker Compose probe 통과

## 불확실성

live Google provider와의 실제 edge case(토큰 만료, consent 화면 거부, 이메일 미인증 계정)는 이 랩에서 검증하지 않는다. mock이 커버하지 못하는 영역이 있다는 것을 인정하되, 이 랩의 핵심은 provider 콘솔 연동이 아니라 **internal identity linking과 multi-step auth flow의 설계**라고 판단했다.
