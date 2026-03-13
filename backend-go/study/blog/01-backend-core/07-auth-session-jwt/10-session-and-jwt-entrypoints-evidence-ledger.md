# 07 Auth Session JWT Evidence Ledger

## 10 session-and-jwt-entrypoints

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: Server 구조체 정의 (internal/auth/server.go) -> 5단계: 사용자 초기화 (initUsers) -> 6단계: 라우트 등록 -> 7단계: 세션 로그인 구현 -> 8단계: JWT 로그인 구현
- 당시 목표: cookie session과 bearer JWT를 둘 다 경험해야 한다.
- 변경 단위: `require golang.org/x/crypto v0.48.0`, `METHOD /path`, `crypto/rand`, `Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict`
- 처음 가설: session과 JWT를 같은 프로젝트에 두어 저장 위치와 검증 흐름 차이를 직접 비교하게 했다.
- 실제 조치: `go.work`에 모듈 경로를 추가한다: `go.mod`에 `require golang.org/x/crypto v0.48.0`이 추가된다. 이 프로젝트 유일한 외부 의존성이다. `jwtSecret`: HMAC 서명에 사용할 비밀 키 (32바이트) `users`: 이메일 → user 맵 (하드코딩) `sessions`: 세션 토큰 → session 맵 `mu`: sessions 맵 동시 접근 보호 bcrypt로 비밀번호 해시를 미리 생성:

CLI:

```bash
cd study/01-backend-core/07-auth-session-jwt/go
go mod init book-task-3/07-auth-session-jwt

cd study
# go.work에 ./01-backend-core/07-auth-session-jwt/go 추가
```

- 검증 신호:
- go mod init book-task-3/07-auth-session-jwt
- `Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict`
- JSON 응답으로 `{"token": "..."}`
- 핵심 코드 앵커: `solution/go/internal/auth/server.go`
- 새로 배운 것: authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.
- 다음: 다음 글에서는 `20-auth-boundary-and-test-closure.md`에서 이어지는 경계를 다룬다.
