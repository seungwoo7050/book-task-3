# Shell Lab - Problem Contract

## Summary

The original Shell Lab asks you to build a tiny Unix shell with job control.

This `problem/` directory now preserves only a self-written contract summary.
For strict public release, the copied starter shell, official traces, and bundled driver have been
removed. The active implementations and self-owned tests live in `../c/`, `../cpp/`, and `../tests/`.

## What Is Included

| Path | Purpose |
|---|---|
| `README.md` | shell-lab contract summary |
| `Makefile` | status target explaining the public-release boundary |
| `code/README.md` | notes about the removed starter shell assets |
| `data/README.md` | notes about the removed starter traces |
| `script/README.md` | notes about the removed starter driver |

## What Is Not Included

- copied starter shell sources
- official trace files
- the bundled Perl driver

## Public-Release Rule

The public repository keeps the learning contract here, but the actual runnable verification path is
study-owned and lives outside `problem/`.

## Official Learning Goal

Shell Lab is about:

- process groups and job control
- correct `SIGCHLD` reaping
- forwarding interactive signals to the foreground job
- avoiding races between `fork`, signal delivery, and job-list updates
