# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: parser, summarizer, race-safe recorder
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && go run ./cmd/debugdemo`
- `cd solution/go && go test ./... -bench=.`

## 현재 한계

- pprof와 trace는 후속 observability 과제로 넘긴다.
