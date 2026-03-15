# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/docs/README.md)
- [`docs/concepts/lru-eviction.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/docs/concepts/lru-eviction.md)
- [`docs/concepts/pin-and-dirty.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/docs/concepts/pin-and-dirty.md)
- [`internal/bufferpool/buffer_pool.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go)
- [`tests/buffer_pool_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/tests/buffer_pool_test.go)
- [`tests/lru_cache_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/tests/lru_cache_test.go)
- [`cmd/buffer-pool/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/cmd/buffer-pool/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool
GOWORK=off go test ./...
GOWORK=off go run ./cmd/buffer-pool
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 dirty flush와 pinned eviction failure를 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/07-buffer-pool/tests (cached)`
- demo:
  - `page-1`
- extra snippet:
  - `disk_after_flush modified`
  - `pinned_evict_error true`

## Source-grounded claims

- cache hit increments `PinCount` on the same page object.
- dirty state is set through `UnpinPage(..., true)`.
- dirty pages are written back on `FlushPage()` or eviction.
- pinned eviction currently fails fast instead of searching another victim.

## Explicit boundaries

- No concurrency control
- No async IO
- No advanced replacer fallback
- No page allocation/growth management
