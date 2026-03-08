# Stage 02 Fixtures And Harness

seeded KB, sample conversations, replay harness를 작은 deterministic harness로 재현한 stage pack이다.

## Stage Question

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?

## Current Implementation

- 구현됨: seeded KB loader, deterministic replay harness
- staged/known gap: database 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/data/knowledge_base/`
- `python/data/replay_sessions.json`
- `python/src/stage02/harness.py`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
