# Realloc And Coalescing

The key allocator decisions in this project are immediate coalescing and a two-stage `realloc`
path.

## Immediate Coalescing

When a block is freed:

1. mark the header and footer free
2. inspect the previous and next neighbours
3. merge with either or both neighbours if they are free
4. insert the merged result back into the free list

That keeps the heap easier to reason about and makes later large requests more likely to fit
without extending the heap.

## Placement

Allocation is first-fit over the explicit free list.

When a fit is found:

- if the remainder is large enough to form a valid free block, split
- otherwise consume the whole block to avoid creating unusable fragments

## Realloc Strategy

The implementation handles `realloc` in this order:

1. `ptr == NULL`: treat as `malloc`
2. `size == 0`: treat as `free`
3. current block already large enough: optionally shrink-split
4. next block is free and the merged size is enough: grow in place
5. otherwise allocate-copy-free

The important learning point is that `realloc` correctness is not only about returning a pointer.
The preserved prefix of the old payload must survive the transition.

## Why Not A More Aggressive Design

The study version stops at an explicit free list because the pedagogical target is:

- block arithmetic
- boundary tags
- free-list mutation
- heap growth and split policy

Segregated lists or more aggressive placement heuristics can be added later, but they are not
required to capture the core allocator reasoning this project is meant to teach.
