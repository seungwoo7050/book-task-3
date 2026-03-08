# Performance Lab Docs

## Purpose

This folder keeps the public explanation for the migrated Performance Lab project.

It explains:

- what benchmark policy the study tracks use
- how the cache simulator is validated
- why transpose optimization is measured through misses rather than wall-clock time

## Document Map

- [`concepts/cache-sim-lru.md`](concepts/cache-sim-lru.md): address decomposition, hit path, miss path, and LRU replacement
- [`concepts/transpose-strategies.md`](concepts/transpose-strategies.md): why 32x32, 64x64, and 61x67 need different strategies
- [`references/verification.md`](references/verification.md): commands, oracle checks, and transpose thresholds

## Benchmark Policy

- cache simulator: match known oracle outputs on the self-authored `study.trace`
- transpose: require correctness, require improvement over naive, and target the official miss thresholds
