# Allocator Invariants

The study allocators keep a deliberately small set of invariants.

## Block Layout

Every block has:

- an 8-byte header
- an 8-byte footer
- a payload region

Free blocks use the first 16 payload bytes as:

- next-free pointer
- previous-free pointer

That forces a 32-byte minimum block size:

- 8 bytes header
- 16 bytes free-list links
- 8 bytes footer

## Alignment

Payload pointers are returned at 16-byte boundaries.

The implementation enforces that by:

- keeping block sizes aligned to 16
- using a 16-byte prologue arrangement
- rounding requested payload sizes up after adding header/footer overhead

## Free-List Invariants

The explicit free list must satisfy:

- every block in the list is marked free
- no allocated block appears in the list
- coalesced neighbours do not remain as separate list nodes
- removing and re-inserting a block updates both neighbour pointers

The project intentionally uses one free list instead of segregated classes because that is a good
midpoint for learning:

- more realistic than a bump allocator or implicit-only baseline
- still small enough to reason about by hand

## Correctness Checks

The trace driver checks external invariants, not just crashes:

- allocated payload pointers are 16-byte aligned
- live payload ranges do not overlap
- data written before `realloc` survives in the preserved prefix
- all traces finish with zero logical errors
