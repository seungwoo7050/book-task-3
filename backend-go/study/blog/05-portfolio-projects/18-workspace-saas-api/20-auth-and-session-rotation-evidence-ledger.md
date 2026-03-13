# 18 Workspace SaaS API Evidence Ledger

## 20 auth-and-session-rotation

- 시간 표지: Phase 4 — auth 패키지 (토큰 생성/검증)
- 당시 목표: owner/admin/member RBAC와 invitation, project/issue/comment 흐름을 제품형 도메인으로 묶었다.
- 변경 단위: `crypto/rand`, `internal/auth/tokens.go`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 조치: HMAC-SHA256 JWT: Header.Payload.Signature, base64url 인코딩 Claims: user_id, email, display_name, exp (15분) Refresh token: `crypto/rand` 32바이트 → hex 인코딩 (64자) 저장: SHA256(opaque_token) → DB의 token_hash 컬럼 ParseRefreshToken: hex decode → SHA256 해시 → DB 조회 테스트:

CLI:

```bash
go test ./internal/auth/ -v -count=1
```

- 검증 신호:
- - Refresh token: `crypto/rand` 32바이트 → hex 인코딩 (64자)
- - 저장: SHA256(opaque_token) → DB의 token_hash 컬럼
- - ParseRefreshToken: hex decode → SHA256 해시 → DB 조회
- 핵심 코드 앵커: `solution/go/internal/auth/tokens.go`
- 새로 배운 것: access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다.
- 다음: 다음 글에서는 `30-repository-service-cache-boundaries.md`에서 이어지는 경계를 다룬다.
