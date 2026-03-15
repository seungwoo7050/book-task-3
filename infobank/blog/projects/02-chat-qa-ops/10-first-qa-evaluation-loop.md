# 첫 QA evaluation loop

이 프로젝트의 첫 강점은 "채점이 된다"가 아니다. 실패를 언제 자르고, 어떤 근거를 남기고, 어떤 lineage를 저장하는지가 파이프라인 안에 분명하게 들어 있다는 점이다. `pipeline.py`를 다시 읽으면 이 프로젝트가 처음부터 마지막 점수보다 trace를 더 중요하게 다뤘다는 사실이 보인다.

## 평가 파이프라인의 첫 기준은 critical failure를 일찍 분기하는 것이었다

`EvaluationPipeline.evaluate_turn()`은 rule evaluation을 먼저 돌리고, critical rule이 있으면 evidence/judge 단계를 아예 short-circuit한다.

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

이 순서가 중요한 이유는 두 가지다.

1. 비용: critical rule을 먼저 자르면 뒤 단계 LLM/evidence 비용을 줄일 수 있다.
2. 설명 가능성: operator가 "왜 탈락했는가"를 더 빨리 읽을 수 있다.

`demo-runbook.md`가 Q&A에서 "왜 Rule -> Evidence -> Judge 순서인가?"를 따로 다루는 것도 같은 이유다. 이 프로젝트는 좋은 답변을 만들어 내는 시스템이 아니라, failure reasoning을 운영자에게 설명하는 시스템에 더 가깝다.

## trace는 부가 로그가 아니라 evaluation row의 일부다

파이프라인은 최종 `Evaluation` row에 다음을 모두 저장한다.

- `rule_results`
- `evidence_results`
- `llm_judgment`
- `lineage_json`
- `provider_trace`
- `retrieval_trace`
- `claim_trace`
- `judge_trace`

즉 이 프로젝트에서 evaluation row는 "score row"가 아니라 audit row다. 나중에 dashboard나 session review가 같은 저장 구조를 다시 읽을 수 있는 이유도 여기 있다.

또 `create_trace_envelope()`와 `LineageRecord`로 `run_label`, `dataset`, `evaluator_version`, `prompt_version`, `kb_version`, `retrieval_version`을 함께 남긴다는 점도 중요하다. 처음부터 regression compare를 위한 lineage 슬롯이 준비돼 있었다는 뜻이다.

## CLI가 먼저 중요한 운영 출구가 된 이유

`cli.main`은 `evaluate`, `report`, `compare`, `preflight`, `demo-proof`를 제공한다. 특히 `evaluate --golden-set`은 golden rows를 실제 conversation/turn/evaluation으로 만들어 assertion까지 붙인다. 따라서 CLI는 단순 디버그 유틸이 아니라 batch evaluation runner이자 proof generator다.

실제 2026-03-14 재실행에서도 `gate-all`은 이 파이프라인을 넓게 검사했다.

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make gate-all
```

결과:

- lint 통과
- mypy: `Success: no issues found in 42 source files`
- MP1 `3 passed`
- MP2 `5 passed`
- MP3 `15 passed`
- MP4 `5 passed`
- MP5 `16 passed`
- frontend `5 passed`

즉 evaluation loop는 단일 Python 테스트가 아니라, MP1~MP5와 frontend review surface까지 걸친 integrity gate로 이미 묶여 있다.

## 이 단계의 결론

`Chat QA Ops`의 첫 전환점은 더 좋은 judge model이 아니었다. rule, evidence, judge, lineage, assertion을 한 evaluation row에 같이 남기는 파이프라인을 먼저 세운 것이었다. 그 기반이 있었기 때문에 다음 단계에서 compare proof와 review console이 같은 언어를 쓸 수 있게 됐다.
