# 접근 과정 — 인증 서버를 세우기까지

## bcrypt로 비밀번호 해싱

비밀번호를 그대로 저장하면 DB가 유출될 때 모든 계정이 노출된다. bcrypt는 의도적으로 느린 해시 알고리즘으로, brute-force 공격을 어렵게 만든다.

```go
hash, _ := bcrypt.GenerateFromPassword([]byte("swordfish"), bcrypt.DefaultCost)
bcrypt.CompareHashAndPassword(hash, []byte("swordfish"))
```

`golang.org/x/crypto/bcrypt` 패키지를 사용했다. 표준 라이브러리는 아니지만 Go 공식 조직에서 관리하는 준표준 패키지다. `go get golang.org/x/crypto`로 설치.

## 세션 — 서버가 상태를 들고 있는 방식

로그인 성공 시 `crypto/rand`로 16바이트 랜덤 토큰을 생성하고, 서버의 맵에 세션을 저장한다. 토큰은 `HttpOnly` 쿠키로 클라이언트에 전달한다.

```
클라이언트 → POST /login/session (email, password)
서버 → 비밀번호 검증 → 세션 생성 → Set-Cookie: session_token=...
클라이언트 → GET /me/session (Cookie: session_token=...)
서버 → 세션 맵에서 확인 → 사용자 정보 반환
```

`HttpOnly` 플래그는 JavaScript에서 쿠키에 접근하지 못하게 막는다. XSS 공격을 방어하는 기본 조치다.

## JWT — 클라이언트가 토큰을 들고 다니는 방식

로그인 성공 시 Claims(sub, role, exp)를 JSON으로 만들고, HMAC-SHA256으로 서명한 뒤 base64url로 인코딩한다.

```
header.payload.signature
```

세 부분을 `.`으로 이어 붙인 게 JWT다. 서버는 토큰을 저장하지 않는다. 대신 매 요청에서 서명을 검증하고, 만료 시간을 확인한다.

직접 HMAC-SHA256으로 JWT를 구현했다. `github.com/golang-jwt/jwt` 같은 라이브러리를 쓸 수도 있었지만, JWT의 구조를 체감하려면 직접 만들어 봐야 한다는 판단이었다.

## 미들웨어로 인증 분리

세 가지 인증 미들웨어를 만들었다:
1. **`requireSession`**: 쿠키에서 세션 토큰 검증
2. **`requireBearer`**: Authorization 헤더에서 JWT 검증
3. **`requireAnyAuth`**: JWT 먼저 시도, 실패하면 세션 시도

인가(역할 검사)는 `requireRole`로 별도 분리했다. 인증과 인가를 한 함수에 섞지 않은 건 의도적이다. 그래야 "인증은 됐지만 권한이 없다"(403)와 "인증 자체가 안 됐다"(401)를 깔끔하게 구분할 수 있다.

## 401 vs 403 설계

| 상황 | 코드 |
|------|------|
| 쿠키/토큰 없음 | 401 |
| 토큰이 만료됨 | 401 |
| 비밀번호 틀림 | 401 |
| 인증은 되었으나 admin이 아님 | 403 |

`requireAnyAuth → requireRole` 체인이 이 흐름을 자연스럽게 구현한다.
