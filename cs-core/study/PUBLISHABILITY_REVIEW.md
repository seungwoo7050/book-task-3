# Study Publishability Review

## Purpose

This document records the repository-wide publication review for `study/`.

It separates:

- repository-owned implementations, docs, tests, and Notion-ready writing that are safe to publish
- public `problem/` boundaries that were rewritten or reduced to study-owned starter assets
- official binaries or toolchains that must remain local-only

## Executive Summary

The `study/` migration is complete as a learning workspace, the strict public-release cleanup is
complete, and the official self-study verification paths are now reproducible locally.

Current publication rule:

- `c/`, `cpp/`, `docs/`, `tests/`, and the contents of `notion/` are study-owned and publishable
- `problem/` directories now contain either self-written contract summaries or study-owned starter assets
- official supplied binaries and missing course toolchains remain outside committed Git history

## Project Review

### `Foundations-CSAPP/datalab`

- publishable material:
  - self-written `problem/` specification and starter files
  - fresh C/C++ tracks, docs, and Notion notes
- local-only gap:
  - the restored official handout is placed under ignored `problem/official/`
- judgment:
  - publishable in its current repository form and locally verifiable with official `dlc`

### `Foundations-CSAPP/bomblab`

- publishable material:
  - self-written contract summary, mini-bomb skeleton, solution template, and helper script
  - fresh companion implementations, docs, and Notion notes
- local-only gap:
  - the restored public self-study bomb is kept under ignored `problem/official/`
- judgment:
  - publishable in its current repository form and locally verifiable against the public self-study bomb

### `Foundations-CSAPP/attacklab`

- publishable material:
  - self-written problem contract
  - study-owned companion verifier implementations and payload samples
  - public gadget-farm boundary without any committed target-specific cookie file
- local-only gap:
  - the restored public self-study target set is kept under ignored `problem/official/`
- judgment:
  - publishable in its current repository form and locally verifiable against the public self-study target set

### `Foundations-CSAPP/archlab`

- publishable material:
  - self-written contract-only `problem/` boundary
  - fresh companion models, docs, and Notion notes
- local-only gap:
  - the restored official Y86/HCL toolchain is kept under ignored `problem/official/`
- judgment:
  - publishable in its current repository form and locally verifiable against the official self-study toolchain

### `Foundations-CSAPP/perflab`

- publishable material:
  - self-written starter boundary
  - study-owned `study.trace`
  - fresh implementations, docs, and Notion notes
- local-only gap:
  - none required for repository publication
- judgment:
  - publishable in its current repository form

### `Systems-Programming/shlab`

- publishable material:
  - self-written contract-only `problem/` boundary
  - fresh shells, direct signal harness, docs, and Notion notes
- local-only gap:
  - none required for repository publication
- judgment:
  - publishable in its current repository form

### `Systems-Programming/malloclab`

- publishable material:
  - self-written allocator contract, `memlib`, traces, and trace driver
  - fresh allocators, docs, and Notion notes
- local-only gap:
  - none required for repository publication
- judgment:
  - publishable in its current repository form

### `Systems-Programming/proxylab`

- publishable material:
  - self-written proxy starter boundary and shared socket helpers
  - fresh proxies, local origin harness, docs, tests, and Notion notes
- local-only gap:
  - none required for repository publication
- judgment:
  - publishable in its current repository form

## Repository-Level Decision

For this repository, the publication rule is now:

1. Publish all study-owned implementations, docs, tests, and Notion-derived writing freely.
2. Keep official supplied binaries and missing course toolchains local-only.
3. Restore official self-study assets only into ignored local directories.

## Safest Public Shape

The current remote-safe shape is:

- keep:
  - `problem/` only when it is a self-written contract summary or study-owned starter boundary
  - `c/`
  - `cpp/`
  - `docs/`
  - `tests/`
  - `notion/` content for local upload workflows
  - project and study-level `README.md`
- continue to exclude:
  - official supplied binaries
  - target-specific local cookies
  - restored local simulator/toolchain assets

## Current Conclusion

The `study/` tree is complete as a project-led learning workspace and publishable as a remote
repository in its current form.

Official self-study validation is now complete for the current CS:APP projects, while the restored
handouts and binaries remain outside committed history under ignored local paths.
