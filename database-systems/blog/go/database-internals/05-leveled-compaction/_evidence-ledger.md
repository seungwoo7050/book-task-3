# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/docs/README.md)
- [`docs/concepts/merge-ordering.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/docs/concepts/merge-ordering.md)
- [`docs/concepts/manifest-atomicity.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/docs/concepts/manifest-atomicity.md)
- [`internal/compaction/compaction.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go)
- [`tests/compaction_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/tests/compaction_test.go)
- [`cmd/leveled-compaction/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/cmd/leveled-compaction/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction
GOWORK=off go test ./...
rm -rf .demo-data
GOWORK=off go run ./cmd/leveled-compaction
rm -rf .demo-data
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 deepest 여부에 따른 tombstone drop 조건을 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
rm -rf .tmpcheck-data .tmpcheck-data-l2
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/05-leveled-compaction/tests (cached)`
- demo:
  - `apple=red`
  - `banana=gold`
  - `pear=green`
- extra snippet:
  - `drop_at_deepest true 000003.sst [000003.sst]`
  - `lookup_after_drop false true`
  - `keep_above_deepest false 000003.sst`
  - `lookup_after_keep true true`

## Source-grounded claims

- L0 files are reversed into newest-first source order before merge.
- equal-key conflict keeps the left/newer source record.
- deepest compaction is approximated as `len(Levels[2]) == 0`.
- manifest is persisted through `fileio.AtomicWrite()` after new SSTable creation.

## Explicit boundaries

- No scheduler
- No general multi-level balancing
- No concurrent compaction coordination
- No manifest journal or rollback path
