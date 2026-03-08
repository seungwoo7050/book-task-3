# Part Split

## Why This Lab Needs A Split View

Architecture Lab is not one kind of artifact repeated three times.

- Part A is about program semantics at the ISA level.
- Part B is about control logic that makes a new instruction legal.
- Part C is about performance under a pipeline model.

That is why the study migration keeps the lab as one project but maps each part into a different
companion deliverable.

## Study Mapping

| Official part | Study-owned companion |
|---|---|
| Part A Y86 assembly | C/C++ functions that preserve the same dataflow and return values |
| Part B SEQ `iaddq` | an explicit stage-semantics model with `valB + valC`, write-back, and CC updates |
| Part C PIPE `ncopy` | baseline vs optimized `ncopy` plus a simple pseudo-CPE model |

## Why This Is Acceptable

The public self-study Y86/HCL environment is now restorable locally under `problem/official/`, so
the repository can run the official simulator checks as well as the benchmark. The companion model
still matters because it keeps the same reasoning load visible in tracked C/C++ code instead of
hiding it inside restored local-only handout files.
