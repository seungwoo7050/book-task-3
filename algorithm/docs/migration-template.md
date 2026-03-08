# Migration Template

## Required Project Shape

```text
study/
  <track>/
    <boj>/
      README.md
      problem/
        README.md
        Makefile
        code/
        data/
        script/
      python/
        README.md
        src/
        tests/
      cpp/                  # optional
        README.md
        src/
        include/
        tests/
      docs/
        README.md
        concepts/
        references/
      notion/               # local-only, ignored
        00-problem-framing.md
        01-approach-log.md
        02-debug-log.md
        03-retrospective.md
        04-knowledge-index.md
```

## Rules

- `problem/` keeps only original or explicitly study-authored problem material and fixtures.
- `python/` is always present and contains the default implementation.
- `cpp/` exists only when the repository policy says to retain it.
- `docs/` is public, concise, and durable.
- `notion/` is local-only and can contain process-heavy writing.

## Done Criteria

- `README.md` alone explains the project scope and verify commands.
- `make -C problem test` passes.
- Public docs do not depend on `notion/`.
- Legacy provenance is recorded without copying broken paths or fabricated git metadata.
