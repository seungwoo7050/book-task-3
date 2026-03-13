# 첫 QA evaluation loop

이 글은 `02-chat-qa-ops` 시리즈의 출발점이다. 여기서 따라갈 질문은 명확하다. 상담 품질 평가는 어떻게 "그럴듯한 판단"이 아니라, 다시 실행해도 같은 흐름을 따라갈 수 있는 파이프라인이 되었을까?

앞선 `00-series-map.md`가 전체 경로를 보여 줬다면, 이 글은 `v0 -> v1` 구간에 집중한다. 즉 rule, evidence, judge, scoring이 어떤 순서로 묶였는지, 그리고 왜 그 순서가 운영 관점에서도 중요했는지를 본다.

가장 먼저 봐야 할 파일은 `python/backend/src/evaluator/pipeline.py`다. 이 프로젝트의 핵심은 모델을 한 번 부르는 것이 아니라, 실패를 얼마나 일찍 구분하고 어떤 trace를 남기며 점수로 합치는가에 있다.

아래 코드가 중요한 이유는, 이 프로젝트가 처음부터 "마지막 점수"보다 "판단이 어떻게 흘렀는가"를 남기는 구조를 택했다는 점을 보여 주기 때문이다.

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

이 순서가 중요한 이유는 `docs/demo/demo-runbook.md`의 Q&A에도 드러난다. 왜 Rule -> Evidence -> Judge 순서냐는 질문에 대한 답이 바로 비용 절감과 failure 명확성이다. critical rule을 먼저 자르면 뒤 단계의 비용을 아낄 수 있고, operator는 "무엇 때문에 탈락했는가"를 더 빨리 읽을 수 있다.

같은 판단은 CLI surface에도 이어진다. `python/backend/src/cli/main.py`의 `evaluate`, `report`, `compare` 명령은 모두 이 파이프라인이 만든 evaluation row를 다시 읽어, 사람이 바로 확인할 수 있는 표와 숫자로 바꾼다. 중요한 이유는 여기서 첫 운영 경험이 웹 대시보드보다 CLI에서 먼저 굳어졌기 때문이다.

실제 integrity gate를 다시 돌려 보면 이 구조가 얼마나 넓게 테스트되는지도 바로 보인다.

```bash
UV_PYTHON=python3.12 make gate-all
```

```text
Lint: passed
Mypy: no issues found in 42 source files
MP1: 3 passed
MP2: 5 passed
MP3: 15 passed
MP4: 5 passed
MP5: 16 passed
Frontend: 5 passed
Integrity gate passed for target=all
```

이 출력이 증명하는 것은 테스트가 많이 돈다는 사실만이 아니다. `MP1~MP5`처럼 학습 단위를 integrity gate에 그대로 남겨 두었기 때문에, 이후의 regression compare를 설명할 때도 "어디가 좋아졌는가"를 단계별 언어로 다시 짚을 수 있다.

또 하나 좋은 점은 dashboard가 CLI의 경쟁자가 아니라는 점이다. `python/backend/src/api/routes/dashboard.py`는 evaluation row를 평균 점수, critical count, failure top, version compare 결과로 다시 조립한다. 즉 CLI와 dashboard는 서로 다른 진실을 말하는 것이 아니라, 같은 저장 구조를 다른 형태로 보여 주는 두 개의 출구다.

첫 evaluation loop를 이 프로젝트의 출발점으로 보는 이유도 여기 있다. 좋은 챗봇 답변을 만드는 것만으로는 QA Ops가 되지 않는다. rule, evidence, judge, lineage, assertion이 한 번의 실행 안에서 함께 남아야, 그다음 단계인 golden regression과 운영 review가 가능해진다.

다음 글에서는 바로 그 regression proof 단계로 넘어간다. baseline과 candidate의 차이를 어떻게 `84.06 -> 87.76`, `critical 2 -> 0` 같은 수치로 고정했는지 본다.
