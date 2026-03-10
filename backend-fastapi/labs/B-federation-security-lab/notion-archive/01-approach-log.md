# Approach Log

## 합칠 것인가, 나눌 것인가

가장 먼저 부딪힌 결정은 "A-auth-lab의 로컬 인증과 이 federation을 한 프로젝트에 합칠 것인가?"였다. 합치면 사용자가 비밀번호로도, Google로도 로그인할 수 있어 현실적이다. 하지만 두 인증 경로의 코드가 섞이면 학습 시 각각의 보안 관심사를 분리해서 읽기 어렵다. 결국 분리했다. 이 랩은 비밀번호가 아예 없다. Google OIDC만 유일한 진입 경로이고, 덕분에 서비스 계층에서 password hashing 관련 코드가 전혀 없다.

두 번째 결정은 TOTP 2FA를 이 랩에 포함시킬 것인가였다. 2FA만으로 별도 랩을 만들 수도 있었지만, federation과 session hardening이 같은 맥락에 있어야 "인증이란 단일 이벤트가 아니다"라는 메시지가 선명해진다. Recovery code와 throttling도 같은 이유로 포함시켰다.

## OAuth State와 PKCE: 왜 둘 다 필요한가

Google OIDC 로그인 흐름에서 state와 PKCE는 서로 다른 걸 보호한다. state는 CSRF를 막는다—우리 서버가 시작하지 않은 callback 요청을 걸러낸다. PKCE(code_verifier + code_challenge)는 authorization code 탈취를 막는다—중간에 code를 가로채도 code_verifier 없이는 토큰 교환이 불가능하다.

구현에서는 `sign_oauth_state`로 state, nonce, code_verifier를 하나의 signed cookie에 묶어 저장한다. `itsdangerous.URLSafeSerializer`를 사용하여 secret_key로 서명하기 때문에 클라이언트가 값을 조작할 수 없다. callback에서 이 쿠키를 꺼내 state를 비교하고, code_verifier로 토큰 교환을 수행하고, nonce로 id_token 검증까지 한다. 세 값이 하나의 서명된 번들로 묶여 있다는 것이 핵심이다.

## External Identity Linking

사용자가 Google로 처음 로그인하면 시스템에 User 레코드가 없다. `sync_google_user` 메서드는 이 경우를 순차적으로 처리한다:

1. `external_identities`에서 provider=google, provider_subject=sub 값으로 검색
2. 없으면, email_verified가 true인 경우 같은 이메일의 기존 User를 검색
3. 그래도 없으면 새 User를 생성하고 handle을 이메일 앞부분에서 추출

이후 항상 `link_external_identity`를 호출해서 external_identities 레코드를 생성하거나 갱신한다. 이 설계의 장점은 한 User가 여러 provider를 가질 수 있고(향후 GitHub, Apple 추가 가능), provider별 profile 정보를 JSON 컬럼에 그대로 저장한다는 것이다.

## 2FA의 두 단계: Setup과 Challenge

2FA는 두 가지 시점에서 작동한다. **Setup**은 이미 인증된 사용자가 2FA를 활성화할 때다. `POST /2fa/setup`이 `pending_two_factor_secret`에 pyotp 시크릿을 저장하고, `POST /2fa/confirm`에서 사용자가 TOTP 앱으로 생성한 코드를 보내 검증하면 비로소 `two_factor_enabled = True`로 전환된다. 이때 8개의 recovery code가 생성되어 해시로 DB에 저장된다.

**Challenge**는 2FA가 활성화된 사용자가 Google 로그인을 완료한 뒤의 중간 관문이다. callback에서 `user.two_factor_enabled`가 True이면 access/refresh 토큰 대신 `pending_auth_token`을 발급한다. 이 토큰은 type이 `pending_2fa`이고 TTL이 300초(5분)다. 클라이언트가 `POST /2fa/verify`에 TOTP 코드나 recovery code를 보내면 그때 진짜 세션이 발급된다.

## Rate Limiting

`RateLimiter` 클래스는 Redis가 있으면 Redis INCR+EXPIRE 파이프라인을 사용하고, 없으면 in-memory dict로 fallback한다. 엔드포인트별로 데코레이터 패턴(`Depends(RateLimiter(...))`)으로 적용된다:

- `auth:google-login` → 10회/60초
- `auth:google-callback` → 15회/60초
- `auth:2fa-verify` → 10회/60초
- `auth:refresh` → 20회/60초

IP 기반 제한이라 정교하지는 않지만, brute force의 비용을 높이는 첫 단계로 충분하다.

## Audit Events

모든 인증 관련 상태 변경을 `auth_audit_logs` 테이블에 기록한다. event_type으로 `auth.login.success`, `auth.login.challenge_required`, `auth.2fa.enabled`, `auth.2fa.verified`, `auth.refresh.rotated`, `auth.refresh.reuse_detected`, `auth.logout` 등을 구분하고, IP와 User-Agent를 함께 저장한다. 운영 환경에서 누가, 언제, 어디서 인증했는지 사후 추적할 수 있는 기반이다.

## 기각된 방향

- **live Google 연동을 핵심 요구사항으로**: 학습 저장소가 Google Cloud Console 설정에 의존하면 재현성이 깨진다. mock으로 contract를 검증하는 것이 이 맥락에서는 맞다.
- **2FA를 별도 랩으로 분리**: federation과 session hardening이 조각나면 "인증은 복합 이벤트다"라는 교훈이 약해진다.
- **비밀번호 인증 포함**: 이 랩의 초점은 외부 identity federation이다. 비밀번호를 넣으면 A-auth-lab과 책임이 겹친다.
