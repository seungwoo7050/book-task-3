# 02 챗봇 상담 품질 관리 개발 타임라인

이 문서는 `notion/` 없이 현재 capstone 버전, Python/React 소스, demo 문서, 테스트, 실제 검증 명령만으로 `02-chat-qa-ops`의 chronology를 복원한 기록이다. 실제 commit 시계열이 세밀하지 않아서 `Day / Session`과 `v0 -> v1 -> v2 -> v3` 버전 사다리를 기본 축으로 삼는다.

## Day 1

### Session 1

- 목표: `v0-initial-demo`가 단순 상담 챗봇이 아니라 `rubric + guardrail + evidence + judge + dashboard`를 한 번에 연결한 baseline인지 확인한다.
- 진행: `v0` README, `chatbot/bot.py`, `evaluator/pipeline.py`, `docs/demo/demo-runbook.md`를 함께 읽었다.
- 이슈: 처음엔 챗봇이 답변을 잘 만드는지가 중심일 거라고 생각했다. 그런데 pipeline은 `critical rule`을 먼저 보고, 그다음에만 claim/evidence/judge를 태운다.
- 판단: 이 트랙의 첫 버전은 "좋은 답변 생성"보다 "품질 실패를 어떤 순서로 검출하고 점수화할 것인가"가 더 중요하다.

CLI:

```bash
$ cd projects/02-chat-qa-ops/capstone/v0-initial-demo/python
$ uv sync --extra dev
$ make init-db
$ make seed-demo
$ make test-backend
$ make run-backend
```

별도 터미널:

```bash
$ cd ../react
$ pnpm install
$ pnpm test --run
$ pnpm dev
```

chat runtime이 retrieval과 guardrail을 함께 본다는 점이 먼저 눈에 들어왔다.

```py
docs = self.retriever.search(user_message, top_k=3)

if any(hit.severity == "critical" for hit in guardrail):
    assistant = "정책상 확정 안내가 어려워 상담원 연결로 도와드리겠습니다."
```

처음엔 RAG 챗봇이면 retrieval quality만 보면 될 줄 알았는데, 실제 baseline은 retrieval 이후에도 online guardrail을 한 번 더 태운다. 즉 대답을 잘 만드는 것보다 위험한 대답을 끊는 것이 우선이다.

evaluation pipeline도 같은 순서를 따른다.

```py
if has_critical_rule(rule_results):
    short_circuit = True
    short_circuit_reason = "critical_rule"
else:
    claims = extract_claims(turn.assistant_response)
    evidence_result = verify_claims(self.session, claims, top_k=3)
```

이 구조를 보고 나서야 `v0`의 핵심이 "judge 모델 붙이기"가 아니라 `rule -> evidence -> judge` 순서로 비용과 위험을 다루는 데 있다는 점이 분명해졌다.

### Session 2

- 목표: `v1-regression-hardening`이 기능 추가보다 어떤 운영 신호를 보강했는지 확인한다.
- 진행: `provider_chain.py`, `v1` pipeline, `test_lineage_and_trace.py`, `smoke_postgres.sh`를 읽어 provider fallback과 trace/run metadata 경로를 추적했다.
- 이슈: 처음엔 provider fallback을 편의 기능 정도로 봤다. 그런데 실제 코드는 각 provider 시도 결과를 모두 구조화해서 남기고, lineage payload에도 `run_label`, `dataset`, `retrieval_version`을 함께 넣는다.
- 판단: `v1`의 핵심은 "LLM 공급자 하나 더 붙이기"가 아니라, 실패했을 때 어느 provider에서 어떤 에러가 났는지와 어떤 run/version 조합에서 평가했는지를 회귀 비교 가능한 형태로 남기는 데 있다.

CLI:

```bash
$ cd projects/02-chat-qa-ops/capstone/v1-regression-hardening/python
$ UV_PYTHON=python3.12 uv sync --extra dev
$ UV_PYTHON=python3.12 make gate-all
$ UV_PYTHON=python3.12 make smoke-postgres
```

provider chain은 실패를 숨기지 않고 attempt 단위로 누적한다.

```py
for provider in self.settings.provider_chain:
    payload, attempt = self._generate(
        provider,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        want_json=True,
        model_hint=model_hint,
    )
    attempts.append(attempt)
```

처음엔 fallback이면 조용히 다음 provider로 넘기기만 할 줄 알았는데, 실제 구현은 각 attempt를 그대로 남긴 뒤 마지막에 `DependencyUnavailableError("provider", ...)`로 묶어 올린다. 이후 버전의 `dependency-health`와 `strict` 정책이 이 전제 위에서 동작한다.

lineage 쪽도 생각보다 이르다.

```py
return {
    "trace_id": run.trace_id,
    "lineage_id": run.lineage_id,
    "run_id": run.id,
    "run_label": run.run_label,
    "dataset": run.dataset_name,
    "retrieval_version": run.retrieval_version,
}
```

그리고 테스트는 run-level delta를 직접 확인한다.

```py
compare = client.get("/api/dashboard/version-compare?baseline=v1.0&candidate=v1.1&dataset=golden-set")
assert compare.status_code == 200
assert "pass_delta" in result
assert "critical_delta" in result
```

이 두 조각을 같이 읽고 나니 `v1`의 목표가 "점수를 한 번 더 매긴다"가 아니라, 나중에 baseline/candidate를 같은 축에서 비교할 수 있게 trace와 compare contract를 만드는 것이라는 점이 분명해졌다.

### Session 3

- 목표: `v2-submission-polish`가 어떤 개선을 실제 증빙으로 마감하는지 확인한다.
- 진행: `python/Makefile`, `test_retrieval_v2.py`, `react/src/pages/Overview.tsx`, `docs/demo/phase1-demo-proof.md`, `docs/demo/demo-runbook.md`, 실제 `make gate-all`, `make smoke-postgres` 경로를 확인했다.
- 이슈: 처음엔 `retrieval-v2`가 문서 설명만 더 좋아진 버전일 거라고 생각했다. 그런데 테스트는 alias/category 조합 때문에 상위 문서 순서가 실제로 바뀌어야 한다고 못 박고, Overview는 baseline/candidate compare hook를 직접 노출한다.
- 판단: `v2`의 핵심은 "개선됐다"는 말을 문서로 주장하는 게 아니라, retrieval 테스트와 dashboard compare hook, proof artifact를 같은 제출 surface로 묶는 데 있다.
- 검증:
- `UV_PYTHON=python3.12 make gate-all` 출력: `ruff` 통과, `mypy` 42 source files 통과, MP1 `3 passed`, MP2 `5 passed`, MP3 `15 passed`, MP4 `5 passed`, MP5 `16 passed`, frontend `5 passed`
- `UV_PYTHON=python3.12 make smoke-postgres` 출력: `PostgreSQL smoke verification passed`

CLI:

```bash
$ cd projects/02-chat-qa-ops/capstone/v2-submission-polish/python
$ UV_PYTHON=python3.12 uv sync --extra dev
$ UV_PYTHON=python3.12 make gate-all
$ UV_PYTHON=python3.12 make smoke-postgres
```

retrieval-v2가 정말 ranking을 바꾸는지부터 테스트가 보여 준다.

```py
baseline = _search("로밍패스 신청 없이 써도 되나요?", version="retrieval-v1")
candidate = _search("로밍패스 신청 없이 써도 되나요?", version="retrieval-v2")

assert "plans__roaming_pack.md" not in baseline[:1]
assert candidate[0] == "plans__roaming_pack.md"
```

처음엔 `retrieval-v2`가 파라미터 이름만 바꾼 튜닝처럼 보였는데, 테스트는 baseline과 candidate의 top 문서가 달라져야만 통과한다. 즉 개선 주장 자체가 이미 regression contract에 묶여 있다.

Overview 화면도 compare를 장식으로 두지 않는다.

```tsx
const params = new URLSearchParams({ baseline, candidate });
if (dataset.trim()) {
  params.set("dataset", dataset.trim());
}
const result = await apiGet<CompareResult>(`/api/dashboard/version-compare?${params.toString()}`);
```

이 compare hook를 보고 나서 `v2`를 발표 자료 정리 버전이라고만 읽을 수 없게 됐다. baseline/candidate를 직접 고르고 실패 분포와 delta를 같은 화면에서 보게 했기 때문에, 제출용 proof가 UI와 API 양쪽에 동시에 걸려 있다.

proof 문서는 실제로 어떤 산출물을 남겨야 하는지도 고정한다.

```text
evaluated=5 avg_score=65.48 critical=0 pass_count=1 fail_count=4
```

`phase1-demo-proof.md`는 `api-golden-run.json`, `api-overview.json`, `api-failures.json`, `api-pipeline-stats.json`, `cli-report.txt`를 한 묶음으로 요구한다. 따라서 `v2`에서 중요한 것은 점수 상승 하나가 아니라, 같은 평가 결과가 CLI, API, 대시보드, proof artifact에 동시에 남는지다.

### Session 4

- 목표: `v3-self-hosted-oss`가 demo 보존본이 아니라 실제 self-hosted 운영 스냅샷인지 확인한다.
- 진행: `auth.py`, `datasets.py`, `services/importers.py`, `services/jobs.py`, `react/src/App.test.tsx`, `react/src/pages/Jobs.test.tsx`, `v3` README를 읽어 login, upload, job worker, product shell을 같이 정리했다.
- 이슈: 처음엔 self-hosted라고 해도 로그인 화면과 업로드 버튼만 추가된 정도로 생각했다. 그런데 실제 구현은 `.jsonl` dataset import, Markdown ZIP KB bundle import, pending job picker, progress counter, worker loop까지 따로 있다.
- 판단: `v3`의 경계는 새 평가 지표가 아니라, 평가용 데이터와 KB를 업로드하고 evaluation run을 비동기 job으로 운영할 수 있게 만든 데 있다.

CLI:

```bash
$ cd projects/02-chat-qa-ops/capstone/v3-self-hosted-oss
$ docker compose up --build
```

또는 로컬:

```bash
$ cd python
$ UV_PYTHON=python3.12 uv sync --extra dev
$ UV_PYTHON=python3.12 make init-db
$ UV_PYTHON=python3.12 make seed-demo
$ UV_PYTHON=python3.12 make worker
$ UV_PYTHON=python3.12 make run-backend
```

별도 터미널:

```bash
$ cd react
$ pnpm install
$ pnpm test --run
$ pnpm dev
```

auth는 정말 최소하지만 product shell 진입을 강제한다.

```py
if admin is None or not verify_password(payload.password, admin.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
response.set_cookie(
    key=SESSION_COOKIE_NAME,
    value=cookie_value,
    httponly=True,
```

그리고 프론트 테스트도 login gate를 먼저 본다.

```tsx
expect(await screen.findByText("Self-Hosted QA Ops")).toBeDefined();
fireEvent.click(screen.getByText("로그인"));
expect(await screen.findByText("single-team self-hosted QA Ops workflow")).toBeDefined();
```

처음엔 self-hosted라고 해도 backend 기능만 늘어났을 줄 알았는데, 실제 product shell 자체가 `authenticated / unauthenticated` 상태를 먼저 나눈다.

업로드와 job worker는 더 운영형이다.

```py
if not file.filename.lower().endswith(".jsonl"):
    raise HTTPException(status_code=400, detail="dataset import only accepts .jsonl files")
```

```py
job.progress_total = len(turn_ids)
job.progress_completed = 0
job.status = "running"
...
for index, turn_id in enumerate(turn_ids, start=1):
    pipeline.evaluate_turn(
```

처음엔 dataset import가 샘플 fixture 복사 정도일 거라고 생각했는데, 실제 코드는 import validation과 background evaluation progress를 별도 엔드포인트/worker로 분리한다. 그래서 `v3`는 더 이상 "좋아진 제출 데모"가 아니라, single-team이 직접 로그인해서 dataset과 KB를 올리고 evaluation job을 돌리는 self-hosted QA Ops snapshot으로 읽는 편이 정확하다.
