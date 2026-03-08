# study

This directory is the active project-led learning workspace.

## Mission

The goal of `study/` is not to mirror `legacy/` mechanically.
The goal is to build the right set of projects for learning the target books through
implementation.

## Source Of Truth

- `../legacy/` is the frozen reference tree.
- `study/` is the actively designed learning tree.
- If `legacy/` is weak as a curriculum, `study/` should improve it.

## Main References

Current inference from the legacy material:

- `Computer Systems: A Programmer's Perspective (CS:APP)`
- `Operating Systems: Three Easy Pieces (OSTEP)`

Potential future expansion already hinted by the legacy tree:

- `xv6`

## What This Repository Is Trying To Learn

Based on the current legacy roadmap, this repository is trying to learn:

- data representation and bit-level reasoning
- assembly and reverse engineering
- exploit mechanics and low-level security intuition
- processor design and performance
- process control, signals, memory allocation, and network programming
- later, operating-system internals through xv6-style projects

## Curriculum Rule

Project-led learning succeeds only if the project set is well designed.

So every time a track is migrated into `study/`, we must ask:

1. What concepts are supposed to be learned?
2. Which projects teach them best?
3. Is the legacy project set sufficient?
4. Which projects should be added, removed, split, merged, or reordered?

`study/` is allowed to diverge from `legacy/` when that produces a better learning path.

## Current Working Judgment

Preliminary judgment from `legacy/README.md`:

- The CS:APP Phase 1 and Phase 2 project list is a strong starting backbone.
- The OSTEP and xv6 expansion is still only partially represented.
- New projects may need to be designed later to bridge missing operating-systems topics.

This judgment should be refined as each track is audited in detail.

## Expected Project Shape

Each project in `study/` should contain:

- `problem/`
- `c/`
- `cpp/`
- `docs/`
- `notion/`

## Current Language Preference

For the current `cs-core` systems-oriented curriculum, the default implementation preference is:

- `c/`
- `cpp/`

This is a repository-specific choice, not a universal rule for all legacy migrations.
If a future track in this repository clearly calls for a different language or stack, that can
be changed when the pedagogical reason is explicit.

## Notion Rule

Each project's `notion/` directory should be good enough to move into Notion as-is.

It should contain:

- problem framing
- approach and decision log
- debug log
- retrospective
- knowledge index with annotated reference links

## Current Order

Default migration order:

1. `Foundations-CSAPP/datalab`
2. `Foundations-CSAPP/bomblab`
3. `Foundations-CSAPP/attacklab`
4. `Foundations-CSAPP/archlab`
5. `Foundations-CSAPP/perflab`
6. `Systems-Programming/shlab`
7. `Systems-Programming/malloclab`
8. `Systems-Programming/proxylab`

This order can change if the curriculum audit shows a better dependency order.

## Completed So Far

- [`Foundations-CSAPP/datalab`](/Users/woopinbell/work/cs-core/study/Foundations-CSAPP/datalab)
- [`Foundations-CSAPP/bomblab`](/Users/woopinbell/work/cs-core/study/Foundations-CSAPP/bomblab)
- [`Foundations-CSAPP/attacklab`](/Users/woopinbell/work/cs-core/study/Foundations-CSAPP/attacklab)
- [`Foundations-CSAPP/archlab`](/Users/woopinbell/work/cs-core/study/Foundations-CSAPP/archlab)
- [`Foundations-CSAPP/perflab`](/Users/woopinbell/work/cs-core/study/Foundations-CSAPP/perflab)
- [`Systems-Programming/shlab`](/Users/woopinbell/work/cs-core/study/Systems-Programming/shlab)
- [`Systems-Programming/malloclab`](/Users/woopinbell/work/cs-core/study/Systems-Programming/malloclab)
- [`Systems-Programming/proxylab`](/Users/woopinbell/work/cs-core/study/Systems-Programming/proxylab)

## Current Next Project

- migration pass is complete
- upload-ready `notion/` authoring is complete
- strict public-release cleanup of `problem/` assets is complete
- official self-study asset restoration and Docker-based validation are complete for all current
  CS:APP projects

## Master Tracker

Use the repository-wide execution board here:

- [`TODO.md`](/Users/woopinbell/work/cs-core/study/TODO.md)
- [`PUBLISHABILITY_REVIEW.md`](/Users/woopinbell/work/cs-core/study/PUBLISHABILITY_REVIEW.md)
