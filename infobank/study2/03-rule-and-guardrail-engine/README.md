# Stage 03 Guardrails

mandatory notice, forbidden promise, PII, escalation rule을 독립 룰 엔진으로 분리한 stage pack이다.

## Stage Question

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?

## Current Implementation

- 구현됨: rule matcher, deterministic guardrail tests
- staged/known gap: YAML loader 대신 JSON 사용
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/data/rules.json`
- `python/src/stage03/guardrails.py`
- `python/tests/test_guardrails.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
