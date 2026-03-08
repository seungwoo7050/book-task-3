# C Track

## Scope

This directory contains the fresh C companion model for Architecture Lab.

It keeps the three official parts executable without depending on the missing Y86/HCL simulator
stack.

## Companion Mapping

- Part A -> linked-list sum and copy-with-XOR semantics
- Part B -> a direct `iaddq` stage-semantics model with condition-code updates
- Part C -> correctness-preserving `ncopy` implementations plus a simple pipeline-cost estimator

## Commands

```bash
cd c
make clean && make test
```
