# Shell Lab

## Purpose

This is the active study-first migration of the tiny shell lab.

The frozen reference tree lives in [`/Users/woopinbell/work/cs-core/legacy/Systems-Programming/shlab`](/Users/woopinbell/work/cs-core/legacy/Systems-Programming/shlab).
This directory separates:

- the official starter and trace boundary in `problem/`
- fresh shell implementations in `c/` and `cpp/`
- durable public explanations in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | publishable | self-written contract-only boundary; copied starter shell, traces, and driver removed |
| `c/` | verified | fresh tiny shell implementation and direct signal-aware tests completed |
| `cpp/` | verified | same shell contract implemented in C++ and direct signal-aware tests completed |
| `docs/` | complete | signal, race, and verification policy documented |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## Project Strategy

This migration keeps `shlab` as a real shell project rather than downgrading it to a companion-only
model. The public tree no longer redistributes the copied starter shell or official traces, but the
active tracks still implement the original job-control contract directly.

Both implementation tracks support:

- foreground and background jobs
- built-ins: `quit`, `jobs`, `bg`, `fg`
- forwarding `SIGINT` and `SIGTSTP` to the foreground job's process group
- reaping children with `SIGCHLD`
- blocking `SIGCHLD` around `fork`/`addjob` to avoid race conditions

## Structure

```text
shlab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
```

## Verification Path

For the public problem boundary:

```bash
cd problem
make status
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
