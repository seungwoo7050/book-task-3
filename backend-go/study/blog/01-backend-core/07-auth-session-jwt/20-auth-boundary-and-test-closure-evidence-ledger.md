# 07 Auth Session JWT Evidence Ledger

## 20 auth-boundary-and-test-closure

- 시간 표지: 9단계: 미들웨어 구현 -> 10단계: main.go 작성 -> 11단계: 실행 및 검증 -> 12단계: docs/ 작성
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/internal/auth/server.go`
- 처음 가설: 권한 실패와 인증 실패를 응답 코드로 분리해 이후 RBAC 과제로 이어지게 했다.
- 실제 조치: requireSession `r.Cookie("session_token")` → 맵에서 세션 확인 context에 이메일과 역할 저장: `context.WithValue` requireBearer `Authorization: Bearer <token>` 파싱 `.` 기준으로 3-part 분리 HMAC 재계산 후 `hmac.Equal`로 서명 검증 exp 확인: `time.Now().Unix()` > exp이면 401 context에 이메일과 역할 저장 포트 4030 사용. 세션 테스트

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

- 검증 신호:
- - `r.Cookie("session_token")` → 맵에서 세션 확인
- - `Authorization: Bearer <token>` 파싱
- curl -c cookies.txt -X POST http://localhost:4030/login/session \
- curl -b cookies.txt http://localhost:4030/me/session
- curl -b cookies.txt http://localhost:4030/admin
- 핵심 코드 앵커: `solution/go/internal/auth/server.go`
- 새로 배운 것: 세션은 서버가 상태를 들고, JWT는 클라이언트가 서명된 토큰을 들고 온다.
- 다음: refresh token, persistent session store, logout 흐름은 범위에서 제외했다.
