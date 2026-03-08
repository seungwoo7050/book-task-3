# C Track

## Scope

This directory contains the fresh C companion implementation for Attack Lab.

Instead of redistributing or rebuilding the official exploit targets, this track implements a
payload verifier that checks whether a hex byte stream matches the intended structure of each
study phase.

## Layout

```text
c/
  README.md
  include/
    mini_attacklab.h
  src/
    mini_attacklab.c
    main.c
  tests/
    test_mini_attacklab.c
  data/
    phase1.txt
    phase2.txt
    phase3.txt
    phase4.txt
    phase5.txt
  Makefile
```

## Commands

```bash
cd c
make clean && make test
```

## Notes

- The verifier keeps the learning focus on payload layout and exploit reasoning.
- It does not execute arbitrary injected code.
- Sample payload files in `data/` are valid for the companion verifier only.
