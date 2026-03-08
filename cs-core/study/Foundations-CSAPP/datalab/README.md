# Data Lab

## Purpose

This is the active study-first migration of CS:APP Data Lab.

The reference tree lives in [`/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/datalab`](/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/datalab).
This directory is the normalized workspace where problem assets, language-specific solutions,
durable docs, and private notes are separated.

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | verified | public contract plus restorable official self-study handout verified with official `dlc` and `btest -T 20` in Docker |
| `c/` | verified | fresh solution and expanded edge-case tests completed |
| `cpp/` | verified | same contract implemented in C++ with parallel tests |
| `docs/` | complete | public reasoning and verification notes written |
| `notion/` | complete | local-only upload-ready notes filled with real content |

## Structure

```text
datalab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
```

## Working Rules

- Read `problem/README.md` first.
- Treat `problem/` as the canonical problem contract.
- Keep implementation work in `c/` and `cpp/`.
- Keep durable in-repo explanations in `docs/`.
- Keep process logs, retrospectives, and link notes in `notion/`.

## Current Verification Path

For the official self-study handout:

```bash
cd problem
make restore-official
make verify-official
```

For the C track:

```bash
cp c/src/bits.c problem/code/bits.c
cd problem
make clean && make
make test
bash script/grade.sh
cd ../c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits
```

For the C++ track:

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

Official operator-legality checking now runs through the restored self-study handout in
`problem/official/datalab-handout/`. The `verify-official` target uses `btest -T 20` because the
Linux/amd64 handout runs through Docker on an Apple Silicon host here, and the default 10 second
limit is too tight under emulation even when the solution is correct.
