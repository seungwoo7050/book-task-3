# Architecture Lab - Problem Contract

## Summary

The original Architecture Lab has three parts:

- Part A: write Y86-64 assembly programs
- Part B: add `iaddq` to the SEQ processor in HCL
- Part C: optimize `ncopy` for the PIPE processor

This `problem/` directory preserves the public handout boundary while restoring the official
self-study handout locally on demand under `official/`.

## What Is Included

| Path | Purpose |
|---|---|
| `README.md` | problem boundary and official restore notes |
| `Makefile` | restore, sync, and official verification helpers |
| `code/README.md` | notes about the tracked study-owned hand-in files living in `../y86/` |
| `script/README.md` | notes about the official simulator workflow |

## Local Official Restore

```bash
cd problem
make restore-official
make verify-official
```

The restore target downloads the public Architecture Lab self-study handout from the official
CS:APP site into the ignored local directory `problem/official/`. The official verification target
then copies the study-owned `../y86/` hand-in files into that restored toolchain and runs the
official Part A/B/C checks in Docker.

## Official Learning Goal

Architecture Lab is about:

- mapping C-like logic to Y86-64
- understanding which control signals implement a new instruction
- reasoning about pipeline hazards and throughput, not just correctness
