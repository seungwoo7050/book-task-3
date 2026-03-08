# C++ Track

## Scope

This directory contains the fresh C++ companion implementation for Bomb Lab.

Like the C track, this is a study-owned mini-bomb rather than a redistributed course binary.
The goal is to solve the same conceptual phase families with modern C++ tooling and tests.

## Layout

```text
cpp/
  README.md
  include/
    mini_bomb.hpp
  src/
    mini_bomb.cpp
    main.cpp
  tests/
    test_mini_bomb.cpp
  data/
  Makefile
```

## Commands

```bash
cd cpp
make clean && make test

printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

## Notes

- The C++ track mirrors the C companion contract, so behavior can be compared phase by phase.
- Parsing and validation use C++ standard-library facilities, but the underlying puzzle constraints
  stay the same.
