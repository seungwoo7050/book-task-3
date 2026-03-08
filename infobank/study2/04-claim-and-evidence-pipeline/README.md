# Stage 04 Claim And Evidence

claim extraction, retrieval trace, verdict trace를 남기는 evidence pipeline pack이다.

## Stage Question

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?

## Current Implementation

- 구현됨: claim trace, retrieval trace and verdict trace
- staged/known gap: LLM provider 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/src/stage04/pipeline.py`
- `python/tests/test_pipeline.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
