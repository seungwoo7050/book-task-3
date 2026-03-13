# 02 Types Errors Interfaces 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../00-go-fundamentals/02-types-errors-interfaces/README.md), [`problem/README.md`](../../../00-go-fundamentals/02-types-errors-interfaces/problem/README.md)
- 구현 표면:
- `solution/go/domain/catalog.go`
- `solution/go/domain/catalog_test.go`
- `solution/go/cmd/inventorydemo/main.go`
- 검증 표면: `cd solution/go && go run ./cmd/inventorydemo`, `cd solution/go && go test ./...`
- 개념 축: struct는 상태를, method는 그 상태에 대한 동작을 표현한다., interface는 “무엇을 할 수 있는가”를 분리할 때만 쓰는 편이 단순하다., custom error 타입은 `errors.As`로 세부 의미를 복원할 수 있게 해 준다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

struct, method, interface, custom error를 카탈로그 가격 계산이라는 한 문제로 묶는다.
