# Verification Notes

## Commands

### Official Self-Study Handout

```bash
cd problem
make restore-official
make verify-official
```

### C Edge Cases

```bash
cd c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c
./test_bits
```

### C++ Edge Cases

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

## Current Results

- `make verify-official`: passed with the restored official `dlc` plus `btest -T 20`
- `c/tests/test_bits.c`: `55 / 55 edge-case tests passed`
- `cpp/tests/test_bits.cpp`: `55 / 55 C++ edge-case tests passed`
