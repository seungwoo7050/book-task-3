# 02 챗봇 상담 품질 관리 Evidence Ledger

이 문서는 이 시리즈를 어떤 근거로 복원했는지 보여 주는 기록이다. 예전 blog 초안을 다시 다듬은 것이 아니라, 현재 `README`, `docs`, 코드, 테스트, CLI 결과를 바탕으로 "이 프로젝트가 어떤 순서로 자랐는가"를 다시 세웠다.

## 독립 프로젝트 판정

- 문제 범위: `rule -> evidence -> judge -> golden regression -> dashboard -> self-hosted review ops`
- 진입점: `projects/02-chat-qa-ops/README.md`
- 검증 표면:
  - `UV_PYTHON=python3.12 make gate-all`
  - `UV_PYTHON=python3.12 make smoke-postgres`
  - `v3 UV_PYTHON=python3.12 make gate-all`
- 복원 근거: `docs/stage-catalog.md`는 `v0 -> v3` 평가 사다리를 보여 주고, `docs/verification-matrix.md`는 v2/v3 검증 경로를 따로 정리해 준다.

## 어떤 자료를 읽었는가

- stage map: `docs/stage-catalog.md`
- verification map: `docs/verification-matrix.md`
- front door 문서: `capstone/v2-submission-polish/README.md`, `capstone/v3-self-hosted-oss/README.md`
- proof 자료: `docs/demo/demo-runbook.md`, `docs/demo/phase1-vs-phase2-diff-matrix.md`, `docs/demo/proof-artifacts/improvement-report.json`, `docs/demo/proof-artifacts/cli-report.txt`, `docs/demo/proof-artifacts/cli-compare.txt`
- 핵심 코드: `python/backend/src/evaluator/pipeline.py`, `python/backend/src/api/routes/dashboard.py`, `python/backend/src/cli/main.py`
- 확장 코드: `v3 python/backend/src/core/auth.py`, `v3 python/backend/src/api/routes/auth.py`, `v3 python/backend/src/api/routes/jobs.py`, `v3 python/backend/src/services/jobs.py`, `v3 react/src/App.tsx`, `v3 react/src/pages/Jobs.tsx`
- git anchor: `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## Chronology Ledger

### 1. Phase 1 - Rule -> Evidence -> Judge 파이프라인을 먼저 세운다

한 줄 요약: 이 프로젝트의 출발점은 더 똑똑한 모델이 아니라, 실패를 일찍 잡고 trace를 남기는 평가 파이프라인이다.

- 당시 목표: 상담 품질 평가를 "좋아 보이는 답변"이 아니라 재실행 가능한 score contract로 만든다.
- 변경 단위: `python/backend/src/evaluator/pipeline.py`, `python/backend/src/cli/main.py`, `docs/stage-catalog.md`
- 처음 가설: critical failure를 초기에 short-circuit하지 않으면 evaluation 비용도 늘고 failure taxonomy도 흐려진다.
- 실제 조치: rule check를 먼저 돌리고, critical이면 즉시 short-circuit하고, 아니면 claim extraction -> evidence verification -> judge -> scoring 순서로 이어지게 했다.
- CLI: `UV_PYTHON=python3.12 make gate-all`
- 검증 신호:
  - mypy `42 source files`
  - MP tests `3 + 5 + 15 + 5 + 16 passed`
  - frontend `5 passed`

이 코드가 중요한 이유는, 이 프로젝트가 처음부터 "한 번 채점하는 함수"가 아니라 단계별로 실패와 근거를 남기는 파이프라인을 목표로 했다는 점을 보여 주기 때문이다.

```python
rule_results = evaluate_rules(...)

if has_critical_rule(rule_results):
    short_circuit = True
    short_circuit_reason = "critical_rule"
else:
    claims, claim_attempts = extract_claims_with_trace(turn.assistant_response)
    evidence_result, evidence_attempts = verify_claims_with_trace(self.session, claims, top_k=3)
    llm_judgment, judge_attempts = judge_response_with_trace(...)
```

- 새로 배운 것: 이 트랙의 첫 안정화 포인트는 LLM 자체가 아니라, failure를 얼마나 빨리 분기해 낼 수 있는가였다.
- 다음: 같은 evaluation 결과를 CLI와 dashboard에서 함께 읽히게 만든다.

### 2. Phase 2 - golden regression과 dashboard compare를 proof로 고정한다

한 줄 요약: 한 번의 평가 결과를 넘어, baseline과 candidate의 차이를 같은 golden set 위에서 수치로 남기기 시작한다.

- 당시 목표: 단일 실행 결과가 아니라 baseline/candidate 개선 수치를 남기는 회귀 루프를 만든다.
- 변경 단위: `python/backend/src/api/routes/dashboard.py`, `python/backend/src/cli/main.py`, `docs/demo/proof-artifacts/*`
- 처음 가설: UI 차이가 작아도 `run_label`, `dataset`, `assertion_result`를 보존하면 compare proof를 수치로 닫을 수 있다.
- 실제 조치: dashboard와 CLI 모두 baseline/candidate의 avg score, critical count, pass/fail count를 같은 데이터 모델로 계산하게 했다.
- CLI: `make gate-all`, `make smoke-postgres`, proof artifact의 `cli-report.txt`, `cli-compare.txt`
- 검증 신호:
  - `PostgreSQL smoke verification passed`
  - `avg_score 84.06 -> 87.76`
  - `critical_count 2 -> 0`
  - `pass_count 16 -> 19`

이 코드 조각은 compare가 별도 계산기를 쓰는 것이 아니라, 이미 저장된 evaluation 결과를 다시 읽어 proof를 만드는 구조라는 점을 보여 준다.

```python
result = VersionCompareResult(
    baseline=baseline,
    candidate=candidate,
    dataset=dataset or "all",
    baseline_avg=_avg(baseline_rows),
    candidate_avg=_avg(candidate_rows),
    ...
    delta=round(_avg(candidate_rows) - _avg(baseline_rows), 2),
)
```

- 새로 배운 것: QA Ops에서 regression은 새 evaluator를 붙이는 일보다 lineage와 run label을 안정적으로 유지하는 일이 더 중요했다.
- 다음: 이 review surface를 로그인, dataset import, job queue가 있는 self-hosted OSS로 확장한다.

### 3. Phase 3 - self-hosted review ops로 productization한다

한 줄 요약: `v2`의 golden-set 중심 증빙을 `dataset + KB bundle + async job` 운영 표면으로 옮긴다.

- 당시 목표: `v2`의 증빙을 `dataset + KB bundle + async job`을 가진 운영 표면으로 바꾼다.
- 변경 단위: `v3 python/backend/src/core/auth.py`, `v3 python/backend/src/api/routes/jobs.py`, `v3 python/backend/src/services/jobs.py`, `v3 react/src/App.tsx`, `v3 react/src/pages/Jobs.tsx`
- 처음 가설: self-hosted 확장의 핵심은 새 평가 축이 아니라 로그인, import, job progress, selected job 기반 dashboard filtering이다.
- 실제 조치: admin cookie auth를 추가하고, dataset/KB bundle을 선택해 evaluation job을 만들고, worker loop가 pending job을 처리하게 했다.
- CLI: `cd capstone/v3-self-hosted-oss/python && UV_PYTHON=python3.12 make gate-all`
- 검증 신호:
  - mypy `51 source files`
  - MP tests `2 + 4 + 2 + 1 + 1 passed`
  - frontend `6 passed`

이 단계에서 중요한 코드는 두 군데다. 하나는 로그인 상태를 만드는 auth 코드이고, 다른 하나는 job progress를 실제로 갱신하는 worker 코드다. 덕분에 평가가 더 이상 "한 번 실행하는 명령"이 아니라, 운영자가 기다리고 확인하는 작업이 된다.

```python
cookie_value = create_session_cookie(secret=settings.session_secret, user_id=admin.id, email=admin.email)
response.set_cookie(key=SESSION_COOKIE_NAME, value=cookie_value, httponly=True, samesite="lax")
```

```python
job.progress_total = len(turn_ids)
job.progress_completed = 0
job.status = "running"
...
job.progress_completed = index
...
job.status = "completed"
```

- 새로 배운 것: review ops를 self-hosted로 옮긴다는 건 평가 함수를 갈아엎는 일이 아니라, 같은 평가를 dataset/job 단위로 묶어 운영자가 다룰 수 있게 만드는 일이다.

## 최신 CLI 발췌

```bash
UV_PYTHON=python3.12 make gate-all
UV_PYTHON=python3.12 make smoke-postgres
cd ../v3-self-hosted-oss/python && UV_PYTHON=python3.12 make gate-all
```

```text
v2 gate-all: 3 + 5 + 15 + 5 + 16 passed, frontend 5 passed
PostgreSQL smoke verification passed
v2 compare proof: avg_score 84.06 -> 87.76, critical_count 2 -> 0
v3 gate-all: 2 + 4 + 2 + 1 + 1 passed, frontend 6 passed
```
