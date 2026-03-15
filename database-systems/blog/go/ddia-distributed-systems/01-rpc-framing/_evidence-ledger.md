# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/docs/README.md)
- [`docs/concepts/frame-boundary.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/frame-boundary.md)
- [`docs/concepts/pending-map.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/docs/concepts/pending-map.md)
- [`internal/framing/framing.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing/framing.go)
- [`internal/rpc/rpc.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc/rpc.go)
- [`tests/rpc_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/tests/rpc_test.go)
- [`cmd/rpc-framing/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/cmd/rpc-framing/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing
GOWORK=off go test ./...
GOWORK=off go run ./cmd/rpc-framing
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 split chunk decode와 error/timeout 전파를 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/ddia-distributed-systems/projects/01-rpc-framing/tests (cached)`
- demo:
  - `pong:hello`
- extra snippet:
  - `split_payloads 0 1`
  - `errors true true`

## Source-grounded claims

- framing uses a 4-byte big-endian length prefix.
- client pending map is keyed by correlation id.
- timeout and disconnect both remove pending entries.
- malformed JSON payloads are currently ignored rather than fatal.

## Explicit boundaries

- No TLS
- No auth
- No streaming RPC
- No discovery/load balancing
- No retry policy
