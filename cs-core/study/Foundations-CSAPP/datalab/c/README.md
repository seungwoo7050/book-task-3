# C Track

## Scope

This directory contains the fresh C solution track for Data Lab.

## Layout

```text
c/
  README.md
  src/
    bits.c
  include/
  tests/
    test_bits.c
```

## Commands

```bash
# From datalab/
cp c/src/bits.c problem/code/bits.c
cd problem
make clean && make
make test
bash script/grade.sh

# Edge-case test
cd ../c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits
```

## Notes

- `src/bits.c` was rewritten from the starter contract instead of being copied from the legacy answer.
- `tests/test_bits.c` supplements the lab harness with integer and floating-point edge cases.
- `problem/code/bits.c` should stay as the starter contract file. Copy the active solution into it only for harness-based verification.
