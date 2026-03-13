# 08 SQL Store API 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../01-backend-core/08-sql-store-api/README.md), [`problem/README.md`](../../01-backend-core/08-sql-store-api/problem/README.md)
- 구현 표면:
- `solution/go/internal/store/store.go`
- `solution/go/internal/store/store_test.go`
- `solution/go/cmd/server/main.go`
- 검증 표면: `cd solution/go && go test -v ./internal/store`, `cd solution/go && go test -run TestReserveStockRollback -v ./internal/store`
- 개념 축: `migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.`, `repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.`, optimistic update는 `version` 조건으로 충돌을 감지한다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

migration 가능한 저장소와 HTTP app을 같이 세워 CRUD와 재고 reserve rollback을 설명한다.
