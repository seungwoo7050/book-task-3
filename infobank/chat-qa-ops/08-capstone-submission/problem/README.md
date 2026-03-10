# 08 capstone 문제 정의

v0 runnable snapshot, v1 hardening, v2 improvement proof를 묶은 최종 QA Ops capstone 아카이브다.

## capstone이 답해야 할 질문

상담 품질 관리 플랫폼을 runnable demo, regression hardening, improvement proof까지 포함한 제출물로 어떻게 마감할 것인가?

## 입력

- 00~07 stage에서 분리해 고정한 source brief, rubric, fixtures, guardrails, traces, compare contract, dashboard shape
- v0 baseline runnable snapshot
- v1 provider chain and lineage hardening
- v2 retrieval improvement experiment

## 기대 산출물

- `v0-initial-demo`, `v1-regression-hardening`, `v2-submission-polish` snapshot directories
- proof artifacts under `v2-submission-polish/docs/demo/proof-artifacts`
- release-readiness documents with verification commands and compare summary

## 완료 기준

- v0, v1, v2가 각자 독립적으로 runnable하고 역할이 다르다.
- compare는 같은 dataset과 run label 위에서 baseline 대비 개선을 증빙한다.
- fallback, dependency health, dashboard, proof artifact가 공개 저장소 기준으로 재현 가능하다.

## 이번 capstone에서 바로 확인할 범위

- `v0-initial-demo`: 최초 runnable baseline과 SQLite 중심 local proof
- `v1-regression-hardening`: provider fallback, lineage, PostgreSQL smoke, version compare 강화
- `v2-submission-polish`: 개선 증빙, compare artifact, 발표/제출 runbook 마감
- `v3-self-hosted-oss`: self-hosted 운영을 위한 compose, Docker, OSS hardening 확장
