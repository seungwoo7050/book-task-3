# C++ Track

## Scope

This directory contains the fresh C++ allocator implementation.

It keeps the same `mm_*` contract as the C track while using C++ implementation syntax.

Key properties:

- explicit free list with boundary tags
- eager coalescing
- split on placement when a remainder can form a valid free block
- in-place `realloc` growth into the next free block

## Commands

```bash
cd cpp
make clean && make test
```
