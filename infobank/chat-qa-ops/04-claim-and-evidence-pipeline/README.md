# 04 주장-근거 추적 파이프라인

claim extraction, retrieval trace, verdict trace를 남기는 evidence pipeline pack이다.

## 이 단계에서 답할 질문

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: claim trace, retrieval trace and verdict trace
- 이 pack에 포함하지 않은 범위: LLM provider 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/src/stage04/pipeline.py`
- `python/tests/test_pipeline.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- v1에서 추가한 claim trace, retrieval trace, verdict trace contract의 축소판이다.
- session review 페이지가 보여주는 provenance 데이터의 핵심 구조를 먼저 설명한다.
