# Stage 03 Guardrails Problem

mandatory notice, forbidden promise, PII, escalation 규칙을 deterministic failure code로 환원하는 단계다.

## Stage Question

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?

## Inputs

- 해지/환불/명의변경 시 본인확인이 필요하다는 도메인 규칙
- 과장 약속, PII 노출, 민원/분쟁 escalation 조건

## Required Output

- `python/data/rules.json` rule set
- `python/src/stage03/guardrails.py` 룰 엔진
- failure type별 pytest

## Success Criteria

- mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.
- LLM 없이도 재현 가능한 deterministic regression이 가능하다.
- 후속 score merge에서 compliance 축을 해석할 수 있다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
