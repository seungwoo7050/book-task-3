# 지식 색인 — 인증 관련 개념 정리

## bcrypt

비밀번호 해싱에 특화된 알고리즘. SHA-256과 달리 의도적으로 느리게 설계됐다. cost 파라미터로 연산 횟수를 조절할 수 있어, 하드웨어가 빨라져도 cost를 올려 brute-force를 방어한다. `bcrypt.DefaultCost`는 10이다.

## 세션(Session)

서버가 사용자 상태를 메모리(또는 외부 저장소)에 보관하는 인증 방식. 클라이언트에는 세션 ID만 쿠키로 전달한다. 장점은 서버가 세션을 즉시 무효화할 수 있다는 것. 단점은 서버가 상태를 유지해야 하므로 수평 확장이 어렵다.

## JWT (JSON Web Token)

`header.payload.signature` 세 부분으로 구성된 자가 포함(self-contained) 토큰. 서버가 상태를 저장하지 않는다(stateless). Claims에 사용자 정보가 들어 있어 DB 조회 없이 인증/인가를 처리할 수 있다.

- **Header**: 알고리즘, 토큰 타입 (HS256, JWT)
- **Payload**: Claims — sub(주체), role, exp(만료), iat(발행) 등
- **Signature**: HMAC(header.payload, secret)

## HMAC-SHA256

해시 기반 메시지 인증 코드. 비밀 키와 메시지를 결합해 해시를 생성한다. 키 없이는 동일한 해시를 만들 수 없으므로, JWT의 무결성과 출처를 보장한다.

## 상수 시간 비교 (Constant-Time Comparison)

`hmac.Equal`은 두 바이트 슬라이스를 비교할 때, 첫 바이트가 달라도 모든 바이트를 검사한다. 이를 통해 타이밍 공격을 방지한다. 일반 `==` 연산자는 첫 불일치에서 즉시 반환하므로, 응답 시간 차이로 정보가 유출될 수 있다.

## HttpOnly 쿠키

JavaScript의 `document.cookie`로 접근할 수 없는 쿠키. XSS 공격으로 토큰을 탈취하는 것을 방지한다. `http.Cookie{HttpOnly: true}`로 설정.

## 인증(Authentication) vs 인가(Authorization)

| | 인증 | 인가 |
|---|------|------|
| 질문 | "너 누구야?" | "이 자원에 접근할 수 있어?" |
| 실패 코드 | 401 Unauthorized | 403 Forbidden |
| 이 프로젝트 | `requireAnyAuth` | `requireRole` |

## base64url

표준 base64에서 `+` → `-`, `/` → `_`로 바꾸고 패딩(`=`)을 제거한 인코딩. URL에서 안전하게 사용할 수 있다. JWT의 header와 payload가 이 방식으로 인코딩된다.

## crypto/rand vs math/rand

`crypto/rand`는 운영체제의 엔트로피 소스에서 암호학적으로 안전한 난수를 생성한다. `math/rand`는 의사 난수(pseudorandom)로, 시드를 알면 전체 시퀀스를 예측할 수 있다. 세션 토큰은 반드시 `crypto/rand`를 사용해야 한다.

## 미들웨어 체인

```
requireAnyAuth(requireRole("admin", handler))
```

바깥 미들웨어(`requireAnyAuth`)가 먼저 실행되고, 통과하면 안쪽 미들웨어(`requireRole`)가 실행된다. 인증 실패 시 401, 인가 실패 시 403을 반환하며 내부 핸들러는 호출되지 않는다.

## golang.org/x/crypto

Go 공식 확장 라이브러리. 표준 라이브러리(`crypto/`)에 포함되지 않은 암호화 기능을 제공한다. bcrypt, argon2, ssh, acme 등을 포함한다. `go get golang.org/x/crypto`로 설치하며, Go 팀이 직접 유지보수한다.
