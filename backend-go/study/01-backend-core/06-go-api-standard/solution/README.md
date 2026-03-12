# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: `net/http` API, middleware, in-memory movie store
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- `cd solution/go && go test -race ./...`

## 현재 한계

- DB-backed persistence는 포함하지 않는다.
