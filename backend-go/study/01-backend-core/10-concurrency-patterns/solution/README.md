# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: worker pool, pipeline, context-aware cancellation
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && go run ./cmd/workerpool`
- `cd solution/go && go run ./cmd/pipeline`
- `cd solution/go && go test -race ./...`

## 현재 한계

- 외부 queue와 연결하지 않는다.
