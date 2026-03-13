# 07 Auth Session JWT — Auth Boundary And Test Closure

`01-backend-core/07-auth-session-jwt`는 session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다. 이 글에서는 9단계: 미들웨어 구현 -> 10단계: main.go 작성 -> 11단계: 실행 및 검증 -> 12단계: docs/ 작성 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 9단계: 미들웨어 구현
- 10단계: main.go 작성
- 11단계: 실행 및 검증
- 12단계: docs/ 작성

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/internal/auth/server.go`
- 처음 가설: 권한 실패와 인증 실패를 응답 코드로 분리해 이후 RBAC 과제로 이어지게 했다.
- 실제 진행: requireSession `r.Cookie("session_token")` → 맵에서 세션 확인 context에 이메일과 역할 저장: `context.WithValue` requireBearer `Authorization: Bearer <token>` 파싱 `.` 기준으로 3-part 분리 HMAC 재계산 후 `hmac.Equal`로 서명 검증 exp 확인: `time.Now().Unix()` > exp이면 401 context에 이메일과 역할 저장 포트 4030 사용. 세션 테스트

CLI:

```bash
go run ./cmd/server

# 세션 로그인
curl -c cookies.txt -X POST http://localhost:4030/login/session \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"swordfish"}'

# 세션으로 /me 접근
curl -b cookies.txt http://localhost:4030/me/session

# 세션으로 /admin 접근
curl -b cookies.txt http://localhost:4030/admin
```

검증 신호:

- - `r.Cookie("session_token")` → 맵에서 세션 확인
- - `Authorization: Bearer <token>` 파싱
- curl -c cookies.txt -X POST http://localhost:4030/login/session \
- curl -b cookies.txt http://localhost:4030/me/session
- curl -b cookies.txt http://localhost:4030/admin

핵심 코드: `solution/go/internal/auth/server.go`

```go
var (
	errUnauthorized = errors.New("unauthorized")
	errForbidden    = errors.New("forbidden")
)

type User struct {
	Email        string
	Role         string
	PasswordHash []byte
}

type Session struct {
	Email     string
	Role      string
	ExpiresAt time.Time
}

type Claims struct {
```

왜 이 코드가 중요했는가:

이 코드는 인증 경계를 말이 아니라 서명 규칙과 상태 전이로 고정한다. access token과 refresh/session 흐름이 실제로 어떻게 분리되는지 보여 주는 기준점이다.

새로 배운 것:

- 세션은 서버가 상태를 들고, JWT는 클라이언트가 서명된 토큰을 들고 온다.

보조 코드: `solution/go/internal/auth/server.go`

```go
var (
	errUnauthorized = errors.New("unauthorized")
	errForbidden    = errors.New("forbidden")
)

type User struct {
	Email        string
	Role         string
	PasswordHash []byte
}

type Session struct {
	Email     string
	Role      string
	ExpiresAt time.Time
}

type Claims struct {
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 인증 경계를 말이 아니라 서명 규칙과 상태 전이로 고정한다. access token과 refresh/session 흐름이 실제로 어떻게 분리되는지 보여 주는 기준점이다.

CLI:

```bash
cd 01-backend-core/07-auth-session-jwt/go
go run ./cmd/server
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 세션 로그인, JWT 로그인, 권한 부족, 만료 토큰, 잘못된 서명을 포함한다.

다음:

- refresh token, persistent session store, logout 흐름은 범위에서 제외했다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/auth/server.go` 같은 결정적인 코드와 `cd 01-backend-core/07-auth-session-jwt/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
