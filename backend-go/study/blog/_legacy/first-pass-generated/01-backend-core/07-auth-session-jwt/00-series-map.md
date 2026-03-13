# 07 Auth Session JWT 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../01-backend-core/07-auth-session-jwt/README.md), [`problem/README.md`](../../01-backend-core/07-auth-session-jwt/problem/README.md)
- 구현 표면:
- `solution/go/internal/auth/server.go`
- `solution/go/internal/auth/server_test.go`
- `solution/go/cmd/server/main.go`
- 검증 표면: `cd solution/go && go test -v ./internal/auth`, `cd solution/go && go test -run TestExpiredToken -v ./internal/auth`
- 개념 축: `authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.`, `세션은 서버가 상태를 들고, JWT는 클라이언트가 서명된 토큰을 들고 온다.`, `비밀번호는 평문 저장이 아니라 bcrypt 같은 느린 해시가 기본이다.`

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

session login과 JWT login을 같은 서버 표면 안에서 비교 가능하게 만든다.
