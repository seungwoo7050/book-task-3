# Python 구현 안내

답변 문장을 claim 단위로 분해하고, 각 claim이 어떤 문서로 뒷받침되는지 trace를 남긴다. groundedness를 설명 가능한 형태로 다루는 최소 구현이다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. claim extraction과 retrieval trace 보존이 pytest로 확인된다.
- 남은 범위: vector DB나 live retrieval provider는 이 pack에 포함하지 않는다.

## 먼저 볼 파일

- `src/stage04/pipeline.py`
- `tests/test_pipeline.py`
