# Proxy Lab Docs

## Purpose

This folder keeps the public explanation for the migrated proxy project.

It focuses on:

- how a proxy rewrites and forwards HTTP/1.0 requests
- where the concurrency hazards are
- how cache correctness is tested without relying on official grading servers

## Document Map

- [`concepts/http-forwarding.md`](concepts/http-forwarding.md): request parsing and outbound header normalization
- [`concepts/concurrency-and-cache.md`](concepts/concurrency-and-cache.md): detached-thread model, cache locking, and LRU behavior
- [`references/verification.md`](references/verification.md): local origin harness, cache checks, and concurrency checks
