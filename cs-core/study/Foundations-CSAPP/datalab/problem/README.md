# Data Lab — Problem Specification

## Summary

Implement 13 programming puzzles in `code/bits.c`. Each puzzle is a C function whose body
must use **only** the operators and constants listed in its comment header, within the
stated maximum operator count.

## Puzzle Table

| # | Function | Description | Rating | Max Ops | Allowed Ops |
|---|----------|-------------|--------|---------|-------------|
| 1 | `bitXor(x,y)` | Compute `x ^ y` using only `~` and `&` | 1 | 14 | `~ &` |
| 2 | `tmin()` | Return the minimum two's complement integer | 1 | 4 | `! ~ & ^ \| + << >>` |
| 3 | `isTmax(x)` | Return 1 if `x` is the maximum two's complement integer | 1 | 10 | `! ~ & ^ \| +` |
| 4 | `allOddBits(x)` | Return 1 if all odd-numbered bits in `x` are set to 1 | 2 | 12 | `! ~ & ^ \| + << >>` |
| 5 | `negate(x)` | Return `-x` | 2 | 5 | `! ~ & ^ \| + << >>` |
| 6 | `isAsciiDigit(x)` | Return 1 if `0x30 <= x <= 0x39` | 3 | 15 | `! ~ & ^ \| + << >>` |
| 7 | `conditional(x,y,z)` | Same as `x ? y : z` | 3 | 16 | `! ~ & ^ \| + << >>` |
| 8 | `isLessOrEqual(x,y)` | Return 1 if `x <= y` | 3 | 24 | `! ~ & ^ \| + << >>` |
| 9 | `logicalNeg(x)` | Implement `!x` without using `!` | 4 | 12 | `~ & ^ \| + << >>` |
| 10 | `howManyBits(x)` | Return minimum bits needed to represent `x` in two's complement | 4 | 90 | `! ~ & ^ \| + << >>` |
| 11 | `floatScale2(uf)` | Return bit-level equivalent of `2*f` for float `f` | 4 | 30 | Any integer/unsigned ops; `\|\|`, `&&`, `if`, `while` |
| 12 | `floatFloat2Int(uf)` | Return bit-level equivalent of `(int)f` | 4 | 30 | Any integer/unsigned ops; `\|\|`, `&&`, `if`, `while` |
| 13 | `floatPower2(x)` | Return bit-level equivalent of `2.0^x` | 4 | 30 | Any integer/unsigned ops; `\|\|`, `&&`, `if`, `while` |

## Constraints (All Integer Puzzles, #1–#10)

* **Allowed types**: `int` only. No `unsigned`, `long`, casts, arrays, structs, unions.
* **Allowed operations**: Only those listed per puzzle.
* **Constants**: Only `0x00` through `0xFF` (0–255).
* **No control flow**: No `if`, `while`, `for`, `do-while`, `switch`, `?:`, `||`, `&&`.
* **No function calls** and no macros other than those already in the template.

## Constraints (Floating-Point Puzzles, #11–#13)

* The argument and return type are `unsigned` (bit-level representation of `float`).
* Conditionals and loops **are** allowed.
* Both `int` and `unsigned` types may be used.
* No floating-point types, operations, or constants.

## Input Data

No external input files are needed. The `btest` harness generates exhaustive or random test
vectors internally.

## Official Self-Study Verification

```bash
make restore-official
make verify-official
```

This restores the public CMU self-study handout under `official/datalab-handout/`, copies the
active C solution into the restored handout, and runs the official `dlc` plus `btest -T 20` in a
Linux/amd64 Docker image. The longer timeout is needed because the public handout is exercised
through amd64 emulation on the local Apple Silicon host.

## Files

| Path | Description |
|------|-------------|
| `code/bits.c` | Skeleton file — implement your solutions here. |
| `code/btest.c` | Test harness source. |
| `code/decl.c` | Auto-generated declarations (do not edit). |
| `code/tests.c` | Reference functions used by `btest` (do not edit). |
| `official/datalab-handout/` | restored public self-study handout with the official `dlc` and `btest` |
| `script/grade.sh` | Runs `dlc` + `btest` and prints a score summary. |
| `Makefile` | Builds `btest` from source. |
