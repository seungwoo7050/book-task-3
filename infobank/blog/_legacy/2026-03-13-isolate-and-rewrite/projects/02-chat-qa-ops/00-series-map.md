# 챗봇 상담 품질 관리 시리즈 지도

## 이 프로젝트를 한 줄로

상담 품질을 rubric과 failure taxonomy로 먼저 정의한 뒤, guardrail/evidence/judge/regression/dashboard를 self-hosted review ops 제품까지 밀어 올리는 프로젝트다. 시작점은 "이 답변을 어떻게 평가할까"였지만, 끝에 가면 질문이 "어떤 dataset과 KB bundle 조합을 어떤 운영자가 다시 돌릴 수 있을까"로 바뀐다.

## 문제 구조

- 원 프로젝트: [`../../../projects/02-chat-qa-ops/README.md`](../../../projects/02-chat-qa-ops/README.md)
- 문제 정의: [`../../../projects/02-chat-qa-ops/problem/README.md`](../../../projects/02-chat-qa-ops/problem/README.md)
- 공식 답: [`../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/README.md`](../../../projects/02-chat-qa-ops/capstone/v2-submission-polish/README.md)
- 확장 답: [`../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/README.md`](../../../projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/README.md)
- canonical verify:
  - `UV_PYTHON=python3.12 make init-db`
  - `UV_PYTHON=python3.12 make seed-demo`
  - `UV_PYTHON=python3.12 make gate-all`
  - `UV_PYTHON=python3.12 make smoke-postgres`
  - `UV_PYTHON=python3.12 uv sync --extra dev`

## 버전 사다리

| 버전 | 무엇을 처음 고정했는가 | 대표 코드/문서 | 대표 검증 신호 |
| --- | --- | --- | --- |
| `v0-initial-demo` | guardrail short-circuit, evidence verification, replayable evaluation pipeline | `evaluator/pipeline.py`, `backend/src/cli/main.py` | `make init-db`, `make seed-demo` |
| `v1-regression-hardening` | provider chain, dependency failure trace, PostgreSQL smoke path | `core/provider_chain.py`, `scripts/smoke_postgres.sh` | `make smoke-postgres` |
| `v2-submission-polish` | retrieval-v2, retrieval-conditioned answer composer, compare artifact, improvement report | `chatbot/retriever.py`, `chatbot/bot.py`, `docs/demo/proof-artifacts/*.json` | `gate-all passed`, `84.06 -> 87.76`, `critical 2 -> 0` |
| `v3-self-hosted-oss` | 로그인, dataset/KB bundle selection, async evaluation job, worker loop, Compose quickstart | `api/routes/jobs.py`, `services/jobs.py`, `docker-compose.yml` | `uv sync --extra dev`, `v3 gate-all passed`, Compose quickstart |

## 이 시리즈에서 따라갈 질문

1. 상담 품질 평가에서 judge보다 먼저 고정해야 했던 guardrail과 aggregate 경계는 무엇이었는가.
2. replay와 golden-set evaluation이 왜 CLI와 MP gate 형태로 먼저 굳어야 했는가.
3. provider fallback은 왜 편의 기능이 아니라 regression 안정성 계층이었는가.
4. retrieval-v2 개선은 어떻게 compare JSON과 improvement report로 증명됐는가.
5. self-hosted review ops를 만들면서 왜 `/evaluate/batch`만으로는 부족했고 `/jobs`가 필요해졌는가.

## 근거 메모

- `compare`는 현재 CLI가 positional 인자를 기대하지만 Makefile은 오래된 `--baseline/--candidate` 플래그를 호출한다.
- 그래서 이 시리즈의 compare 수치는 소스의 `compare(baseline, candidate)` 시그니처와 committed proof artifact JSON을 함께 근거로 읽는다.

## 글 목록

| 번호 | 파일 | 범위 |
| --- | --- | --- |
| `10` | [`10-first-qa-evaluation-loop.md`](10-first-qa-evaluation-loop.md) | `v0`의 evaluation pipeline, golden-set CLI, MP gate가 baseline loop로 굳는 구간 |
| `20` | [`20-regression-hardening-and-proof.md`](20-regression-hardening-and-proof.md) | `v1` provider chain에서 `v2` retrieval-v2 compare proof로 넘어가는 구간 |
| `30` | [`30-self-hosted-review-ops.md`](30-self-hosted-review-ops.md) | `v3`에서 async job, worker, self-hosted 운영 경계를 붙이는 구간 |
