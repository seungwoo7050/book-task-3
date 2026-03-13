# 06 Go API Standard 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../01-backend-core/06-go-api-standard/README.md), [`problem/README.md`](../../01-backend-core/06-go-api-standard/problem/README.md)
- 구현 표면:
- `solution/go/internal/data/movies.go`
- `solution/go/cmd/api/handlers.go`
- `solution/go/cmd/api/handlers_test.go`
- `solution/go/cmd/api/main.go`
- 검증 표면: `cd solution/go && go test -v ./cmd/api`, `cd solution/go && go test -race ./...`
- 개념 축: application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다., `JSON envelope는 응답 shape를 고정해 클라이언트와 테스트를 단순하게 만든다.`, recoverPanic`, 요청 로깅, CORS 같은 middleware는 프레임워크 없이도 충분히 조합 가능하다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

외부 router 없이 JSON envelope, middleware, graceful shutdown까지 표준 라이브러리로 정리한다.
