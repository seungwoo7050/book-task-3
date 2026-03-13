# 02 챗봇 상담 품질 관리 evidence ledger

## 독립 프로젝트 판정 근거

- 자기 문제 범위: rubric, guardrail, evidence verification, judge scoring, regression compare, review console을 한 제품 질문으로 설명할 수 있다.
- 자기 검증 명령: `UV_PYTHON=python3.12 make init-db`, `make seed-demo`, `make gate-all`, `make smoke-postgres`, `uv sync --extra dev`, `docker compose up --build`.
- 자기 구현 흐름: `v0 -> v1 -> v2 -> v3` 버전 디렉터리와 `docs/stage-catalog.md`가 독립 chronology를 제공한다.

## Day 1 / Session 1

- 시간 표지: Day 1 / Session 1
- 당시 목표: 상담 품질을 대시보드보다 먼저 replayable evaluation pipeline으로 고정한다.
- 변경 단위: `capstone/v0-initial-demo/python/backend/src/evaluator/pipeline.py`, `capstone/v0-initial-demo/python/backend/src/evaluator/rule_eval.py`, `capstone/v0-initial-demo/python/backend/src/evaluator/scorer.py`
- 처음 가설: 모든 turn은 judge 단계까지 가서 점수를 계산해야 품질 평가가 성립한다고 봤다.
- 실제 조치: critical rule violation이 먼저 나면 evidence/judge 단계를 short-circuit하고, 그래도 evaluation row와 conversation aggregate는 남기게 만들었다.
- CLI:

```bash
$ UV_PYTHON=python3.12 make init-db
Database initialized

$ UV_PYTHON=python3.12 make seed-demo
Seed completed kb_upsert=15, golden_upsert=30, golden_total=30
```

- 검증 신호: knowledge base 15건과 golden set 30건이 고정되면서 replay와 assertion이 같은 데이터셋을 읽을 수 있게 됐다.
- 핵심 코드 앵커: `backend/src/evaluator/pipeline.py`의 `has_critical_rule()` short-circuit, `self.session.flush()` 후 `_refresh_conversation_score()`
- 새로 배운 것: QA Ops의 시작점은 점수 계산이 아니라 "위험한 답변은 평가 흐름에서도 우회하지 못하게 막는 것"이었다.
- 다음: 이 pipeline을 사람이 반복 실행할 수 있는 CLI와 gate로 묶어야 한다.

## Day 1 / Session 2

- 시간 표지: Day 1 / Session 2
- 당시 목표: replay, golden-set evaluation, report를 모두 CLI 한 층으로 묶어 재현 가능한 baseline을 만든다.
- 변경 단위: `capstone/v2-submission-polish/python/backend/src/cli/main.py`, `capstone/v2-submission-polish/python/Makefile`, `capstone/v2-submission-polish/python/tests`
- 처음 가설: `pytest -q` 한 번이면 baseline 품질 관리도 충분할 것이라고 봤다.
- 실제 조치: `init-db`, `seed-demo`, `evaluate --golden-set`, `report`, `compare`, `gate-all`을 각각 명령으로 분리하고 MP1~MP5 무결성 gate를 붙였다.
- CLI:

```bash
$ UV_PYTHON=python3.12 make gate-all
ruff check: OK
mypy: OK
MP1: 3 passed
MP2: 5 passed
MP3: 15 passed
MP4: 5 passed
MP5: 16 passed
frontend vitest: 5 passed
Integrity gate passed for target=all
```

- 검증 신호: lint, type, backend MP gate, frontend vitest가 하나의 진입점으로 묶여 있어서 "평가 파이프라인만 맞는 상태"를 통과시키지 않는다.
- 핵심 코드 앵커: `backend/src/cli/main.py`의 `evaluate(..., golden_set=True)`, `create_evaluation_run()` 호출, `Makefile`의 `gate-all`
- 새로 배운 것: QA Ops baseline은 기능 목록이 아니라 운영자가 다시 눌러 볼 수 있는 명령 집합으로 고정돼야 했다.
- 다음: dependency 불안정성과 provider 실패도 trace 안에 넣어야 regression이 흔들리지 않는다.

## Day 2 / Session 1

- 시간 표지: Day 2 / Session 1
- 당시 목표: 외부 모델 의존성을 한 provider 실패로 무너지지 않는 경로로 바꾼다.
- 변경 단위: `capstone/v1-regression-hardening/python/backend/src/core/provider_chain.py`, `capstone/v1-regression-hardening/python/backend/src/core/config.py`, `capstone/v1-regression-hardening/python/backend/src/core/langfuse_trace.py`
- 처음 가설: judge나 answer generation은 단일 provider에 붙여 두고 timeout만 잘 잡아도 괜찮을 것이라고 봤다.
- 실제 조치: provider chain이 `upstage -> openai -> ollama` 순으로 attempt를 기록하고, 끝까지 실패하면 provider별 에러를 합쳐 `DependencyUnavailableError`로 올리게 했다.
- CLI:

```bash
$ UV_PYTHON=python3.12 make smoke-postgres
PostgreSQL smoke verification passed
```

- 검증 신호: smoke path가 SQLite 데모에서 끝나지 않고 PostgreSQL session, replay, API 기동 경로까지 살아 있음을 확인한다.
- 핵심 코드 앵커: `backend/src/core/provider_chain.py`의 `generate_text()`, `generate_json()`, `_build_error_message()`
- 새로 배운 것: provider fallback은 편의 기능이 아니라 regression trace를 지키는 안정성 계층이었다.
- 다음: 이제 retrieval과 answer composer를 실험해도 baseline/candidate compare가 설명 가능해야 한다.

## Day 3 / Session 1

- 시간 표지: Day 3 / Session 1
- 당시 목표: retrieval 개선을 체감 수준이 아니라 golden-set compare artifact로 증명한다.
- 변경 단위: `capstone/v2-submission-polish/python/backend/src/chatbot/retriever.py`, `capstone/v2-submission-polish/python/backend/src/chatbot/bot.py`, `capstone/v2-submission-polish/python/backend/src/cli/main.py`, `capstone/v2-submission-polish/docs/demo/proof-artifacts/*.json`
- 처음 가설: keyword overlap 기반 retrieval만으로도 제출용 evidence는 충분할 것이라고 봤다.
- 실제 조치: alias/category/risk 기반 `retrieval-v2` plan과 retrieval-conditioned safe answer composer를 넣고, baseline/candidate compare 숫자를 JSON artifact로 남겼다.
- CLI / artifact:

```bash
$ sed -n '1,120p' docs/demo/proof-artifacts/improvement-report.json
baseline avg_score: 84.06
candidate avg_score: 87.76
baseline critical_count: 2
candidate critical_count: 0

$ sed -n '1,120p' docs/demo/proof-artifacts/api-version-compare.json
delta: 3.7
pass_delta: 3
fail_delta: -3
critical_delta: -2
```

- 검증 신호: same golden-set 기준에서 `84.06 -> 87.76`, critical `2 -> 0`, pass `16 -> 19`, fail `14 -> 11`이 함께 남아 있어서 retrieval 개선을 한 문장으로 과장하지 않아도 된다.
- 핵심 코드 앵커: `backend/src/chatbot/retriever.py`의 `_build_retrieval_plan()` / `_search_keyword_v2()`, `backend/src/chatbot/bot.py`의 `_compose_retrieval_v2()`
- 새로 배운 것: retrieval 개선은 "더 잘 찾는다"보다 "위험한 질문에서 어떤 정책 문서를 우선 노출시키는가"를 코드로 밝힐 때 의미가 생긴다.
- 다음: 제출용 compare proof를 self-hosted review product로 옮기려면 sync evaluate를 job system으로 바꿔야 한다.

## Day 4 / Session 1

- 시간 표지: Day 4 / Session 1
- 당시 목표: `v2` 제출 데모를 로그인된 운영자가 dataset과 KB bundle로 돌리는 self-hosted QA Ops 제품으로 확장한다.
- 변경 단위: `capstone/v3-self-hosted-oss/python/backend/src/api/routes/evaluation.py`, `capstone/v3-self-hosted-oss/python/backend/src/api/routes/jobs.py`, `capstone/v3-self-hosted-oss/python/backend/src/services/jobs.py`, `capstone/v3-self-hosted-oss/react/src/pages/Jobs.tsx`
- 처음 가설: `/evaluate/batch` 같은 sync endpoint만 있어도 운영 콘솔에는 충분할 것이라고 봤다.
- 실제 조치: evaluation run 생성, dataset/KB bundle 조합 검증, pending/running/completed 상태, progress 집계, worker loop를 별도 job 계층으로 분리했다.
- CLI:

```bash
$ UV_PYTHON=python3.12 uv sync --extra dev
Resolved and installed dev dependencies

$ UV_PYTHON=python3.12 make gate-all
MP1: 2 passed
MP2: 4 passed
MP3: 2 passed
MP4: 1 passed
MP5: 1 passed
frontend vitest: 6 passed
Integrity gate passed for target=all
```

- 검증 신호: `v3` gate는 backend job flow와 frontend operator surface까지 같은 snapshot으로 묶는다.
- 핵심 코드 앵커: `backend/src/api/routes/jobs.py`의 `create_job()`, `backend/src/services/jobs.py`의 `run_job()` / `run_worker_loop()`, `backend/src/api/routes/evaluation.py`의 `evaluate_batch()`
- 새로 배운 것: productization은 evaluator를 더 똑똑하게 만드는 일이 아니라, 어떤 dataset과 KB bundle 조합을 어떤 권한의 운영자가 다시 돌릴 수 있게 할지 경계를 세우는 일이었다.
- 다음: 최종 blog는 이 흐름을 `10 / 20 / 30` 세 글로 나눠 읽게 만든다.
