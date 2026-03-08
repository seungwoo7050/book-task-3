# Pipeline Cost Model

## What Part C Is Really About

Part C is not only "make `ncopy` shorter." It is "change instruction scheduling so the pipeline
spends fewer cycles per element while still producing the same result."

## Companion Approximation

The study-owned model keeps two views of `ncopy`:

- a baseline schedule
- an optimized schedule with 4-way unrolling

It then assigns a small pseudo-cycle model to each:

- baseline: higher loop overhead and more hazard exposure
- optimized: lower overhead per element and fewer repeated branch costs

The numbers here are not official simulator scores. They are a teaching aid that complements the
restored official benchmark path under `problem/official/` and lets the tracked companion code
verify the intended inequality:

`optimized_cpe < baseline_cpe`

## Why This Still Matters

Even with the official PIPE simulator restored locally, the student still has to reason about:

- preserving correctness under reordering
- why loop unrolling changes throughput
- why performance is a separate dimension from correctness
