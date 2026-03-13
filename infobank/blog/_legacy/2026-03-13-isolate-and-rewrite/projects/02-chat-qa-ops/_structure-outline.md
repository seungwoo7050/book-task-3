# 02 챗봇 상담 품질 관리 structure outline

## 시리즈 목표

- `v0`에서 왜 상담 품질 평가를 guardrail -> evidence -> judge -> aggregate 순으로 먼저 고정했는지 보여 준다.
- `v1~v2`에서 provider chain, retrieval-v2, compare artifact가 어떻게 regression proof 흐름으로 묶였는지 보여 준다.
- `v3`에서 batch evaluate demo가 왜 self-hosted review ops 제품으로 바뀌는지 보여 준다.

## 글 배치

| 글 | 범위 | 중심 질문 | 꼭 넣을 코드 앵커 | 꼭 넣을 CLI |
| --- | --- | --- | --- | --- |
| `10-first-qa-evaluation-loop.md` | `v0` 중심, `v1` 진입 | 상담 품질 평가 loop를 어떻게 replayable pipeline으로 고정했는가 | `evaluator/pipeline.py`, `backend/src/cli/main.py`, `python/Makefile` | `make init-db`, `make seed-demo`, `make gate-all` |
| `20-regression-hardening-and-proof.md` | `v1 -> v2` | provider failure와 retrieval 실험을 어떻게 regression proof로 바꿨는가 | `provider_chain.py`, `retriever.py`, `bot.py`, `cli/main.py` | `make smoke-postgres`, `make gate-all`, proof-artifact compare |
| `30-self-hosted-review-ops.md` | `v3` | 제출용 evaluate demo를 self-hosted review ops 제품으로 바꿀 때 어떤 경계가 필요했는가 | `api/routes/evaluation.py`, `api/routes/jobs.py`, `services/jobs.py` | `uv sync --extra dev`, `make gate-all`, `docker compose up --build` |

## 서술 원칙

- Day/Session은 버전 사다리 기준으로 끊고, 나중에 알게 된 사실을 앞세우지 않는다.
- 각 글마다 코드 스니펫 2개 이상, CLI 블록 2개 이상을 넣는다.
- compare proof는 막연한 "점수가 올랐다"가 아니라 어떤 JSON artifact와 어떤 함수 시그니처를 근거로 읽었는지까지 적는다.
