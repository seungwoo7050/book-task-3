# 03 규칙 엔진과 가드레일

## 이 stage의 문제

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할지 정리한다.

## 입력/제약

- 입력: mandatory notice, forbidden promise, PII, escalation rule
- 제약: LLM 없이도 deterministic rule match로 재현 가능해야 한다.

## 이 stage의 답

- rule matcher와 failure code를 독립 룰 엔진으로 분리한다.
- dashboard failures와 regression assertion이 같은 failure vocabulary를 사용하게 만든다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/03-rule-and-guardrail-engine/python/src/stage03/guardrails.py`
- `projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/rules/mandatory_notices.yaml`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- YAML loader와 production rule distribution은 축소되어 있다.
- evidence verification과 score merge는 아직 포함하지 않는다.
