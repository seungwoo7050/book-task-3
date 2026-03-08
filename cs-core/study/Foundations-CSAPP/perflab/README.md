# Performance Lab

## Purpose

This is the active study-first migration of CS:APP Performance Lab.

The frozen reference tree lives in [`/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/perflab`](/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/perflab).
This directory separates:

- the official problem contract in `problem/`
- fresh study-owned implementations in `c/` and `cpp/`
- durable public explanations in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | publishable | self-written starter boundary plus a study-owned sample trace |
| `c/` | verified | fresh cache simulator and instrumented transpose benchmark implemented and tested |
| `cpp/` | verified | same companion contract implemented and tested in C++ |
| `docs/` | complete | benchmark policy, locality reasoning, and verification notes written |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## Project Strategy

The original lab has two deliverables:

- Part A: a cache simulator
- Part B: a cache-friendly transpose kernel

The migrated `problem/` tree keeps only a self-written starter boundary and a study-owned sample
trace. The active implementations live in `c/` and `cpp/`, where each track contains:

- a real trace-driven cache simulator
- an instrumented transpose benchmark that simulates the official direct-mapped cache
- correctness checks plus a benchmark policy tied to cache misses

## Structure

```text
perflab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
```

## Verification Path

For the official problem track:

```bash
cd problem
make status
make compile
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
