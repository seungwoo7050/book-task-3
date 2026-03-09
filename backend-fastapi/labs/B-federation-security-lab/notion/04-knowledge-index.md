# Knowledge Index

## OIDC: OAuth 위의 Identity 계층

OAuth 2.0은 "이 사용자가 자신의 데이터 접근을 허가했다"는 위임(delegation) 프로토콜이다. 하지만 "이 사용자가 누구인가"는 OAuth만으로 표준화되어 있지 않다. OIDC(OpenID Connect)가 그 위에 id_token이라는 표준 방식을 얹었다. id_token은 JWT 형태이고, `sub`(사용자 고유 식별자), `email`, `name` 등의 claim을 포함한다.

이 랩에서 OIDC 흐름은 다음과 같다:
1. 서버가 Google authorization endpoint로 리다이렉트 URL을 생성 (state, nonce, PKCE code_challenge 포함)
2. 사용자가 Google에서 인증 후, authorization code와 함께 callback URL로 돌아옴
3. 서버가 code + code_verifier로 Google token endpoint에서 access_token과 id_token을 교환
4. id_token을 Google의 JWKS(JSON Web Key Set)로 서명 검증하고 nonce를 확인
5. userinfo endpoint에서 추가 프로필 정보(avatar 등) 획득

## PKCE (Proof Key for Code Exchange)

PKCE는 authorization code가 중간에 탈취되더라도 토큰 교환에 사용하지 못하게 하는 방어 메커니즘이다. 흐름은 이렇다:

1. 서버가 random `code_verifier`를 생성 (`secrets.token_urlsafe(64)`)
2. 그 verifier의 SHA-256 해시를 base64url로 인코딩한 것이 `code_challenge`
3. authorization 요청에 code_challenge를 포함
4. token 교환 요청에 원본 code_verifier를 포함
5. Google이 code_verifier를 해시해서 처음 보낸 code_challenge와 비교

이 랩에서는 `generate_pkce_verifier()`와 `build_pkce_challenge()` 두 함수로 구현했다. code_verifier는 signed OAuth state cookie에 저장되므로 브라우저에서 직접 접근할 수 없다.

## itsdangerous를 이용한 서명된 쿠키

OAuth state를 전달하는 방법으로 서버 세션이나 DB 저장 대신 **서명된 쿠키**를 선택했다. `itsdangerous.URLSafeSerializer`가 `secret_key`와 `salt`를 사용해 payload를 서명하고, 나중에 같은 키로 복원한다. 서명이 변조되면 `BadSignature` 예외가 발생한다.

이 방식의 장점은 서버에 상태를 저장하지 않아도 된다는 것이다. state, nonce, code_verifier가 하나의 쿠키 값에 담기고, callback에서 그 쿠키를 꺼내 검증하면 끝이다. 단점은 쿠키 크기 제한(약 4KB)이 있고, secret_key 유출 시 모든 서명이 무효화된다는 것이다.

## TOTP (Time-based One-Time Password)

TOTP는 shared secret과 현재 시각을 입력으로 6자리 코드를 생성하는 알고리즘이다(RFC 6238). 서버와 클라이언트(Google Authenticator 등)가 같은 secret을 갖고 있으면, 같은 시각에 같은 코드를 생성할 수 있다.

이 랩에서 `pyotp` 라이브러리가 이를 처리한다:
- `pyotp.random_base32()`: 32자리 base32 secret 생성
- `pyotp.TOTP(secret).provisioning_uri(email, issuer_name=...)`: QR 코드용 URI 생성
- `pyotp.TOTP(secret).verify(code, valid_window=1)`: 현재 시각 ±1 window에서 코드 검증

`valid_window=1`은 시계 오차 허용이다. 30초 단위 코드에서 앞뒤 30초를 더 허용한다. 이 값이 너무 크면 보안이 약해지고, 0이면 사소한 시계 차이에 실패한다.

## Recovery Code 설계

TOTP 앱을 잃어버렸을 때의 비상 수단이다. 이 랩에서는 8개의 `XXXX-XXXX` 형태 코드를 생성하고, HMAC-SHA256 해시로 DB에 저장한다. 원본은 생성 시 한 번만 사용자에게 반환되고, 서버는 해시만 보관한다.

recovery code로 2FA를 통과하면 해당 코드의 `used_at`이 기록되어 재사용이 불가능해진다. 코드를 재생성하려면 먼저 현재 TOTP 코드나 남은 recovery code로 인증해야 한다—이것은 recovery code 탈취만으로 2FA를 무력화할 수 없게 하는 설계다.

## Refresh Token Family와 Reuse Detection

A-auth-lab에서도 다뤘지만 이 랩에서 더 명확해지는 개념이다. family_id로 하나의 로그인 세션에서 파생된 모든 refresh token을 묶는다. 정상 흐름에서는 토큰을 rotate할 때마다 이전 토큰을 revoke하고 새 토큰에 같은 family_id를 부여한다.

만약 이미 revoke된 토큰이 다시 사용되면(`revoked_at is not None`), **reuse detection**이 작동한다. 해당 family의 모든 토큰이 일괄 revoke되고, `auth.refresh.reuse_detected` 감사 이벤트가 기록된다. 이는 토큰이 탈취되었을 가능성을 의미하므로, 가장 안전한 대응은 해당 세션 family 전체를 무효화하는 것이다.

## Rate Limiting: Redis vs In-Memory Fallback

이 랩의 `RateLimiter`는 두 가지 백엔드를 지원한다. Redis가 있으면 `INCR` + `EXPIRE` 파이프라인으로 atomic한 카운팅을 하고, 없으면 `threading.Lock`으로 보호되는 dict를 사용한다.

Redis 방식의 장점은 여러 서버 인스턴스 간에 카운트를 공유할 수 있다는 것이다. In-memory 방식은 단일 프로세스 테스트에서만 유효하고, 서버 재시작 시 카운트가 리셋된다. 이 랩에서 in-memory fallback이 존재하는 이유는 테스트 환경에서 Redis 없이도 동작하게 하기 위함이다.
