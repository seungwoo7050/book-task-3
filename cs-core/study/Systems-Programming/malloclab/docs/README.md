# Malloc Lab Docs

## Purpose

This folder keeps the public explanation for the migrated allocator project.

It focuses on:

- allocator invariants that must remain true after every operation
- why explicit free lists are a better midpoint than an implicit-only allocator here
- how `realloc` correctness is verified

## Document Map

- [`concepts/allocator-invariants.md`](concepts/allocator-invariants.md): block layout, alignment, and free-list invariants
- [`concepts/realloc-and-coalescing.md`](concepts/realloc-and-coalescing.md): coalescing policy and in-place growth strategy
- [`references/verification.md`](references/verification.md): starter compile path, trace coverage, and measured results
