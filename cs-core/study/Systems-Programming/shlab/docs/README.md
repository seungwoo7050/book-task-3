# Shell Lab Docs

## Purpose

This folder keeps the public explanation for the migrated tiny shell project.

It explains:

- how job control depends on process groups
- where the shell-race hazards come from
- how the study tracks verify more than just "the shell did not crash"

## Document Map

- [`concepts/signal-and-race-discipline.md`](concepts/signal-and-race-discipline.md): `fork`, `SIGCHLD`, and why masking matters
- [`concepts/job-control-flow.md`](concepts/job-control-flow.md): how `fg`, `bg`, and foreground signal forwarding fit together
- [`references/verification.md`](references/verification.md): starter build path, trace coverage, and custom signal traces
