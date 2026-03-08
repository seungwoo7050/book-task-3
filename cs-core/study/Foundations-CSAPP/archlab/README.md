# Architecture Lab

## Purpose

This is the active study-first migration of CS:APP Architecture Lab.

The frozen reference tree lives in [`/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/archlab`](/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/archlab).
This directory separates:

- the official multi-part problem contract in `problem/`
- the study-owned official hand-in track in `y86/`
- fresh study-owned companion models in `c/` and `cpp/`
- durable public explanations in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | verified | official self-study handout is restorable locally and the simulator stack is exercised in Docker, including the Part C benchmark |
| `y86/` | verified | study-owned Part A and Part C hand-in files plus HCL patch logic pass the official Part A/B/C checks; latest Part C benchmark is `Average CPE 9.16`, `Score 26.8/60.0` |
| `c/` | verified | fresh companion model for Parts A, B, and C implemented and tested |
| `cpp/` | verified | same companion contract implemented and tested in C++ |
| `docs/` | complete | part split, control-signal reasoning, and verification notes written |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## Project Strategy

The original lab has three different deliverable types:

- Y86-64 assembly programs
- HCL control-logic modifications
- pipeline-oriented performance optimization

The legacy tree keeps only partial starter material, and the simulator/HCL submission files are
not present. So this migration now uses three layers:

- `problem/` restores the public self-study handout locally when verification is needed.
- `y86/` holds the study-owned Part A assembly, Part C `ncopy`, and the HCL patch logic applied to
  the restored official templates.
- `c/` and `cpp/` implement a companion model that keeps the three core lessons executable:
  - Part A: iterative sum, recursive sum, and copy-with-XOR semantics
  - Part B: `iaddq` stage semantics, destination write-back, and condition-code updates
  - Part C: correctness-preserving `ncopy` plus a simple pipeline-cost estimator that shows why
    an optimized schedule lowers pseudo-CPE

## Structure

```text
archlab/
  README.md
  problem/
  y86/
  c/
  cpp/
  docs/
  notion/
```

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
```

For the C++ companion track:

```bash
cd cpp
make clean && make test
```

The restored official toolchain lives under the ignored local directory `problem/official/`.
The latest official Part C run completed with `Average CPE 9.16` and `Score 26.8/60.0`.
