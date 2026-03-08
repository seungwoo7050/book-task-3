# Y86 Official Track

## Scope

This directory holds the study-owned hand-in artifacts for the official CS:APP Architecture Lab.

It contains:

- Part A Y86-64 assembly solutions
- Part C optimized `ncopy.ys`
- a patch script that applies the required Part B and Part C `iaddq` changes to the restored
  official HCL templates

The official simulator and handout files are restored locally under `problem/official/` and are
not tracked. `make verify-official` from `problem/` copies these study-owned files into that local
handout tree and runs the official tests in Docker.

Latest official Part C result:

- `Average CPE 9.16`
- `Score 26.8/60.0`

## Commands

```bash
cd problem
make restore-official
make verify-official
```
