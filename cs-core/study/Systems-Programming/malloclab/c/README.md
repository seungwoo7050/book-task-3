# C Track

## Scope

This directory contains the fresh C allocator implementation.

It uses:

- 16-byte aligned blocks
- boundary tags
- a doubly-linked explicit free list
- eager coalescing
- in-place `realloc` growth when the next block is free

## Commands

```bash
cd c
make clean && make test
```
