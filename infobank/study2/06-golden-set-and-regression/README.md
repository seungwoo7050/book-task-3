# Stage 06 Golden Regression

golden case, replay runner, version compare input manifest를 분리한 regression pack이다.

## Stage Question

개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?

## Current Implementation

- 구현됨: golden assertion, replay summary and compare manifest
- staged/known gap: DB-backed dashboard 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/data/golden_cases.json`
- `python/data/compare_manifest.json`
- `python/src/stage06/regression.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
