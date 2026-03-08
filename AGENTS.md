# AGENTS.md

## Mission

This repository is a study-first project, not a deployable product and not an answer book.
When you work on a legacy-style tree here, your job is to turn it into a clean learning
archive with runnable code, explicit reasoning, and stable navigation.

This file is intended to be self-sufficient.
If a file like `docs/legacy-study-rebuild-plan.md` exists, treat it as supplemental context,
not as a required dependency for understanding how to work.

## Working Assumptions

- In this repository, `legacy/` is the old source tree and must be treated as read-only
  reference material.
- `study/` is the active migration workspace. New structure and content should be created
  there.
- Both `legacy/` and `study/` are intended to live at the repository root and be uploaded to
  GitHub.
- Do not assume existing metadata is trustworthy. Validate references, commands, and
  repository state.
- Keep the repository understandable without private notes.
- Preserve original problem material separately from your own solutions and commentary.

## Repository Layout

Use this root-level meaning consistently:

- `legacy/`: frozen reference tree
- `study/`: active migration and study tree
- `docs/`: repository-wide migration rules and shared guidance

Do not repurpose `legacy/` into the new structure. The point is to preserve the old tree as a
reference artifact while building the new one separately.

## Core Goals

For every migrated project, make these boundaries obvious:

- what the problem is
- what files were provided
- what code is your solution
- how to build and test it
- what was learned
- which notes are private and local-only

At the repository level, also make these things explicit:

- what the original `legacy/` tree was trying to study
- whether the existing project set is sufficient for that learning goal
- which projects are missing, redundant, too narrow, or poorly sequenced
- why the `study/` project list is the right curriculum shape

## Good Study Repository Test

A good study repository should let another reader answer these questions quickly:

1. What was the problem?
2. How were the constraints interpreted?
3. What approaches were tried and rejected?
4. What code currently works?
5. How do I rebuild and retest it?
6. What concept was actually learned?

If the repository instead feels like an answer booklet, a raw file dump, or a pile of
personal scraps, the structure is wrong.

## Curriculum Interpretation

Do not treat `legacy/` as a perfect project plan.

Before migrating a family of projects, infer the intended learning program from:

- referenced books or courses
- project names and ordering
- existing docs and roadmaps
- recurring concepts in the notes and solutions
- missing but obviously implied topics

Write or preserve enough summary so that another agent can answer:

- what subjects this repository is trying to learn
- what the main reference materials are
- which concepts each project is supposed to teach
- what order makes pedagogical sense

## Project-Set Audit

For each track or book-driven cluster, evaluate whether the project list is actually good
enough for project-led learning.

Check for:

- coverage gaps
- duplicated projects with little added learning value
- projects that are too small to justify their own slot
- projects that are too broad and should be split
- poor ordering dependencies
- missing bridge projects between theory-heavy and implementation-heavy topics

If the legacy project set is weak, say so plainly and improve it in `study/`.

## Authority To Redesign

`legacy/` is a reference source, not a design constraint.

You may do any of the following in `study/` when it improves the learning program:

- add a brand new project not present in `legacy/`
- split one legacy project into multiple clearer projects
- merge several weak legacy projects into one stronger project
- reorder projects
- rename projects for clarity
- replace a poor project with a better one that teaches the same target concepts

Do this only when you can explain the pedagogical reason clearly.

When adding a new project, document:

- which gap it fills
- which concepts or chapters it covers
- why the legacy set was insufficient without it
- where it belongs in the learning sequence

## Required Project Shape

Unless the user explicitly asks for a different structure, use this layout:

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

Interpretation:

- `README.md`: concise public index
- `problem/`: provided specification, fixtures, scripts, starter code
- `<implementation-*>/`: one or more language- or stack-specific solution directories
- `docs/`: durable tracked notes and references
- `notion/`: private upload-ready Markdown, ignored by git

Directory roles:

- `problem/`: original statement, provided starter code, fixtures, grading scripts
- `<implementation-*>/`: active implementation paths such as `c/`, `cpp/`, `python/`,
  `java/`, `go/`, `rust/`, `node/`, `react/`, or other topic-appropriate stacks
- `docs/`: short, durable, repository-native knowledge
- `notion/`: private, process-heavy, upload-ready technical writing

If the source material belongs to another stack or language family, preserve the same
separation of concerns even if directory names differ.

## Public vs Private Content

Tracked files should contain:

- short project summary
- constraints and scope
- build and test commands
- implementation status
- compact concept notes that remain useful in-repo

Private `notion/` files should contain:

- process logs
- failed attempts
- retrospective writing
- reusable knowledge summaries
- personal confusion notes

Do not make tracked files depend on `notion/` existing.

Tracked files should feel like a stable index.
Private `notion/` files should feel like a technical notebook.

## Language And Stack Policy

Do not assume C/C++ by default across all legacy trees.

Choose implementation language or stack based on:

- the learning goal
- the subject domain
- the reference books or courses
- the kind of project being built
- explicit user preference

Rules:

- use one or more implementation directories named after the chosen language or stack
- if multiple implementations exist, they should target the same problem scope unless
  intentionally documented otherwise
- if one implementation is incomplete, mark status explicitly
- document build and test commands per implementation
- keep shared fixtures in neutral locations
- explain intentional design differences between implementations

Repository-specific override is allowed.
For example, a systems repository may prefer `c/` and `cpp/`, while an algorithms repository
may prefer `python/` plus `cpp/`, and a frontend repository may use `ts/` or `react/`.

Minimum per-implementation README contents:

- problem scope covered
- build command
- test command
- current status
- known gaps
- implementation notes

## Notion Rules

The `notion/` folder is local-only and should be directly usable in Notion.

Minimum expected files:

- `00-problem-framing.md`
- `01-approach-log.md`
- `02-debug-log.md`
- `03-retrospective.md`
- `04-knowledge-index.md`

Quality requirements:

- complete technical sentences
- explicit evidence and uncertainty
- no fake git metadata
- useful after the implementation details are forgotten

Expected content categories:

- problem framing
- approach and decision log
- debugging and failed cases
- retrospective
- reusable knowledge index

Recommended meaning of each file:

- `00-problem-framing.md`: problem statement, constraints, success criteria, prerequisites
- `01-approach-log.md`: options considered, chosen direction, decision reasons
- `02-debug-log.md`: failures, root causes, fixes, verification
- `03-retrospective.md`: what improved, what remains weak, what to revisit
- `04-knowledge-index.md`: reusable concepts, glossary, annotated reference links

When saving reference links in `notion/`, record at least:

- title
- URL or local path
- checked date
- why it was consulted
- what was learned
- how it affected the current project

Avoid these `notion/` anti-patterns:

- full code dumps without commentary
- meaningless chronological logs
- bare link collections
- copied AI output without verification
- fabricated branch, commit, or environment metadata

## Migration Workflow

Follow this order:

1. inspect `legacy/` and identify the source project or topic cluster
2. infer what the cluster was meant to teach
3. audit whether the current project set is sufficient
4. classify files as `problem`, `solution`, `docs`, `notes`, `generated`, or `unknown`
5. remove or ignore generated noise before expanding the structure
6. create or update the target project under `study/`
7. add, split, merge, or reorder projects when the curriculum needs it
8. migrate one pilot project end to end
9. reuse the pilot pattern for the rest of the tree
10. verify links, commands, and tests after each migration

Do not rewrite every project at once without a pilot.

Default pilot order for this repository:

1. `study/Foundations-CSAPP/datalab`
2. `study/Foundations-CSAPP/bomblab`
3. `study/Foundations-CSAPP/attacklab`
4. `study/Foundations-CSAPP/archlab`
5. `study/Foundations-CSAPP/perflab`
6. `study/Systems-Programming/shlab`
7. `study/Systems-Programming/malloclab`
8. `study/Systems-Programming/proxylab`

Recommended execution phases:

1. Freeze and audit
2. Establish templates
3. Migrate one pilot project
4. Roll out by family
5. Clean and normalize

Phase goals:

- Freeze and audit:
  - inventory projects and classify files
  - record broken links and duplicates
  - infer the learning goals of each track
  - audit project sufficiency
- Establish templates:
  - lock the per-project layout
  - lock the `notion/` file set
  - lock per-language README expectations
  - add ignore rules early
- Migrate one pilot project:
  - copy only required source material from `legacy/`
  - create the normalized `study/` project
  - verify builds and tests
- Roll out by family:
  - reuse the pilot pattern
  - redesign the project set where needed
- Clean and normalize:
  - remove stale generated files
  - fix references
  - unify README tone
  - make missing parity explicit

Recommended first move in a new repository:

1. add ignore rules
2. define the project template
3. migrate one pilot project
4. review the template after one full migration
5. scale to the rest of the tree

## Planning Checklist

Before migrating a project, confirm these decisions:

- naming rules and casing
- completion states such as `planned`, `in-progress`, `verified`, `archived`
- provenance rules for original vs user-authored content
- verification scope: compile, tests, benchmark, sanitizer, debugger
- spoiler policy for public tracked files
- ignore rules for private notes and build artifacts
- definition of done for the migrated project

Before migrating a track, also confirm:

- main books, papers, or courses being learned
- concept-to-project mapping
- whether the existing sequence teaches the material in the right order
- which missing projects should be added to `study/`
- which legacy projects should not be carried forward as-is

## Evidence Standard

When you keep or write technical claims:

- tie commands to real files in the repository
- prefer reproducible commands over narrative claims
- flag unknowns instead of inventing them
- remove or fix broken links
- do not reference files that do not exist

## Noise To Remove Or Ignore

Treat these as noise unless there is a strong reason to vendor them:

- object files and compiled binaries
- debug symbol bundles
- editor files
- local scratch notes
- generated test outputs
- temporary benchmark artifacts

If they must remain locally, keep them ignored and out of the conceptual structure.

## Non-Goals

Do not optimize for:

- portfolio presentation first
- exposing final answers as the primary interface
- long duplicate explanations across many files
- invented commit history or fabricated workflow metadata

## Done Criteria

A migrated project is complete when:

- `README.md` is enough to understand the project
- `problem/` is clearly separated from user-authored work
- implementation directories are present or explicitly staged
- validation commands are documented
- `docs/` is concise and durable
- `notion/` is created locally and ignored
- generated artifacts are no longer treated as source content

A migrated track is complete when:

- the intended learning goals are explicit
- the project set has been audited for sufficiency
- missing projects have been added where necessary
- redundant or weak projects have been removed, merged, or reframed
- the sequence of projects now supports the reference materials well

## If You Apply This To Another Legacy Tree

Keep the same workflow, but parameterize these items per repository:

- target languages or stacks
- reference books or courses
- project naming rules
- spoiler policy
- verification tools
- privacy rules for local notes
- curriculum design standards for project selection

Do not assume the content domain is the same as CS:APP. Reuse the structure, not the topic.

## Repository-Specific Constraint

In this repository, do not modify files under `legacy/` unless the user explicitly asks for
changes there. Use it only as a source to reference, compare, or copy from.
