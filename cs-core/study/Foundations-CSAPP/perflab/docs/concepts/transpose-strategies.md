# Transpose Strategies

## Why One Strategy Is Not Enough

Performance Lab is unusual because all matrices solve the same semantic task but stress the cache
differently.

| Size | Main issue | Study strategy |
|---|---|---|
| 32x32 | diagonal conflict in a direct-mapped cache | 8x8 blocking with deferred diagonal write |
| 64x64 | severe conflict when naive 8x8 blocking is reused | quadrant-aware 8x8 schedule with temporary movement through `B` |
| 61x67 | irregular shape and edges | 16x16 blocked traversal with guards |

## What The Companion Benchmark Measures

The study tracks simulate the official `s=5, E=1, b=5` cache while the transpose kernels run.
They count misses on matrix reads and writes only.

This is not a replacement for the official driver, but it preserves the main judgment:

- correctness first
- then miss count
- then relative improvement over the naive kernel
