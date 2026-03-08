# C++ Track

## Scope

This directory contains the fresh C++ implementation of the tiny shell.

It mirrors the C track:

- foreground and background jobs
- built-ins: `quit`, `jobs`, `bg`, `fg`
- signal forwarding and `SIGCHLD` reaping
- trace-driven tests plus stronger custom signal traces

## Commands

```bash
cd cpp
make clean && make test
```
