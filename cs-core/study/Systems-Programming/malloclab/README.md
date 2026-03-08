# Malloc Lab

## Purpose

This is the active study-first migration of the allocator lab.

The frozen reference tree lives in
[`/Users/woopinbell/work/cs-core/legacy/Systems-Programming/malloclab`](/Users/woopinbell/work/cs-core/legacy/Systems-Programming/malloclab).
This project separates:

- the allocator contract and shared trace driver in `problem/`
- fresh allocators in `c/` and `cpp/`
- public design notes and verification records in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | migrated safely | starter allocator, shared memlib, publishable trace set, and shared driver |
| `c/` | verified | explicit free list allocator with in-place growth path |
| `cpp/` | verified | same allocator contract implemented in C++ |
| `docs/` | complete | invariants, coalescing, realloc strategy, and verification policy documented |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## Learning Goals

This project is meant to force three kinds of understanding at once:

- heap block layout and alignment discipline
- free-list policy and coalescing tradeoffs
- correctness under `malloc`, `free`, and `realloc` traces

The `study/` version keeps the official-style API but replaces the weak legacy driver with a
trace runner that checks alignment, overlap, and `realloc` payload preservation.

## Structure

```text
malloclab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
```

## Verification Path

For the starter contract:

```bash
cd problem
make clean && make
```

For the C track:

```bash
cd c
make clean && make test
```

For the C++ track:

```bash
cd cpp
make clean && make test
```
