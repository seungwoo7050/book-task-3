# 04 SQL And Data Modeling 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../01-backend-core/04-sql-and-data-modeling/README.md), [`problem/README.md`](../../../01-backend-core/04-sql-and-data-modeling/problem/README.md)
- 구현 표면:
- `solution/go/catalog/catalog.go`
- `solution/go/catalog/catalog_test.go`
- `solution/go/cmd/schemawalk/main.go`
- 검증 표면: `cd solution/go && go run ./cmd/schemawalk`, `cd solution/go && go test ./...`
- 개념 축: `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다., `PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다., join query는 정규화된 데이터를 읽기 쉬운 뷰로 복원하는 단계다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

메모리 DB 위에서 schema, seed, purchase 흐름을 가장 작은 SQL 계약으로 묶는다.
