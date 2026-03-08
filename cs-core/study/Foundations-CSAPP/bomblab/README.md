# Bomb Lab

## Purpose

This is the active study-first migration of CS:APP Bomb Lab.

The frozen reference tree lives in [`/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/bomblab`](/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/bomblab).
This directory separates three concerns that were mixed together in `legacy/`:

- the official lab contract in `problem/`
- fresh companion implementations in `c/` and `cpp/`
- stable public explanations in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | verified | public self-study bomb is restored locally on demand and defused in Docker with tracked sample answers |
| `c/` | verified | fresh companion mini-bomb implemented and tested |
| `cpp/` | verified | same companion contract implemented and tested in C++ |
| `docs/` | complete | reverse-engineering workflow, disclosure policy, and verification notes written |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## What This Project Contains

- `problem/` preserves the official lab shape without redistributing the course bomb.
- `c/` and `cpp/` implement a companion "mini bomb" that recreates the same concept families:
  - string comparison
  - loop-derived numeric constraints
  - switch / jump-table style branching
  - recursion and path encoding
  - nibble-indexed lookup tables
  - linked-list reordering
  - optional BST-based secret phase

The companion tracks are not claimed to be the official bomb binary. They exist so the project
still contains fresh code, tests, and verifiable outputs even when the original course asset
cannot be redistributed.

## Structure

```text
bomblab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
```

## Working Rules

- Read `problem/README.md` first.
- Treat `problem/` as the official contract and external-asset boundary.
- Treat `c/` and `cpp/` as the study-owned code deliverables.
- Keep public explanations in `docs/`.
- Keep process logs, annotated references, and retrospectives in `notion/`.
- Do not paste official answer strings or disassembly dumps into public docs.

## Verification Path

For the official problem track:

```bash
cd problem
make restore-official
make verify-official
```

For the C companion track:

```bash
cd c
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

For the C++ companion track:

```bash
cd cpp
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

The restored official bomb lives under the ignored local directory `problem/official/`.
