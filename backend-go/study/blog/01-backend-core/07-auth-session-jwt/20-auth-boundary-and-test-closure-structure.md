# 07 Auth Session JWT Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 권한 실패와 인증 실패를 응답 코드로 분리해 이후 RBAC 과제로 이어지게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/07-auth-session-jwt` 안에서 `20-auth-boundary-and-test-closure.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 9단계: 미들웨어 구현 -> 10단계: main.go 작성 -> 11단계: 실행 및 검증 -> 12단계: docs/ 작성
- 세션 본문: `solution/go/internal/auth/server.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/auth/server.go`
- 코드 앵커 2: `solution/go/internal/auth/server.go`
- 코드 설명 초점: 이 코드는 인증 경계를 말이 아니라 서명 규칙과 상태 전이로 고정한다. access token과 refresh/session 흐름이 실제로 어떻게 분리되는지 보여 주는 기준점이다.
- 개념 설명: 세션은 서버가 상태를 들고, JWT는 클라이언트가 서명된 토큰을 들고 온다.
- 마지막 단락: refresh token, persistent session store, logout 흐름은 범위에서 제외했다.
