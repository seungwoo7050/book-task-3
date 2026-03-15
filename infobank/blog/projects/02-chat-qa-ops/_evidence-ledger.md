# 02 챗봇 상담 품질 관리 Evidence Ledger

이 문서는 현재 blog를 어떤 근거와 어떤 재실행 결과로 다시 세웠는지 남긴다. 기존 blog를 정리한 것이 아니라, 현재 코드와 2026-03-14 검증 로그를 기준으로 chronology를 다시 잡았다.

## 독립 프로젝트 판정

- front door가 분명하다: `projects/02-chat-qa-ops/README.md`
- 공식 답과 확장 답이 분리돼 있다: `capstone/v2-submission-polish`, `capstone/v3-self-hosted-oss`
- stage map과 verification matrix가 따로 있다: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- blog 대상은 "상담 챗봇 앱"이 아니라 "QA evaluation + proof + review ops" 전체다.

## 이번에 읽은 핵심 자료

- 문제/범위: `problem/README.md`, `v2-submission-polish/README.md`, `v3-self-hosted-oss/README.md`
- stage/verification 지도: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 평가 파이프라인: `python/backend/src/evaluator/pipeline.py`
- dashboard/CLI: `python/backend/src/api/routes/dashboard.py`, `python/backend/src/cli/main.py`
- historical proof: `docs/demo/proof-artifacts/improvement-report.json`, `cli-compare.txt`, `demo-runbook.md`
- self-hosted 확장: `v3 core/auth.py`, `v3 services/jobs.py`, `v3 react/src/App.tsx`, `v3 react/src/pages/Jobs.tsx`

## Chronology Ledger

### 1. Rule -> Evidence -> Judge 순서로 평가를 고정한다

- 기준 파일: `pipeline.py`
- 핵심 신호: critical short-circuit, claim/evidence/judge trace, lineage metadata
- 해석: 이 프로젝트의 첫 안정화 포인트는 모델 품질보다 failure routing과 auditability였다.

### 2. 같은 evaluation row를 다시 읽어 proof를 만든다

- 기준 파일: `dashboard.py`, `cli/main.py`
- 핵심 신호: version compare가 stored rows를 `run_label`/`dataset` 기준으로 다시 집계
- 해석: compare는 별도 evaluator가 아니라 lineage discipline 위에 세워진 증빙 출구다.

### 3. historical improvement artifact와 current rerun을 분리해 읽어야 한다

- 기준 자료: `improvement-report.json`, `cli-compare.txt`, 현재 `cli.main compare`
- 핵심 신호:
  - historical artifact: `84.06 -> 87.76`, `critical 2 -> 0`
  - current local rerun on same snapshot: `87.76 -> 87.76`, delta `0.0`
- 해석: 현재 `v2` snapshot 하나만으로는 baseline `v1` uplift를 그대로 재생하지 못하고, 지금 rerun의 의미는 "historical uplift를 다시 증명"하는 것보다 "compare surface와 lineage discipline이 아직 살아 있는지 확인"하는 쪽에 더 가깝다.

### 4. self-hosted 확장은 evaluator보다 운영 surface를 확장한다

- 기준 파일: `v3 auth.py`, `jobs.py`, `App.tsx`, `Jobs.tsx`
- 핵심 신호: signed session cookie, job progress, selected job state, polling refresh
- 해석: `v3`의 본질은 evaluation logic 추가가 아니라 운영 단위 추가다.

## 이번 재실행 CLI 기록

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make gate-all
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make smoke-postgres
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make init-db
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make seed-demo
PATH="$HOME/.local/bin:$PATH" QUALBOT_EVAL_MODE=heuristic QUALBOT_RETRIEVAL_BACKEND=keyword UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main evaluate --golden-set --run-label v1.0 --retrieval-version retrieval-v1
PATH="$HOME/.local/bin:$PATH" QUALBOT_EVAL_MODE=heuristic QUALBOT_RETRIEVAL_BACKEND=keyword UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main evaluate --golden-set --run-label v1.1 --retrieval-version retrieval-v2
PATH="$HOME/.local/bin:$PATH" QUALBOT_EVAL_MODE=heuristic QUALBOT_RETRIEVAL_BACKEND=keyword UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main compare v1.0 v1.1
cd ../../v3-self-hosted-oss/python
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make gate-all
```

## 이번 재실행 결과 요약

- `v2 gate-all`: lint + mypy + MP1~MP5 + frontend 전부 통과
- `v2 smoke-postgres`: 통과
- `make compare`: `No such option: --baseline`으로 실패
- `cli.main compare v1.0 v1.1`: `87.76 -> 87.76`, delta `0.0`
- `v3 gate-all`: lint + mypy + MP1~MP5 + frontend 전부 통과
- `v3 frontend`: tests pass, non-blocking tooling warnings 존재
