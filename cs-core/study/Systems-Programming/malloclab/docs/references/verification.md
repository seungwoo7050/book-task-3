# Verification

## Problem Starter

Commands:

```bash
cd problem
make clean && make
```

Current result:

- the starter allocator contract compiles
- active functional verification happens in the C and C++ tracks

## Shared Driver

The legacy driver was too weak because it did not iterate traces meaningfully or check payload
preservation.

The `study/` driver now checks:

- 16-byte alignment
- no overlap between live payload ranges
- payload preservation across `realloc`
- aggregate utilization and throughput summaries across all traces

## C Track

Commands:

```bash
cd c
make clean && make test
```

Validation coverage:

- `basic.rep` for allocation/free baseline behavior
- `coalesce.rep` for split and merge pressure
- `realloc.rep` for `realloc(NULL, size)`, growth, shrink, and `realloc(ptr, 0)`
- `mixed.rep` for interleaved allocator behavior

Current result:

- `make test` passes
- `basic.rep`, `coalesce.rep`, `mixed.rep`, `realloc.rep` all finish with `errors=0`
- summary: `avg_util=0.077`, `throughput=4691933 ops/s`

## C++ Track

Commands:

```bash
cd cpp
make clean && make test
```

Validation coverage matches the C track.

Current result:

- `make test` passes
- the same four traces finish with `errors=0`
- summary: `avg_util=0.077`, `throughput=5033165 ops/s`
