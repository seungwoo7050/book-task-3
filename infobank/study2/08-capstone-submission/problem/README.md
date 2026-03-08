# Capstone Problem

v0 runnable snapshot, v1 hardening, v2 improvement proof를 묶은 최종 QA Ops capstone 아카이브다.

## Stage Question

상담 품질 관리 플랫폼을 runnable demo, regression hardening, improvement proof까지 포함한 제출물로 어떻게 마감할 것인가?

## Inputs

- 00~07 stage에서 분리해 고정한 source brief, rubric, fixtures, guardrails, traces, compare contract, dashboard shape
- v0 baseline runnable snapshot
- v1 provider chain and lineage hardening
- v2 retrieval improvement experiment

## Required Output

- `v0-initial-demo`, `v1-regression-hardening`, `v2-submission-polish` snapshot directories
- proof artifacts under `v2-submission-polish/docs/demo/proof-artifacts`
- release-readiness documents with verification commands and compare summary

## Success Criteria

- v0, v1, v2가 각자 독립적으로 runnable하고 역할이 다르다.
- compare는 같은 dataset과 run label 위에서 baseline 대비 개선을 증빙한다.
- fallback, dependency health, dashboard, proof artifact가 공개 저장소 기준으로 재현 가능하다.
