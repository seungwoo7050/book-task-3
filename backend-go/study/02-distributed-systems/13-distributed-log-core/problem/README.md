# Problem: Distributed Log

## Objective

Implement a **distributed commit log** — an append-only, ordered data structure
that forms the backbone of systems like Kafka, NATS, and Pulsar.

## Part 1: Store

### Requirements

1. Implement a `Store` that wraps a file for storing record data.
2. Records are stored with a **length prefix** (8 bytes, big-endian uint64).
3. `Append(data []byte)` writes the record and returns `(n int, pos uint64, err error)`:
   - `n`: total bytes written (including the length prefix).
   - `pos`: the starting position of the record in the file.
4. `Read(pos uint64)` reads the record at the given position.
5. The store must be closeable and flushable.

### Format

```
┌──────────┬──────────────────┐
│ len (8B) │ data (len bytes) │
├──────────┼──────────────────┤
│ len (8B) │ data (len bytes) │
└──────────┴──────────────────┘
```

## Part 2: Index

### Requirements

1. Implement an `Index` that maps **offsets to store positions**.
2. Each index entry is a fixed `12 bytes`: `[offset (4B) | position (8B)]`.
3. The index file should be pre-allocated (memory-mapped) for fast access.
4. `Write(off uint32, pos uint64)` appends an entry.
5. `Read(entryNum int64)` returns `(off uint32, pos uint64, err error)`.
   - If `entryNum == -1`, read the last entry.

## Part 3: Segment

### Requirements

1. A `Segment` pairs a `Store` and an `Index`.
2. It has a `baseOffset` and `nextOffset`.
3. `Append(record []byte)` stores the data and index entry.
4. `Read(off uint64)` retrieves a record by its absolute offset.
5. When the store or index exceeds `MaxBytes`, the segment is "full."

## Part 4: Log

### Requirements

1. A `Log` manages an ordered list of segments.
2. New records go to the **active segment** (last segment).
3. When the active segment is full, a new one is created.
4. `Append(record []byte)` returns the offset.
5. `Read(offset uint64)` finds the right segment and reads from it.
6. `Close()` closes all segments.
7. `Reset()` removes all segments and data.

## Part 5: Replicator (Bonus)

1. Implement a basic replicator that reads from a leader log and appends
   to a follower log.
2. Tracks the last replicated offset.

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Store correctness | 20% | Append and read work with binary encoding |
| Index correctness | 20% | Offset-to-position mapping is accurate |
| Segment + Log | 25% | Multi-segment management works |
| File cleanup | 15% | Close, truncate, and reset work properly |
| Tests | 20% | Full test coverage for each component |
