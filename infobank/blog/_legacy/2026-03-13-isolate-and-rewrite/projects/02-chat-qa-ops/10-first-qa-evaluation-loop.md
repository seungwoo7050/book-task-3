# First QA Evaluation Loop

프로젝트 전체에서 보면 이 글은 가장 앞쪽 구간이다. 아직 compare artifact나 self-hosted 운영 얘기로 가지 않고, `v0`가 왜 상담 품질 평가를 replayable pipeline으로 먼저 고정했는지, 그리고 그 baseline을 어떻게 CLI와 gate로 묶었는지까지 따라간다.

구현 순서 요약:

- critical rule violation이 나오면 evidence/judge 전에 short-circuit하는 evaluation pipeline을 먼저 세웠다.
- golden set과 knowledge base를 CLI로 seed하고, 같은 흐름을 evaluation run과 report까지 연결했다.
- 이후 `gate-all`이 lint, type, backend MP, frontend vitest를 한 번에 묶으면서 baseline이 실험이 아니라 운영 루틴이 됐다.

## Day 1

### Session 1

- 당시 목표: 상담 품질을 설명하는 vocabulary보다 먼저, unsafe answer를 어떤 순서로 막고 점수화할지 pipeline 경계를 고정한다.
- 변경 단위: `evaluator/pipeline.py`
- 처음 가설: judge를 모든 turn에 적용해야 품질 평가라고 부를 수 있다고 생각했다.
- 실제 진행: rule engine이 critical violation을 잡으면 evidence verify와 judge call을 건너뛰고, 그 사실을 `short_circuit_reason`으로 evaluation payload에 남겼다.

CLI:

```bash
$ UV_PYTHON=python3.12 make init-db
Database initialized

$ UV_PYTHON=python3.12 make seed-demo
Seed completed kb_upsert=15, golden_upsert=30, golden_total=30
```

이 seed 출력이 중요한 이유는, QA Ops baseline이 추상적인 rubric 문서가 아니라 knowledge base 15건과 golden set 30건으로 바로 재생 가능한 상태라는 점을 보여 주기 때문이다.

핵심 코드는 여기서 시작한다.

```py
rule_results = evaluate_rules(
    user_message=turn.user_message,
    assistant_response=turn.assistant_response,
    rules_dir="backend/rules",
)

if has_critical_rule(rule_results):
    short_circuit = True
    short_circuit_reason = "critical_rule"
    evidence_result = EvidenceResult(groundedness_score=0.0, has_contradiction=False, retrieval_hit_at_k=0.0)
    llm_judgment = LLMJudgment(
        correctness=0.0,
        resolution=0.0,
        communication=0.0,
        escalation_needed=True,
        failure_types=[item.failure_type for item in rule_results],
        explanation="Critical rule violation short-circuit",
        judge_ms=0,
    )
else:
    claims = extract_claims(turn.assistant_response)
    evidence_result = verify_claims(self.session, claims, top_k=3)
```

왜 이 코드가 중요했는가:

QA Ops를 "judge가 몇 점 줬나"로만 읽으면 guardrail은 사후 설명에 그친다. 하지만 여기서는 rule engine이 pipeline 순서를 실제로 바꾼다. 즉 위험한 답변은 점수 계산 이전에 평가 흐름의 경계를 바꿔 버린다.

그리고 aggregate도 느슨하게 처리하지 않는다.

```py
self.session.flush()
self._refresh_conversation_score(turn.conversation_id)
```

이 두 줄은 evaluation row를 conversation 집계보다 먼저 확정한다. 덕분에 turn-level 평가와 session-level score가 따로 놀지 않는다.

새로 배운 것:

- QA Ops baseline은 점수 함수보다 먼저 execution order를 설계하는 일이다.
- "이 답이 위험하다"는 판단은 report 컬럼이 아니라 pipeline 제어 흐름에 들어가야 했다.

### Session 2

- 당시 목표: pipeline을 사람이 다시 누를 수 있는 CLI와 golden-set evaluation으로 바꾼다.
- 변경 단위: `backend/src/cli/main.py`, `python/Makefile`
- 처음 가설: `pytest -q` 한 번이면 baseline 회귀도 충분할 것이라고 봤다.
- 실제 진행: `seed-demo`, `evaluate --golden-set`, `report`, `compare`, `gate-all`을 각각 명령으로 분리하고, golden-set 실행 시 evaluation run과 assertion summary를 같이 남기게 했다.

핵심 코드는 golden set path에서 드러난다.

```py
elif golden_set:
    golden_rows = list(session.scalars(select(GoldenSet).order_by(GoldenSet.id.asc())).all())
    assertions = []
    run = create_evaluation_run(
        session,
        run_label=run_label,
        dataset_name=dataset,
        retrieval_version=retrieval_version,
    )
    for row in golden_rows:
        convo = Conversation(
            id=str(uuid.uuid4()),
            run_id=run.id,
            prompt_version=run.prompt_version,
            kb_version=run.kb_version,
        )
        session.add(convo)
```

왜 이 코드가 중요했는가:

여기서 QA Ops는 "한 번 평가해 본다"가 아니라 "같은 golden set을 run label과 retrieval version을 붙여 다시 돌린다"로 바뀐다. 즉 이후 compare proof의 뼈대가 이미 `v0` CLI 경로 안에서 준비된다.

CLI:

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

검증 신호:

- lint와 mypy가 먼저 막고,
- backend MP1~MP5가 pipeline과 regression path를 쪼개서 검사하고,
- frontend vitest가 review surface까지 같이 묶는다.

새로 배운 것:

baseline이 실제 제품 흐름으로 굳는 순간은 코드가 완성됐을 때가 아니라, 누군가가 `make gate-all`을 다시 눌러도 같은 경로가 살아 있을 때였다.

## 다음

baseline loop가 생긴 뒤의 핵심 문제는 "실험을 어디에 붙일까"가 아니라 "의존성과 retrieval 변경을 어떻게 regression proof로 남길까"가 된다. 다음 글에서는 `v1` provider chain과 `v2` retrieval-v2 compare artifact로 넘어간다.
