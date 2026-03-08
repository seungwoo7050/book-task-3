# Verification

## Commands

```bash
cd 01-backend-core/07-auth-session-jwt/go
go run ./cmd/server
go test ./...
```

## Result

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 세션 로그인, JWT 로그인, 권한 부족, 만료 토큰, 잘못된 서명을 포함한다.

## Remaining Checks

- refresh token, persistent session store, logout 흐름은 범위에서 제외했다.
