# Stage 07 Monitoring Console

overview/failures/session review/eval runner/version compare를 보여주는 focused API + React pack이다.

## Stage Question

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## Current Implementation

- 구현됨: FastAPI snapshot endpoints, React dashboard pages and mocked tests
- staged/known gap: 실제 DB persistence 없음
- problem/은 원문 범위와 stage goal을 설명한다.
- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.

## Key Paths

- `python/src/stage07/app.py`
- `python/tests/test_api.py`
- `react/src/pages/Overview.tsx`
- `react/src/pages/SessionReview.tsx`

## Commands

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
- `cd react && pnpm test --run`
