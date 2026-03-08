# Verification

## Official Problem Track

Commands:

```bash
cd problem
make restore-official
make verify-official
```

Current result:

- all five official phases pass against the restored public `target1` self-study handout
- the restored binaries remain local-only under the ignored `problem/official/` tree

## C Companion Track

Commands:

```bash
cd c
make clean && make test
```

Actual result:

- sample payload verification passes for phases 1 through 5
- unit tests pass

## C++ Companion Track

Commands:

```bash
cd cpp
make clean && make test
```

Actual result:

- sample payload verification passes for phases 1 through 5
- unit tests pass

## Current Judgment

The project is verifiable at both the official self-study and companion-track levels.
