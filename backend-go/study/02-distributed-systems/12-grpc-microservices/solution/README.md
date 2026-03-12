# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: proto-first contract, minimal server/client, interceptor examples
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/server ./server/cmd`
- `cd solution/go && mkdir -p ./bin && go build -o ./bin/client ./client/cmd`
- `cd solution/go && go test ./...`

## 현재 한계

- generated `.pb.go` workflow는 자동화하지 않았다.
