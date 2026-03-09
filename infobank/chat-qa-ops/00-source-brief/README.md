# Stage 00 Source Brief

문제 정의, reference spine, scope contract를 코드 객체로 정리한 source brief pack이다.

## Stage Question

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?

## Current Implementation

- 구현됨: reference source manifest, project selection rationale snapshot
- staged/known gap: capstone runtime 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/src/stage00/source_brief.py`
- `python/tests/test_source_brief.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
