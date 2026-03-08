# Stage 01 Quality Rubric

weighted score, grade band, critical override를 독립 패키지로 분리한 rubric contract pack이다.

## Stage Question

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?

## Current Implementation

- 구현됨: weighted rubric, critical override score contract
- staged/known gap: LLM judge 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/src/stage01/rubric.py`
- `python/tests/test_rubric.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
