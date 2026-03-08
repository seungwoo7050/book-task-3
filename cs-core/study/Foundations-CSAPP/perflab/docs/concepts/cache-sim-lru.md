# Cache Simulator And LRU

## Core Lesson

Part A is about turning an address trace into cache-state transitions.

For each access, the simulator must answer:

1. which set does this address map to?
2. which tag should be present for a hit?
3. if it misses, is there an empty line?
4. if not, which line is the LRU victim?

## Companion Validation Policy

The study tracks validate the simulator against known outputs from the migrated study-owned
`study.trace`:

- `s=1 E=1 b=1` -> `hits:5 misses:10 evictions:8`
- `s=2 E=1 b=2` -> `hits:6 misses:9 evictions:7`
- `s=5 E=1 b=5` -> `hits:10 misses:5 evictions:0`

This gives the migrated implementation a fixed oracle without redistributing any course trace asset.
