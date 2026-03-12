# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: outbox repository, relay, consumer, CLI entrypoints
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/relay ./cmd/relay`
- `cd solution/go && go build -o ./bin/consumer ./cmd/consumer`
- `cd solution/go && go test ./...`
- `cd solution/go && make repro`

## 현재 한계

- 대규모 Kafka 운영 설정은 포함하지 않는다.
