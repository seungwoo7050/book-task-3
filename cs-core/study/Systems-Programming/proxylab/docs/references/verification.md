# Verification

## Problem Starter

Commands:

```bash
cd problem
make clean && make
```

Current result:

- the starter proxy contract compiles
- active functional verification happens in the C and C++ tracks

## Shared Harness

The `study/` project uses a local threaded origin server and a reusable shell harness.

The harness checks:

- basic proxying of a local request
- required outbound header rewriting
- cache hits for small responses
- no caching for oversized responses
- concurrent servicing of two slow requests
- continued operation after a failed upstream connection

## C Track

Commands:

```bash
cd c
make clean && make test
```

Current result:

- `make test` passes
- basic local GET through the proxy passes
- required `Host`, `User-Agent`, `Connection`, and `Proxy-Connection` rewriting is observed
- a small object is served from cache on the second request
- an oversized object is fetched again on the second request
- the proxy remains usable after a failed upstream connection

## C++ Track

Commands:

```bash
cd cpp
make clean && make test
```

Current result:

- `make test` passes
- the same forwarding, header, cache, concurrency, and failure-recovery checks all pass
