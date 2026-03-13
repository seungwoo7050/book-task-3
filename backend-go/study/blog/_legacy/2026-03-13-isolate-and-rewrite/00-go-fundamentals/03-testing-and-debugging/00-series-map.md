# 03 Testing And Debugging 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../00-go-fundamentals/03-testing-and-debugging/README.md), [`problem/README.md`](../../../00-go-fundamentals/03-testing-and-debugging/problem/README.md)
- 구현 표면:
- `solution/go/analyzer/analyzer.go`
- `solution/go/analyzer/analyzer_test.go`
- `solution/go/cmd/debugdemo/main.go`
- 검증 표면: `cd solution/go && go run ./cmd/debugdemo`, `cd solution/go && go test ./... -bench=.`
- 개념 축: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다., subtest는 실패 지점을 이름으로 드러내 준다., benchmark는 “더 빠르다”는 감각을 숫자로 바꾸는 최소 도구다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

로그 parser와 recorder를 쪼갠 뒤 table-driven test, benchmark, race detector를 같은 루프로 돌린다.
