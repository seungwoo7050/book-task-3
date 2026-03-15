# Chat QA Ops 시리즈 맵

이 프로젝트를 제대로 읽으려면 챗봇 품질 평가를 "점수 하나"로 보지 말아야 한다. 실제 소스는 더 복합적인 구조를 갖는다. rule/guardrail이 먼저 실패를 자르고, evidence verifier가 근거를 남기고, judge/scorer가 점수를 합치고, dashboard/CLI가 같은 evaluation row를 다시 읽어 compare proof를 만든다. 마지막에는 그 same evaluation grammar가 로그인, dataset upload, async job, selected-job review UI를 가진 self-hosted 운영 표면으로 옮겨 간다.

## 이 프로젝트를 읽는 질문

- 왜 Rule -> Evidence -> Judge 순서가 평가 파이프라인의 첫 고정점이 되었는가
- regression proof는 어떤 데이터 모델과 저장 구조 위에 세워졌는가
- historical improvement artifact와 현재 재실행 결과는 왜 분리해서 읽어야 하는가
- `v3` 확장은 새 evaluator보다 어떤 운영 surface를 추가한 것인가

## 이번에 사용한 근거

- 문제 정의: `projects/02-chat-qa-ops/problem/README.md`
- 단계 지도: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 공식 답: `capstone/v2-submission-polish/README.md`
- 핵심 코드:
  - `capstone/v2-submission-polish/python/backend/src/evaluator/pipeline.py`
  - `capstone/v2-submission-polish/python/backend/src/api/routes/dashboard.py`
  - `capstone/v2-submission-polish/python/backend/src/cli/main.py`
  - `capstone/v3-self-hosted-oss/python/backend/src/core/auth.py`
  - `capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py`
  - `capstone/v3-self-hosted-oss/react/src/App.tsx`
  - `capstone/v3-self-hosted-oss/react/src/pages/Jobs.tsx`
- proof 자료:
  - `capstone/v2-submission-polish/docs/demo/demo-runbook.md`
  - `capstone/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json`
  - `capstone/v2-submission-polish/docs/demo/proof-artifacts/cli-compare.txt`
- 실제 검증:
  - `PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make gate-all`
  - `PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make smoke-postgres`
  - `PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 uv run python -m cli.main compare v1.0 v1.1`
  - `v3 PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make gate-all`

## 이번 재실행에서 먼저 드러난 사실

2026-03-14에 현재 snapshot을 다시 검증했을 때, `gate-all`과 `smoke-postgres`는 정상 통과했다. 다만 regression proof는 둘로 나뉘어 읽어야 했다.

- historical proof artifact: `avg_score 84.06 -> 87.76`, `critical_count 2 -> 0`, `pass_count 16 -> 19`, `fail_count 14 -> 11`
- current local rerun on the same snapshot: `avg_score 87.76 -> 87.76`, delta `0.0`

이 차이는 중요하다. 현재 `v2` snapshot 안에는 baseline `v1` 코드가 따로 살아 있지 않고, run label만 바꿔 같은 snapshot에서 golden evaluation을 다시 만들면 improvement가 재현되지 않는다. 즉 docs/demo proof artifact는 historical compare evidence이고, 현재 로컬 재실행은 "이 snapshot 하나만으로는 그 uplift를 다시 만들 수 없다"는 현재 상태를 보여 준다.

또 하나 드러난 사실은 `Makefile`의 `compare` 타깃이 현재 CLI 시그니처와 맞지 않는다는 점이다. `make compare`는 `--baseline/--candidate` 옵션을 넘기지만, `cli.main compare`는 positional args를 요구한다. 그래서 compare는 `python -m cli.main compare v1.0 v1.1`로 직접 호출해야 했다.

## 챕터 구성

1. [10-first-qa-evaluation-loop.md](./10-first-qa-evaluation-loop.md)
   - 평가 파이프라인이 왜 단계별 trace를 남기는 구조로 시작했는지 본다.
2. [20-regression-hardening-and-proof.md](./20-regression-hardening-and-proof.md)
   - dashboard/CLI/proof artifact가 어떤 개선 증빙을 만들고, 현재 snapshot 재실행과는 어디서 갈라지는지 본다.
3. [30-self-hosted-review-ops.md](./30-self-hosted-review-ops.md)
   - 같은 평가 문법이 `v3`에서 auth, dataset, job, selected review surface로 어떻게 이동하는지 본다.
