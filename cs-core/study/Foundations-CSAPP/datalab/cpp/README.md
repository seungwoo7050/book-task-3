# C++ Track

## Scope

This directory contains the C++ solution track for Data Lab.

The external contract matches the C track: the same 13 functions, the same inputs and outputs,
and the same problem ordering.

## Layout

```text
cpp/
  README.md
  src/
    bits.cpp
  include/
  tests/
    test_bits.cpp
```

## Commands

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

## Notes

- The implementation is written freshly for `study/`, not copied from the legacy answer tree.
- The track keeps the same observable behavior as the C version so both languages remain comparable.
- The test set mirrors the C edge-case coverage, including floating-point boundary cases.
