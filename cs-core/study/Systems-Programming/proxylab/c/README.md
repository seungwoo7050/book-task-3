# C Track

## Scope

This directory contains the fresh C implementation of the proxy.

It supports:

- HTTP/1.0 `GET` forwarding
- per-connection detached threads
- a process-wide mutex-protected LRU cache
- canonical proxy header rewriting

## Commands

```bash
cd c
make clean && make test
```
