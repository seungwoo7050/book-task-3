# 03-rule-and-guardrail-engine-python 문제지

## 왜 중요한가

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?

## 목표

시작 위치의 구현을 완성해 mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다, LLM 없이도 재현 가능한 deterministic regression이 가능하다, 후속 score merge에서 compliance 축을 해석할 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/src/stage03/__init__.py`
- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/src/stage03/guardrails.py`
- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/tests/test_guardrails.py`
- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/data/rules.json`
- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/src/stage03/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.
- LLM 없이도 재현 가능한 deterministic regression이 가능하다.
- 후속 score merge에서 compliance 축을 해석할 수 있다.

## 제외 범위

- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/data/rules.json` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `load_rules`와 `evaluate`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_mandatory_notice_rule`와 `test_forbidden_promise_rule`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/data/rules.json` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-rule-and-guardrail-engine-python_answer.md`](03-rule-and-guardrail-engine-python_answer.md)에서 확인한다.
