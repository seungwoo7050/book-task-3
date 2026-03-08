# Legacy Audit

## Baseline

- Audit date: 2026-03-07
- Legacy core problems discovered: 42
- Legacy `problem` test status: 42/42 `make test` passed
- Repository git status: not a git repository
- Broken internal Markdown links caused by missing `RULEBOOK.md`: 44
- Metrics artifact present: `legacy/core/.devlog_test_metrics.json`
- Manifest snapshot: `docs/legacy-file-manifest.txt`

## What Was Accepted As Source Material

- `legacy/core/*/*/problem`: original statements, starter code, fixtures, scripts
- `legacy/core/*/*/solve/solution/*`: user-authored solutions
- `legacy/core/*/*/docs/*`: public study notes
- `legacy/core/*/*/devlog/*`, `lab-report.md`: private/process-heavy notes to be reclassified into `study/**/notion/`

## What Was Not Carried Forward Verbatim

- Broken `RULEBOOK.md` references
- `algorithm-clrs/advanced/` and `common-docs/` ghost paths mentioned only in legacy docs
- fabricated git metadata inside legacy devlogs
- standalone metrics blobs copied into prose

## Migration Decisions

- Preserve all 42 core problems.
- Add one bridge project for BOJ 1717 (union-find) before the MST/topological-sort capstone track.
- Retain C++ only for all legacy gold problems plus BOJ 1753 and 1197.
