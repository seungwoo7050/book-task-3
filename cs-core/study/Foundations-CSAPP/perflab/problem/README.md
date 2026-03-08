# Performance Lab - Problem Contract

## Summary

The original Performance Lab has two parts:

- Part A: build a cache simulator that replays memory traces
- Part B: optimize matrix transpose to reduce cache misses

This `problem/` directory preserves that official starter boundary while leaving active
implementation work to `c/` and `cpp/`.

## What Is Included

| Path | Purpose |
|---|---|
| `README.md` | problem contract and local starter notes |
| `Makefile` | starter compile checks |
| `code/csim.c` | Part A starter |
| `code/trans.c` | Part B starter |
| `code/cachelab.h` | helper declarations |
| `code/cachelab.c` | helper implementation |
| `data/traces/study.trace` | study-owned sample trace asset |
| `script/driver.py` | self-written simplified grading helper |

## What Is Not Included

- the compiled legacy `csim` binary
- platform-specific debug bundles such as `.dSYM`
- missing official test drivers referenced in some readmes

## Public-Release Note

The sample trace shipped here is study-owned and exists only to keep the cache simulator example
verifiable without redistributing course trace assets.

## Official Learning Goal

Performance Lab is about:

- decomposing addresses into cache fields
- implementing LRU replacement correctly
- understanding locality and conflict misses
- using matrix-specific access patterns to reduce misses on a fixed cache
