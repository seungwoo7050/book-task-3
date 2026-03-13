# 11 Rate Limiter 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../01-backend-core/11-rate-limiter/README.md), [`problem/README.md`](../../01-backend-core/11-rate-limiter/problem/README.md)
- 구현 표면:
- `solution/go/limiter.go`
- `solution/go/middleware.go`
- `solution/go/limiter_test.go`
- 검증 표면: `make -C problem test`, `cd solution/go && go test -bench=. -benchmem ./...`
- 개념 축: `token bucket은 burst를 허용하면서 평균 처리율을 제한한다.`, `per-client limiter는 같은 서버 안에서 클라이언트 간 간섭을 줄인다.`, `middleware에 붙이면 개별 handler가 rate limit 세부 사항을 몰라도 된다.`

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

token bucket 구현과 per-client middleware를 분리해 rate limit을 코드로 설명한다.
