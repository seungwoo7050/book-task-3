# 18 Workspace SaaS API Structure

## 이 글이 답할 질문

- owner/admin/member RBAC와 invitation, project/issue/comment 흐름을 제품형 도메인으로 묶었다.
- worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `05-portfolio-projects/18-workspace-saas-api` 안에서 `20-auth-and-session-rotation.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 4 — auth 패키지 (토큰 생성/검증)
- 세션 본문: `crypto/rand, internal/auth/tokens.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/auth/tokens.go`
- 코드 앵커 2: `solution/go/internal/repository/store.go`
- 코드 설명 초점: 이 코드는 인증 경계를 말이 아니라 서명 규칙과 상태 전이로 고정한다. access token과 refresh/session 흐름이 실제로 어떻게 분리되는지 보여 주는 기준점이다.
- 개념 설명: access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다.
- 마지막 단락: 다음 글에서는 `30-repository-service-cache-boundaries.md`에서 이어지는 경계를 다룬다.
