# Bomb Lab - Problem Contract

## Summary

The original CS:APP Bomb Lab gives you an x86-64 Linux executable with six phases and an optional
secret phase. Each phase expects a specific input. Wrong input explodes the bomb.

This `problem/` directory preserves that contract while restoring the public CMU self-study bomb
locally on demand under `official/`.

## What Is Included

| Path | Purpose |
|---|---|
| `README.md` | problem contract and local setup instructions |
| `Makefile` | restore, analysis, and Docker verification helpers for the public self-study bomb |
| `code/bomb.c` | high-level structural skeleton, not the runnable bomb |
| `data/solutions.txt` | verified answer file for the public self-study bomb |
| `script/run_bomb.sh` | convenience runner for a locally supplied bomb |

## Local Official Restore

```bash
cd problem
make restore-official
make verify-official
```

The restore target downloads the public self-study bomb from the official CS:APP site into the
ignored local directory `problem/official/`.

## Official Learning Goal

Bomb Lab is about:

- reading x86-64 assembly
- using `gdb`, `objdump`, `strings`, and `nm`
- mapping machine-level control flow back to C-like logic
- recognizing arrays, linked lists, and trees in memory
- working methodically under a "do not brute force" constraint

## Local Workflow With A Supplied Bomb

```bash
cd problem
make status
make disas
make strings
make symbols
bash script/run_bomb.sh --gdb
```

## Publication Rule

- keep restored official binaries out of version control
- keep course-instance-specific answer strings out of public docs
- keep public material focused on workflow, patterns, and verification boundaries
