# Stage 05 Judge And Score

judge output와 weighted score merge를 분리한 pack이다.

## Stage Question

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?

## Current Implementation

- 구현됨: heuristic judge, score merge contract
- staged/known gap: LLM adapter 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/src/stage05/judge.py`
- `python/tests/test_judge.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
