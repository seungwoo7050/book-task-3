# 07 Auth Session JWT Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/internal/auth/server.go`, `solution/go/internal/auth/server_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./internal/auth`, `cd solution/go && go test -run TestExpiredToken -v ./internal/auth`
- 핵심 개념 축: `authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.`, `세션은 서버가 상태를 들고, JWT는 클라이언트가 서명된 토큰을 들고 온다.`, `비밀번호는 평문 저장이 아니라 bcrypt 같은 느린 해시가 기본이다.`, 401`은 인증 실패, `403`은 인증은 되었지만 권한 부족일 때가 자연스럽다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - Claims와 Session을 나눠 auth 상태 모델을 먼저 세운다

        - 당시 목표: Claims와 Session을 나눠 auth 상태 모델을 먼저 세운다
        - 변경 단위: `solution/go/internal/auth/server.go`의 `Claims`
        - 처음 가설: `Claims` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
        - 실제 조치: `solution/go/internal/auth/server.go`의 `Claims`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
        - CLI: `cd solution/go && go test -v ./internal/auth`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestSessionLoginAndProtectedResource`였다.
        - 핵심 코드 앵커:
        - `Claims`: `solution/go/internal/auth/server.go`

        ```go
        type Claims struct {
	Sub  string `json:"sub"`
	Role string `json:"role"`
	Exp  int64  `json:"exp"`
}

type Server struct {
	mu       sync.Mutex
	now      func() time.Time
        ```

        - 새로 배운 것: authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.
        - 다음: loginSession, loginJWT와 protected route로 두 인증 경로를 연결한다
        ### 2. Phase 2 - loginSession, loginJWT와 protected route로 두 인증 경로를 연결한다

        - 당시 목표: loginSession, loginJWT와 protected route로 두 인증 경로를 연결한다
        - 변경 단위: `solution/go/internal/auth/server.go`의 `loginJWT`
        - 처음 가설: `loginJWT`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
        - 실제 조치: `solution/go/internal/auth/server.go`의 `loginJWT`를 통해 transport, validation, auth or cache surface를 노출했다.
        - CLI: `cd solution/go && go test -run TestExpiredToken -v ./internal/auth`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestExpiredToken`였다.
        - 핵심 코드 앵커:
        - `loginJWT`: `solution/go/internal/auth/server.go`

        ```go
        func (s *Server) loginJWT(w http.ResponseWriter, r *http.Request) {
	user, err := s.authenticateCredentials(r)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "invalid credentials")
		return
	}

	token, err := s.signClaims(Claims{
		Sub:  user.Email,
        ```

        - 새로 배운 것: JWT는 stateless라 편하지만 만료, revoke, 서명키 관리가 추가된다.
        - 다음: server_test로 role, expiry, signature 검증을 잠근다
        ### 3. Phase 3 - server_test로 role, expiry, signature 검증을 잠근다

        - 당시 목표: server_test로 role, expiry, signature 검증을 잠근다
        - 변경 단위: `solution/go/internal/auth/server_test.go`의 `TestJWTProtectedResource`
        - 처음 가설: `TestJWTProtectedResource` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
        - 실제 조치: `solution/go/internal/auth/server_test.go`의 `TestJWTProtectedResource`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
        - CLI: `cd solution/go && go test -run TestExpiredToken -v ./internal/auth`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestExpiredToken`였다.
        - 핵심 코드 앵커:
        - `TestJWTProtectedResource`: `solution/go/internal/auth/server_test.go`

        ```go
        func TestJWTProtectedResource(t *testing.T) {
	t.Parallel()

	server := newTestServer(t)
	loginReq := httptest.NewRequest(http.MethodPost, "/login/jwt", bytes.NewBufferString(`{"email":"player@example.com","password":"adventurer"}`))
	loginRR := httptest.NewRecorder()
	server.Routes().ServeHTTP(loginRR, loginReq)

	if loginRR.Code != http.StatusOK {
        ```

        - 새로 배운 것: 테스트에서 실제 bcrypt 해시를 쓰면 속도는 느려지지만 현실성은 높아진다. 작은 예제에서는 받아들일 만한 비용이다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/07-auth-session-jwt && cd solution/go && go test -v ./internal/auth)
```

```text
=== RUN   TestSessionLoginAndProtectedResource
=== PAUSE TestSessionLoginAndProtectedResource
=== RUN   TestJWTProtectedResource
=== PAUSE TestJWTProtectedResource
=== RUN   TestForbiddenRole
=== PAUSE TestForbiddenRole
=== RUN   TestExpiredToken
=== PAUSE TestExpiredToken
=== RUN   TestInvalidSignature
=== PAUSE TestInvalidSignature
=== CONT  TestSessionLoginAndProtectedResource
=== CONT  TestExpiredToken
=== CONT  TestForbiddenRole
=== CONT  TestJWTProtectedResource
=== CONT  TestInvalidSignature
--- PASS: TestForbiddenRole (0.17s)
--- PASS: TestExpiredToken (0.17s)
--- PASS: TestSessionLoginAndProtectedResource (0.23s)
--- PASS: TestJWTProtectedResource (0.24s)
--- PASS: TestInvalidSignature (0.29s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/07-auth-session-jwt/internal/auth	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/07-auth-session-jwt && cd solution/go && go test -run TestExpiredToken -v ./internal/auth)
```

```text
=== RUN   TestExpiredToken
=== PAUSE TestExpiredToken
=== CONT  TestExpiredToken
--- PASS: TestExpiredToken (0.15s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/07-auth-session-jwt/internal/auth	(cached)
```
