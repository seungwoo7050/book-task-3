# Study Master TODO

## Purpose

This file is the execution board for finishing the `study/` tree.

It tracks:

- which projects exist in `legacy/`
- which projects have been migrated into `study/`
- what "done" means for each project
- the next highest-value action for each unfinished project

## Current Execution Rule

- The project-by-project implementation migration is complete.
- Upload-ready `notion/` authoring is complete for all current projects.
- Official self-study asset restoration and Docker-based validation are complete for the current
  CS:APP gap projects.

## Project Completion Standard

A project is complete only when all of these are true:

- [ ] `problem/` is migrated and stripped of accidental build artifacts
- [ ] C track is implemented fresh in `study/`
- [ ] C track verification is documented and passing
- [ ] C++ track is implemented fresh in `study/`
- [ ] C++ track verification is documented and passing
- [ ] `docs/` explains core reasoning and edge cases without becoming a code dump
- [ ] `notion/` is filled with upload-ready documentation
- [ ] publishability risks are reviewed

## Global Blockers

- [x] Review whether redistributed lab assets inside `study/problem/` are safe to publish remotely
- [x] Decide whether `dlc` should be restored, replaced, or permanently documented as unavailable
- [x] Keep `study/README.md` in sync with actual project status
- [x] If strict public redistribution safety is required, replace or rewrite the copied starter assets listed in `PUBLISHABILITY_REVIEW.md`

## Current Status Board

| Order | Track | Project | Status | Next Action |
|---|---|---|---|---|
| 1 | Foundations-CSAPP | `datalab` | complete, publishable, and verified against the official self-study handout | no required follow-up |
| 2 | Foundations-CSAPP | `bomblab` | complete, publishable, and verified against the public self-study bomb | no required follow-up |
| 3 | Foundations-CSAPP | `attacklab` | complete, publishable, and verified against the public self-study target set | no required follow-up |
| 4 | Foundations-CSAPP | `archlab` | complete, publishable, and verified against the restored official Y86/HCL toolchain | no required follow-up |
| 5 | Foundations-CSAPP | `perflab` | complete and publishable | no required follow-up |
| 6 | Systems-Programming | `shlab` | complete and publishable | no required follow-up |
| 7 | Systems-Programming | `malloclab` | complete and publishable | no required follow-up |
| 8 | Systems-Programming | `proxylab` | complete and publishable | no required follow-up |

## Per-Project TODO

### 1. `datalab`

- [x] Migrate `problem/`
- [x] Fresh C implementation
- [x] Fresh C++ implementation
- [x] Public docs
- [x] Notion docs
- [x] C verification
- [x] C++ verification
- [x] Publishability review
- [x] Decide whether to restore `dlc`
- [x] Restore the official self-study handout and run official `dlc` + `btest`

### 2. `bomblab`

- [x] Audit what the project is supposed to teach in `study/`
- [x] Review binary redistribution and answer-spoiler risks
- [x] Scaffold `study/Foundations-CSAPP/bomblab`
- [x] Migrate problem contract safely
- [x] Define C track expectations
- [x] Define C++ track expectations
- [x] Write public docs policy for reverse-engineering disclosures
- [x] Write upload-ready `notion/`
- [x] Define verification flow
- [x] Restore the public self-study bomb and verify the official problem track in Docker

### 3. `attacklab`

- [x] Audit intended learning goals
- [x] Review exploit-material publication risk
- [x] Scaffold `study/Foundations-CSAPP/attacklab`
- [x] Migrate problem contract safely
- [x] Define C and C++ deliverables
- [x] Write public docs policy for exploit logic disclosure
- [x] Write upload-ready `notion/`
- [x] Define verification flow
- [x] Restore the public `target1` self-study handout and verify all five official phases in Docker

### 4. `archlab`

- [x] Audit intended learning goals
- [x] Split Part A/B/C into explicit `study/` milestones
- [x] Scaffold `study/Foundations-CSAPP/archlab`
- [x] Migrate problem contract safely
- [x] Define C and C++ implementation boundaries
- [x] Write public docs
- [x] Write upload-ready `notion/`
- [x] Define verification flow
- [x] Restore the public self-study handout, rebuild the Y86/HCL toolchain, and verify Parts A/B/C in Docker

### 5. `perflab`

- [x] Audit intended learning goals
- [x] Decide benchmark and comparison policy
- [x] Scaffold `study/Foundations-CSAPP/perflab`
- [x] Migrate problem contract safely
- [x] Implement fresh C track
- [x] Implement fresh C++ track
- [x] Document performance methodology in `docs/`
- [x] Write upload-ready `notion/`
- [x] Verify correctness and performance

### 6. `shlab`

- [x] Audit intended learning goals
- [x] Define shell milestone sequence
- [x] Scaffold `study/Systems-Programming/shlab`
- [x] Migrate problem contract safely
- [x] Implement fresh C track
- [x] Implement fresh C++ track
- [x] Document signal/race-condition reasoning
- [x] Write upload-ready `notion/`
- [x] Verify traces and edge cases

### 7. `malloclab`

- [x] Audit intended learning goals
- [x] Define allocator milestone sequence
- [x] Scaffold `study/Systems-Programming/malloclab`
- [x] Migrate problem contract safely
- [x] Implement fresh C track
- [x] Implement fresh C++ track
- [x] Document allocator invariants and tradeoffs
- [x] Write upload-ready `notion/`
- [x] Verify correctness and allocator behavior

### 8. `proxylab`

- [x] Audit intended learning goals
- [x] Split into sequential, concurrent, and caching milestones
- [x] Scaffold `study/Systems-Programming/proxylab`
- [x] Migrate problem contract safely
- [x] Implement fresh C track
- [x] Implement fresh C++ track
- [x] Document concurrency and cache design
- [x] Write upload-ready `notion/`
- [x] Verify functional and concurrency behavior

## Future Expansion Backlog

These are not current `legacy/` projects, but they are implied by the repository learning goals.

- [ ] Decide whether xv6 should become a new `study/` track after the current legacy set is migrated
- [ ] If yes, define the first xv6 milestone set before implementation starts
