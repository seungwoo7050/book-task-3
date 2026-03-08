# C Track

## Scope

This directory contains the fresh C implementation of the tiny shell.

It includes:

- real job control with foreground and background execution
- forwarding `SIGINT` and `SIGTSTP` to the foreground process group
- trace-driven tests plus a few stronger custom traces for signal and `fg`/`bg` behavior

## Commands

```bash
cd c
make clean && make test
```
