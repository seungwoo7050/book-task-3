# Malloc Lab Problem Boundary

## Overview

Implement a dynamic memory allocator that exposes:

- `mm_init`
- `mm_malloc`
- `mm_free`
- `mm_realloc`

The allocator must use the simulated heap from `memlib.c`.

## Rules

- Do not call the system allocator from the implementation path.
- All returned payload pointers must be 16-byte aligned.
- `realloc(NULL, size)` must behave like `malloc(size)`.
- `realloc(ptr, 0)` must free the block and return `NULL`.
- The `study/` solution tracks may use only `mem_sbrk()` to extend the heap.

## What Lives Here

This folder is the shared problem contract.

It contains:

- a starter allocator file with TODOs
- shared `memlib` heap emulation
- a publishable trace format and trace set
- a stronger trace driver than the one found in `legacy/`

The actual completed allocators live in `../c` and `../cpp`.

## Trace Format

Each trace begins with:

```text
<num_ids> <num_ops>
```

Operations are:

- `a <id> <size>`: allocate `size` bytes
- `f <id>`: free block `id`
- `r <id> <size>`: reallocate block `id` to `size` bytes

The driver writes and validates deterministic payload patterns so that `realloc` correctness
is checked without embedding answer code in the traces themselves.
