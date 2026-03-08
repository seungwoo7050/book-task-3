# Capstone Docs

이 디렉터리는 capstone 버전 공통 문서와 시연 자료를 보관한다.

## Version Roles

- `v0-*`: runnable baseline과 local heuristic path 정리
- `v1-*`: provider fallback, lineage/trace, PostgreSQL smoke, version compare hardening
- `v2-*`: retrieval improvement proof와 제출용 artifact 마감

## Concept Focus

- immutable version snapshots
- provider fallback chain
- trace-rich evaluation pipeline
- run-level version compare
- RAG improvement proof

## Verification Snapshot

- `v0`, `v1`, `v2` 모두 `UV_PYTHON=python3.12 make gate-all`을 통과시켰다.
- `v1`, `v2`에서 `make smoke-postgres`를 통과시켰다.
- baseline/candidate compare 결과는 `avg_score 84.06 -> 87.76`, `critical 2 -> 0`, `pass 16 -> 19`, `fail 14 -> 11`이다.

## Read In This Order

- `README.md`
- `docs/release-readiness.md`
- `v0-*/README.md`, `v1-*/README.md`, `v2-*/README.md`
- `v2-submission-polish/docs/demo/proof-artifacts/`

## Known Gap

- live Upstage/OpenAI/Langfuse credential path는 기본 검증에 포함되지 않았다.
- tracked 문서는 stable index 역할을 하고, 세부 process log는 local-only `notion/`에 남긴다.
