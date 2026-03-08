# Verification

## Official Problem Track

Commands:

```bash
cd problem
make restore-official
make verify-official
```

Current result:

- Part A Y86-64 programs assemble and produce the expected `0xcba` results
- Part B SEQ `iaddq` changes pass the official regression tests
- Part C PIPE `iaddq` regression, `ncopy` correctness, and benchmark all run in Docker
- latest official Part C benchmark: `Average CPE 9.16`, `Score 26.8/60.0`
- the restored simulator stack remains local-only under the ignored `problem/official/` tree

## C Companion Track

Commands:

```bash
cd c
make clean && make test
```

Actual result:

- companion sample run succeeds
- unit tests pass
- optimized pseudo-CPE beats baseline while preserving correctness

## C++ Companion Track

Commands:

```bash
cd cpp
make clean && make test
```

Actual result:

- companion sample run succeeds
- unit tests pass
- optimized pseudo-CPE beats baseline while preserving correctness

## Current Judgment

The project is verifiable at both the restored official-toolchain and companion-track levels.
