# Stage 02 Python

fixture와 harness만 따로 검증하는 소형 구현이다.

- build: `UV_PYTHON=python3.12 uv sync`
- test: `UV_PYTHON=python3.12 uv run pytest -q`
- current status: verified
- known gaps: 실제 DB persistence 없음
