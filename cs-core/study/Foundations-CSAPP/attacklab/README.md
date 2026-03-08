# Attack Lab

## Purpose

This is the active study-first migration of CS:APP Attack Lab.

The frozen reference tree lives in [`/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/attacklab`](/Users/woopinbell/work/cs-core/legacy/Foundations-CSAPP/attacklab).
This directory separates:

- the official problem contract in `problem/`
- fresh study-owned companion verifiers in `c/` and `cpp/`
- durable public explanations in `docs/`

## Status

| Area | Status | Notes |
|---|---|---|
| `problem/` | verified | public self-study target set is restored locally on demand and all five official phases pass in Docker |
| `c/` | verified | fresh payload-layout verifier implemented and tested |
| `cpp/` | verified | same companion contract implemented and tested |
| `docs/` | complete | disclosure policy, attack models, and verification notes written |
| `notion/` | complete | upload-ready local notes written for the migrated project |

## Project Strategy

The original lab depends on external binaries (`ctarget`, `rtarget`, `hex2raw`) that are not
present in `legacy/` and should not be blindly redistributed here.

So this migration uses two layers:

- `problem/` keeps the official contract and the external-asset boundary.
- `c/` and `cpp/` implement a companion verifier that checks hex payloads against concept-preserving
  models for:
  - return-address overwrite
  - code injection layout
  - cookie-string placement
  - simple ROP chain construction
  - runtime-relative string addressing

## Structure

```text
attacklab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
```

## Verification Path

For the official problem track:

```bash
cd problem
make restore-official
make verify-official
```

For the C companion track:

```bash
cd c
make clean && make test
```

For the C++ companion track:

```bash
cd cpp
make clean && make test
```

The restored official targets live under the ignored local directory `problem/official/`.
