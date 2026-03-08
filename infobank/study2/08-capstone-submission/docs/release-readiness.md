# Capstone Release Matrix

이 문서는 `08-capstone-submission`의 공개 저장소 마감 기준을 한 장에 요약한다.

## Version Roles

- `v0-initial-demo`: SQLite + heuristic baseline. runnable snapshot을 우선 안정화한 버전.
- `v1-regression-hardening`: provider chain, lineage/version compare, trace payload, PostgreSQL smoke를 더한 운영 안정화 버전.
- `v2-submission-polish`: retrieval improvement experiment와 compare proof를 반영한 제출 버전.
- `v3-self-hosted-oss`: `v2`를 single-team self-hosted OSS snapshot으로 승격한 버전. 로그인, 업로드, 비동기 job, Docker Compose quickstart를 제공한다.

## Verified Commands

- `v0`
  - `cd python && UV_PYTHON=python3.12 make gate-all`
- `v1`
  - `cd python && UV_PYTHON=python3.12 make gate-all`
  - `cd python && UV_PYTHON=python3.12 make smoke-postgres`
- `v2`
  - `cd python && UV_PYTHON=python3.12 make gate-all`
  - `cd python && UV_PYTHON=python3.12 make smoke-postgres`
- `v3`
  - `cd python && UV_PYTHON=python3.12 uv sync --extra dev`
  - `cd python && UV_PYTHON=python3.12 make gate-all`
  - `cd ../react && pnpm install && pnpm build`
  - `cd .. && docker compose config`
  - `cd .. && docker compose build api worker web`
  - `cd .. && docker compose up -d && docker compose ps -a`

## Compare Result Used For Submission

- baseline source: `v1` code with `retrieval-v1`
- candidate source: `v2` code with `retrieval-v2`
- dataset: `golden-set`
- measured result:
  - `avg_score 84.06 -> 87.76`
  - `critical_count 2 -> 0`
  - `pass_count 16 -> 19`
  - `fail_count 14 -> 11`

증빙 파일:

- [`api-version-compare.json`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v2-submission-polish/docs/demo/proof-artifacts/api-version-compare.json)
- [`cli-compare.txt`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v2-submission-polish/docs/demo/proof-artifacts/cli-compare.txt)
- [`improvement-report.json`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json)

## Public Notes

- `v0/v1/v2`는 폴더 단위 snapshot 규칙을 유지한다.
- self-hosted 사용 권장 버전은 `v3-self-hosted-oss`다.
- 최종 설계는 PostgreSQL, Langfuse, Upstage Solar 중심이지만, 공개 저장소 기준 재현 가능한 기본 검증은 heuristic + SQLite fallback도 함께 남긴다.
- live credential이 없어도 테스트와 compare proof는 재현된다.
