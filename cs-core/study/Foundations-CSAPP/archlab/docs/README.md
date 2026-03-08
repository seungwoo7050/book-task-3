# Architecture Lab Docs

## Purpose

This folder keeps the public explanation for the migrated Architecture Lab project.

It explains how the lab splits into three different kinds of work and how the restored official
toolchain and companion model fit together.

## Document Map

- [`concepts/part-split.md`](concepts/part-split.md): how Parts A, B, and C map into the study migration
- [`concepts/iaddq-and-control-signals.md`](concepts/iaddq-and-control-signals.md): why one instruction touches multiple control paths
- [`concepts/pipeline-cost-model.md`](concepts/pipeline-cost-model.md): how the companion project models Part C performance reasoning
- [`references/verification.md`](references/verification.md): commands and current results for both the restored official toolchain and the companion tracks

## Disclosure Boundary

- publish only the self-written boundary files under `problem/`
- publish study-owned companion models and tests
- keep restored official handouts local-only under ignored paths
