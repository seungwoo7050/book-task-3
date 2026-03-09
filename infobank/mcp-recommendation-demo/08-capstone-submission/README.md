# 08 Capstone Submission

이 트랙은 `MCP 추천 최적화`를 운영형 시스템으로 완성하는 capstone archive다. `v0 -> v1 -> v2`는 capstone 본선이고, `v3`는 `v2`를 self-hosted OSS 후보로 확장한 productization extension이다.

## Versions

- `v0-initial-demo`: registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable demo
- `v1-ranking-hardening`: reranker, usage logs, feedback loop, baseline/candidate compare, catalog/experiment CRUD를 추가한 운영형 추천 버전
- `v2-submission-polish`: compatibility gate, release gate, submission artifact export, dry-run pipeline, release candidate CRUD를 추가한 최종 capstone demo
- `v3-oss-hardening`: auth/RBAC, single-workspace 운영 코어, background jobs, audit log, compose deployment를 추가한 OSS hardening 버전

## How To Read

1. `v0`에서 baseline selector와 offline eval을 본다.
2. `v1`에서 rerank/feedback/compare 운영 루프를 본다.
3. `v2`에서 release gate와 submission artifact로 capstone을 닫는다.
4. `v3`에서 self-hosted 팀 도구로 만들기 위해 무엇을 더 붙였는지 본다.

## Presentation Assets

- `v0`, `v1`, `v2`, `v3`는 각각 `docs/presentation-deck.md`와 `docs/presentation-assets/`를 가진다.
- 발표에서는 `v2`가 최종 capstone임을 먼저 말하고, `v3`는 “사람들이 실제로 설치해서 쓸 수 있게 만들려면 무엇이 더 필요한가”를 답하는 확장으로 다룬다.
