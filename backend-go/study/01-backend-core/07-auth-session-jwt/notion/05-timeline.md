# 타임라인 — 인증 서버 개발 전체 과정

## 1단계: 프로젝트 초기화

```bash
cd study/01-backend-core/07-auth-session-jwt/go
go mod init book-task-3/07-auth-session-jwt
```

`go.work`에 모듈 경로를 추가한다:

```bash
cd study
# go.work에 ./01-backend-core/07-auth-session-jwt/go 추가
```

## 2단계: 외부 의존성 설치

```bash
cd study/01-backend-core/07-auth-session-jwt/go
go get golang.org/x/crypto
```

`go.mod`에 `require golang.org/x/crypto v0.48.0`이 추가된다. 이 프로젝트 유일한 외부 의존성이다.

## 3단계: 디렉토리 구조 생성

```bash
mkdir -p internal/auth
mkdir -p cmd/server
```

```
go/
├── go.mod
├── cmd/
│   └── server/
│       └── main.go
└── internal/
    └── auth/
        └── server.go
```

## 4단계: Server 구조체 정의 (internal/auth/server.go)

```go
type Server struct {
    jwtSecret []byte
    users     map[string]user
    sessions  map[string]session
    mu        sync.Mutex
}
```

- `jwtSecret`: HMAC 서명에 사용할 비밀 키 (32바이트)
- `users`: 이메일 → user 맵 (하드코딩)
- `sessions`: 세션 토큰 → session 맵
- `mu`: sessions 맵 동시 접근 보호

## 5단계: 사용자 초기화 (initUsers)

bcrypt로 비밀번호 해시를 미리 생성:

```go
hash, _ := bcrypt.GenerateFromPassword([]byte("swordfish"), bcrypt.DefaultCost)
```

두 사용자: `admin@example.com` (admin 역할), `player@example.com` (player 역할).

## 6단계: 라우트 등록

```go
mux.HandleFunc("POST /login/session", s.handleSessionLogin)
mux.HandleFunc("POST /login/jwt", s.handleJWTLogin)
mux.HandleFunc("GET /me/session", s.requireSession(s.handleSessionMe))
mux.HandleFunc("GET /me/jwt", s.requireBearer(s.handleJWTMe))
mux.HandleFunc("GET /admin", s.requireAnyAuth(s.requireRole("admin", s.handleAdmin)))
```

Go 1.22의 `METHOD /path` 라우팅 사용.

## 7단계: 세션 로그인 구현

`handleSessionLogin`에서:
1. JSON 요청 디코딩 (email, password)
2. `bcrypt.CompareHashAndPassword`로 비밀번호 검증
3. `crypto/rand`로 16바이트 토큰 생성, hex 인코딩
4. `s.mu.Lock()` → sessions 맵에 저장 → `s.mu.Unlock()`
5. `Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict`

## 8단계: JWT 로그인 구현

`handleJWTLogin`에서:
1. 비밀번호 검증 (세션과 동일)
2. Claims 구성: `sub`, `role`, `exp` (1시간 후)
3. Header JSON: `{"alg":"HS256","typ":"JWT"}`
4. base64url(header) + "." + base64url(payload)
5. HMAC-SHA256(signingInput, jwtSecret)
6. 최종 토큰: signingInput + "." + base64url(signature)
7. JSON 응답으로 `{"token": "..."}`

## 9단계: 미들웨어 구현

### requireSession
- `r.Cookie("session_token")` → 맵에서 세션 확인
- context에 이메일과 역할 저장: `context.WithValue`

### requireBearer
- `Authorization: Bearer <token>` 파싱
- `.` 기준으로 3-part 분리
- HMAC 재계산 후 `hmac.Equal`로 서명 검증
- exp 확인: `time.Now().Unix()` > exp이면 401
- context에 이메일과 역할 저장

### requireAnyAuth
- JWT 검증 먼저 시도 → 실패 시 세션 시도
- 둘 다 실패하면 401

### requireRole
- context에서 역할 추출
- 기대 역할과 불일치하면 403

## 10단계: main.go 작성

```go
srv := auth.NewServer()
log.Println("listening on :4030")
log.Fatal(http.ListenAndServe(":4030", srv))
```

포트 4030 사용.

## 11단계: 실행 및 검증

```bash
go run ./cmd/server
```

### 세션 테스트

```bash
# 세션 로그인
curl -c cookies.txt -X POST http://localhost:4030/login/session \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"swordfish"}'

# 세션으로 /me 접근
curl -b cookies.txt http://localhost:4030/me/session

# 세션으로 /admin 접근
curl -b cookies.txt http://localhost:4030/admin
```

### JWT 테스트

```bash
# JWT 토큰 발급
TOKEN=$(curl -s -X POST http://localhost:4030/login/jwt \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"swordfish"}' | jq -r '.token')

# JWT로 /me 접근
curl -H "Authorization: Bearer $TOKEN" http://localhost:4030/me/jwt

# JWT로 /admin 접근
curl -H "Authorization: Bearer $TOKEN" http://localhost:4030/admin
```

### 권한 부족 테스트 (403)

```bash
# player 계정으로 JWT 발급
PLAYER_TOKEN=$(curl -s -X POST http://localhost:4030/login/jwt \
  -H "Content-Type: application/json" \
  -d '{"email":"player@example.com","password":"adventurer"}' | jq -r '.token')

# player가 /admin 접근 → 403
curl -H "Authorization: Bearer $PLAYER_TOKEN" http://localhost:4030/admin
```

### 비밀번호 오류 테스트 (401)

```bash
curl -X POST http://localhost:4030/login/session \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"wrongpass"}'
```

## 12단계: docs/ 작성

```bash
# docs/ 디렉토리에 개념 설명과 검증 기준 문서 작성
vim docs/concepts/core-concepts.md
vim docs/verification.md
```

## 파일 목록

| 순서 | 파일 | 설명 |
|------|------|------|
| 1 | `go.mod` | 모듈 정의, golang.org/x/crypto 의존성 |
| 2 | `internal/auth/server.go` | Server 구조체, 라우트, 핸들러, 미들웨어, JWT 서명 |
| 3 | `cmd/server/main.go` | 엔트리포인트, :4030 |
| 4 | `docs/concepts/core-concepts.md` | 인증/인가 개념 설명 |
| 5 | `docs/verification.md` | 검증 기준 |
