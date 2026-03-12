# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: API server, purchase service, relay, repository, e2e tests
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- `cd solution/go && go test ./...`
- `cd solution/go && make repro`

## 현재 한계

- OAuth나 MSA 분리는 필수 범위에 넣지 않는다.
