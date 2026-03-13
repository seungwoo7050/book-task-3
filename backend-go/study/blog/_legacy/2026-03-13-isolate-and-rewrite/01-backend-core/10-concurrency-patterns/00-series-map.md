# 10 Concurrency Patterns 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../01-backend-core/10-concurrency-patterns/README.md), [`problem/README.md`](../../../01-backend-core/10-concurrency-patterns/problem/README.md)
- 구현 표면:
- `solution/go/workerpool/pool.go`
- `solution/go/pipeline/pipeline.go`
- `solution/go/workerpool/pool_test.go`
- 검증 표면: `make -C problem run-workerpool`, `make -C problem run-pipeline`, `make -C problem test`
- 개념 축: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다., pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다., `context.Context`는 중단 신호를 한 방향으로 전파하는 공통 장치다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

worker pool과 pipeline을 각각 분리해 context cancellation, backpressure, fan-out을 비교한다.
