# 07 Auth Session JWT — Session And Jwt Entrypoints

`01-backend-core/07-auth-session-jwt`는 session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: Server 구조체 정의 (internal/auth/server.go) -> 5단계: 사용자 초기화 (initUsers) -> 6단계: 라우트 등록 -> 7단계: 세션 로그인 구현 -> 8단계: JWT 로그인 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: 외부 의존성 설치
- 3단계: 디렉토리 구조 생성
- 4단계: Server 구조체 정의 (internal/auth/server.go)
- 5단계: 사용자 초기화 (initUsers)
- 6단계: 라우트 등록
- 7단계: 세션 로그인 구현
- 8단계: JWT 로그인 구현

## Day 1
### Session 1

- 당시 목표: cookie session과 bearer JWT를 둘 다 경험해야 한다.
- 변경 단위: `require golang.org/x/crypto v0.48.0`, `METHOD /path`, `crypto/rand`, `Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict`
- 처음 가설: session과 JWT를 같은 프로젝트에 두어 저장 위치와 검증 흐름 차이를 직접 비교하게 했다.
- 실제 진행: `go.work`에 모듈 경로를 추가한다: `go.mod`에 `require golang.org/x/crypto v0.48.0`이 추가된다. 이 프로젝트 유일한 외부 의존성이다. `jwtSecret`: HMAC 서명에 사용할 비밀 키 (32바이트) `users`: 이메일 → user 맵 (하드코딩) `sessions`: 세션 토큰 → session 맵 `mu`: sessions 맵 동시 접근 보호 bcrypt로 비밀번호 해시를 미리 생성:

CLI:

```bash
cd study/01-backend-core/07-auth-session-jwt/go
go mod init book-task-3/07-auth-session-jwt

cd study
# go.work에 ./01-backend-core/07-auth-session-jwt/go 추가
```

검증 신호:

- go mod init book-task-3/07-auth-session-jwt
- `Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict`
- JSON 응답으로 `{"token": "..."}`

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

- authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.

보조 코드: `solution/go/cmd/server/main.go`

```go
func main() {
	server, err := auth.NewServer(nil)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("listening on :4030")
	log.Fatal(http.ListenAndServe(":4030", server.Routes()))
}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

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

- 다음 글에서는 `20-auth-boundary-and-test-closure.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/auth/server.go` 같은 결정적인 코드와 `cd 01-backend-core/07-auth-session-jwt/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
