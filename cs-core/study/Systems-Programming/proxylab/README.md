# Proxy Lab

## Purpose

This is the active study-first migration of the web proxy lab.

The frozen reference tree lives in
[`/Users/woopinbell/work/cs-core/legacy/Systems-Programming/proxylab`](/Users/woopinbell/work/cs-core/legacy/Systems-Programming/proxylab).
This project separates:

- the starter proxy contract and shared CS:APP helpers in `problem/`
- fresh proxy implementations in `c/` and `cpp/`
- public explanations and verification records in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | migrated safely | starter proxy, shared helpers, and reusable driver wrapper |
| `c/` | verified | GET-only concurrent proxy with in-memory LRU cache |
| `cpp/` | verified | same proxy contract implemented in C++ |
| `docs/` | complete | HTTP forwarding, concurrency, caching, and verification policy documented |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## Learning Goals

This project is designed around three milestones:

1. sequential forwarding of HTTP/1.0 `GET`
2. per-connection threading and process robustness
3. object caching with a thread-safe LRU policy

The `study/` version keeps those milestones explicit and verifies them with a local origin server
that can expose header rewriting, concurrent requests, and cache hits.

## Structure

```text
proxylab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  tests/
```

## Verification Path

For the starter contract:

```bash
cd problem
make clean && make
```

For the C track:

```bash
cd c
make clean && make test
```

For the C++ track:

```bash
cd cpp
make clean && make test
```
