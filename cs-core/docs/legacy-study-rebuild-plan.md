# Legacy Study Repository Rebuild Plan

## Purpose

This document defines how to turn a legacy-style lab archive into a study-first repository.
The goal is not to publish an answer book. The goal is to preserve problem context, record
decisions, keep runnable code, and make future review easier.

## Current Diagnosis

The current tree under `legacy/` already contains useful material, but the boundary between
"problem", "reference", "solution", "journal", and "build noise" is weak.

The repository now also has a new root-level `study/` directory. That is the active
migration workspace. `legacy/` remains a read-only reference tree and should not be edited
during routine migration work.

Observed issues in the current repository:

- The legacy reference tree originally had the typo `regacy/` and has been renamed to
  `legacy/`.
- Build artifacts and binaries are mixed into the study tree, such as `*.o`, `*.dSYM`,
  `btest`, `tsh`, `proxy`, `mdriver`, and `csim`.
- Some files behave like a workbook or answer sheet rather than a learning archive.
- Some references are broken or unverifiable, such as links to `RULEBOOK.md` that do not
  exist in this repository.
- Some devlogs include environment metadata that is not trustworthy in the current tree
  (for example branch and commit-range fields in a directory that is not currently a git
  repository).

## What A Good Study Repository Looks Like

A study repository should optimize for these questions:

1. What was the problem?
2. How did I interpret the constraints?
3. What did I try, and why did I reject some paths?
4. What code currently works?
5. How do I rebuild and retest it?
6. What concept did I actually learn from this work?

That means the repository should feel like a technical notebook with runnable code, not like
an exam-prep booklet or a polished answer dump.

## Design Principles

- Keep one project per problem or lab.
- Separate original problem material from your own work.
- Separate public tracked files from private local notes.
- Keep implementation directories aligned with the chosen language or stack strategy.
- Prefer concise indexes in tracked files and deeper reflection in `notion/`.
- Keep every claim reproducible through commands, tests, or cited source files.
- Remove generated files from the source tree unless they are intentionally vendored.
- Treat the legacy tree as a reference, not as a fixed curriculum.
- Improve the project set when the legacy design is not good enough for learning goals.

## Curriculum-First Rule

In project-led learning, the hardest and most important design choice is the project set
itself.

Before migrating a track, answer these questions:

1. What is the track trying to learn?
2. Which books, courses, or references define that scope?
3. Which concepts must be learned through implementation, not just reading?
4. Does the existing legacy project list actually cover those concepts well?
5. Are there missing, redundant, or badly sequenced projects?

The `study/` tree should represent the best learning curriculum you can justify, not a
mechanical copy of `legacy/`.

## Allowed Redesign Moves

When the legacy project plan is weak, these moves are allowed in `study/`:

- add a new project
- remove a weak or redundant project
- split a project
- merge projects
- rename projects
- reorder projects

Each redesign should be justified by:

- concept coverage
- dependency order
- project size and coherence
- implementation value relative to the reference books

## Target Structure

The active target root is `study/`.

Keep `legacy/` untouched as the source reference. Build the normalized structure under
`study/`.

Recommended per-project layout:

```text
study/
  <track>/
    <project>/
      README.md
      problem/
        README.md
        code/
        data/
        script/
      <implementation-1>/
        README.md
        src/
        include/
        tests/
      <implementation-2>/
        README.md
        src/
        include/
        tests/
      docs/
        README.md
        concepts/
        references/
      notion/
        00-problem-framing.md
        01-approach-log.md
        02-debug-log.md
        03-retrospective.md
        04-knowledge-index.md
```

### Directory Roles

- `README.md`: public entry point; short and stable.
- `problem/`: original statement, provided code, fixtures, scripts, grading tools.
- `<implementation-*>/`: your language- or stack-specific solutions and tests.
- `docs/`: concise tracked notes that remain useful in the repository itself.
- `notion/`: local, private, upload-ready writing for Notion. This directory should be
  git-ignored.

## Public vs Private Writing

Use this split consistently:

- Public tracked files:
  - project summary
  - build/test instructions
  - minimal concept map
  - solution status
  - important constraints
- Private `notion/` files:
  - day-by-day logs
  - failed approaches
  - long retrospectives
  - personal confusion notes
  - interview-style concept summaries

The repository should still make sense without opening `notion/`.

## Language And Stack Policy

Every project should define the expected implementation strategy.

Recommended rules:

- Choose language or stack based on the topic, reference materials, and learning goal.
- If multiple implementations exist, they should solve the same problem scope unless the
  difference is intentionally documented.
- If only one implementation is complete, mark the others as `planned` or `in-progress`.
- Tests should verify behavior, not just compilation.
- Shared fixtures belong under `problem/` or a neutral test-data location.
- Implementation-specific rationale goes into each implementation README.
- If different implementations intentionally differ in design, explain the trade-off explicitly.

Minimum per-implementation README contents:

- problem scope covered
- build command
- test command
- current status
- known gaps
- implementation notes

## Notion Folder Standard

Each project should have a local `notion/` directory with Markdown that can be pasted or
uploaded to Notion with minimal cleanup.

Recommended file set:

- `00-problem-framing.md`
  - what the problem asks
  - constraints
  - success criteria
  - prerequisites
- `01-approach-log.md`
  - hypotheses
  - design options
  - chosen plan
  - why alternatives were rejected
- `02-debug-log.md`
  - failing cases
  - command outputs worth preserving
  - root cause notes
  - fix verification
- `03-retrospective.md`
  - what became easier after solving
  - what still feels weak
  - what to revisit later
- `04-knowledge-index.md`
  - reusable concepts
  - glossary
  - cross-links to later projects

Quality bar for `notion/` documents:

- good enough to upload as-is
- written in complete technical sentences
- explicit about evidence and uncertainty
- useful even after the code is forgotten

## What You Were Missing

These items should be decided before migration starts:

1. Naming policy
   - `legacy/` remains reference-only
   - `study/` is the active workspace
   - directory casing
   - project slug format
2. Completion states
   - `planned`, `in-progress`, `verified`, `archived`
3. Provenance policy
   - what is copied from the original lab
   - what is your own writing
4. Verification policy
   - compile only
   - tests
   - benchmark
   - sanitizer or debugger checks
5. Spoiler policy
   - how much of the final answer should be exposed in public tracked files
6. Ignore policy
   - `notion/`, binaries, object files, debug artifacts, local notes
7. Definition of done
   - what must exist before a project is considered migrated
8. Curriculum adequacy
   - whether the project set is sufficient for the intended learning goals
   - which new projects must be added to `study/`

## Migration Plan

### Phase 0: Freeze and Audit

- Inventory all projects and classify each file as `problem`, `solution`, `note`, `report`,
  `generated`, or `unknown`.
- Record broken links and duplicate documents.
- Confirm `legacy/` remains frozen and all new work happens in `study/`.
- Infer what each track was originally trying to study.
- Audit whether the current projects are sufficient for project-led learning.

### Phase 1: Establish Templates

- Create one canonical project template.
- Create one canonical `notion/` file set.
- Create one canonical per-language README template.
- Add ignore rules before local private folders spread.
- Create a curriculum-audit template for deciding whether projects should be added or changed.

### Phase 2: Pilot One Project

Use `datalab` first. It is small, conceptually dense, and already has both study notes and
verification hooks.

Pilot goals:

- copy only the required source material from `legacy/`
- rewrite project README into a study-first index
- move the first implementation into its own implementation directory
- scaffold additional implementations if the curriculum calls for them
- compress tracked docs so they are navigational, not bloated
- move reflective writing into local `notion/`
- verify build and tests

### Phase 3: Roll Out By Family

Suggested order:

1. `Foundations-CSAPP/datalab`
2. `Foundations-CSAPP/bomblab`
3. `Foundations-CSAPP/attacklab`
4. `Foundations-CSAPP/archlab`
5. `Foundations-CSAPP/perflab`
6. `Systems-Programming/shlab`
7. `Systems-Programming/malloclab`
8. `Systems-Programming/proxylab`

This order is a default, not a prison. Change it if the dependency graph or learning value
demands it.

### Phase 4: Clean and Normalize

- remove stale binaries and object files
- fix broken links
- unify README tone
- mark missing implementation parity explicitly
- make sure every project has the same top-level rhythm

## Definition Of Done

A migrated project is done when:

- its purpose is understandable from `README.md` alone
- `problem/` contains only source material and provided assets
- implementation directory roles are explicit
- tests or validation commands are documented and runnable
- `docs/` contains only durable tracked knowledge
- `notion/` exists locally and is ignored by git
- no generated artifacts are tracked by mistake
- broken references have been removed or replaced

A migrated track is done when:

- the intended learning targets are explicit
- the project set has been audited
- missing projects have been added when needed
- weak legacy projects have been reframed or dropped where appropriate
- the resulting sequence supports the reference materials better than the original tree

## Recommended First Move

Do not start by rewriting every file.

Start with this sequence:

1. add `.gitignore`
2. define the project template
3. migrate `datalab` as the pilot
4. review the template after one full migration
5. scale the pattern to the remaining labs

This keeps the redesign grounded in one real example instead of spreading guesswork across the
entire tree.
