# C++ Track

## Scope

This directory contains the fresh C++ implementation of the proxy.

It mirrors the C track:

- HTTP/1.0 `GET` forwarding
- detached per-connection threads
- mutex-protected LRU cache
- canonical header rewriting

## Commands

```bash
cd cpp
make clean && make test
```
