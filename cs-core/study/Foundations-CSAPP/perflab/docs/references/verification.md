# Verification

## Official Problem Track

Commands:

```bash
cd problem
make status
make compile
```

Current result:

- starter files and `study.trace` are present
- compile checks pass for the starter code
- full official grading is still represented by the active C/C++ study tracks, not by the frozen starter tree

## C Companion Track

Commands:

```bash
cd c
make clean && make test
```

Validation policy:

- cache simulator must match three known oracle outputs on `study.trace`
- transpose must be correct for `32x32`, `64x64`, and `61x67`
- optimized misses must beat naive misses
- optimized misses target the official thresholds: `<300`, `<1300`, `<2000`

Actual result:

- `study.trace` matches the oracle on all three checked cache configurations:
  - `s=1 E=1 b=1` -> `hits=5 misses=10 evictions=8`
  - `s=2 E=1 b=2` -> `hits=6 misses=9 evictions=7`
  - `s=5 E=1 b=5` -> `hits=10 misses=5 evictions=0`
- tuned transpose results:
  - `32x32`: `284` misses
  - `64x64`: `1176` misses
  - `61x67`: `1989` misses

## C++ Companion Track

Commands:

```bash
cd cpp
make clean && make test
```

Validation policy matches the C track.

Actual result:

- `study.trace` matches the oracle on all three checked cache configurations:
  - `s=1 E=1 b=1` -> `hits=5 misses=10 evictions=8`
  - `s=2 E=1 b=2` -> `hits=6 misses=9 evictions=7`
  - `s=5 E=1 b=5` -> `hits=10 misses=5 evictions=0`
- tuned transpose results:
  - `32x32`: `284` misses
  - `64x64`: `1176` misses
  - `61x67`: `1989` misses
