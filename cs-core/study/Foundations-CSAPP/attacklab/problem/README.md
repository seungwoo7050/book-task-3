# Attack Lab - Problem Contract

## Summary

The original Attack Lab asks you to craft exploit strings for two vulnerable programs:

- `ctarget` for code injection
- `rtarget` for ROP under stronger defenses

This `problem/` directory preserves that contract while restoring the public CMU self-study target
set locally on demand under `official/`.

## What Is Included

| Path | Purpose |
|---|---|
| `README.md` | official problem boundary and local setup instructions |
| `Makefile` | restore, disassembly, and Docker verification helpers |
| `code/README.md` | notes about locally restoring target-specific cookies and binaries |
| `code/farm.c` | reference gadget-farm source |
| `data/phase*.txt` | verified exploit strings for the public `target1` self-study instance |
| `script/run_attack.sh` | helper script for local phase runs |

## Local Official Restore

```bash
cd problem
make restore-official
make verify-official
```

The restore target downloads the public `target1` self-study handout from the official CS:APP
site into the ignored local directory `problem/official/`.

## Official Learning Goal

Attack Lab is about:

- understanding stack layout and control-flow hijacking
- constructing code-injection payloads
- understanding why W^X and ASLR change the attack surface
- building ROP chains from constrained gadgets

## Publication Rule

- keep restored official binaries out of version control
- do not publish raw exploit strings for a supplied private course target
- keep public material focused on workflow, models, and safety boundaries
