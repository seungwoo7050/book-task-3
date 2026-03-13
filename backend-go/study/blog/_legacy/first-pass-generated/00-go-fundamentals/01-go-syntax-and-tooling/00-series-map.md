# 01 Go Syntax And Tooling 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../00-go-fundamentals/01-go-syntax-and-tooling/README.md), [`problem/README.md`](../../00-go-fundamentals/01-go-syntax-and-tooling/problem/README.md)
- 구현 표면:
- `solution/go/lesson/lesson.go`
- `solution/go/lesson/lesson_test.go`
- `solution/go/cmd/toolingdemo/main.go`
- 검증 표면: `cd solution/go && go run ./cmd/toolingdemo`, `cd solution/go && go test ./...`
- 개념 축: strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다., map[string]int`는 가장 단순한 빈도 계산 구조다., 결과를 `Summary` struct로 묶으면 함수 반환값이 늘어나도 호출부가 덜 흔들린다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

문자열 정규화와 단어 빈도 계산을 CLI보다 먼저 고정한 뒤, 가장 작은 `go run` / `go test` 루프를 닫는다.
