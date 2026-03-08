# C Track

## Scope

This directory contains the fresh C companion implementation for Bomb Lab.

It does not claim to be the official course bomb. It is a study-owned mini-bomb that recreates
the same concept families so the project has verifiable source code and tests.

## Layout

```text
c/
  README.md
  include/
    mini_bomb.h
  src/
    mini_bomb.c
    main.c
  tests/
    test_mini_bomb.c
  data/
  Makefile
```

## Commands

```bash
cd c
make clean && make test

printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

## Notes

- `src/mini_bomb.c` is a fresh implementation, not a copy of the legacy notes.
- `tests/test_mini_bomb.c` exercises valid and invalid cases for every phase.
- The official reverse-engineering workflow still lives under `../problem/` and `../docs/`.
