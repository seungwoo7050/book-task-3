# Verification

## Problem Boundary

Commands:

```bash
cd problem
make status
```

Current result:

- `problem/` reports the contract-only public-release boundary
- copied starter shell sources, official traces, and the bundled Perl driver are intentionally absent
- active functional verification happens in the C and C++ tracks plus the shared direct harness

## C Track

Commands:

```bash
cd c
make clean && make test
```

Validation coverage:

- direct shell launch and command execution via FIFO control
- direct FIFO-based harness for background-job state and `jobs`
- direct FIFO-based harness that sends `SIGINT` to the actual shell PID and checks `terminated by signal`
- direct FIFO-based harness that stops a foreground job, resumes it with `fg`, then interrupts it

Current result:

- `make test` passes
- the background-job harness observes `Running /bin/sleep 1 &`
- the signal harness observes `terminated by signal 2`
- the stop/resume harness observes both `stopped by signal 18` and later termination

## C++ Track

Commands:

```bash
cd cpp
make clean && make test
```

Validation coverage matches the C track.

Current result:

- `make test` passes
- the same direct signal and stop/resume assertions pass in the C++ implementation
