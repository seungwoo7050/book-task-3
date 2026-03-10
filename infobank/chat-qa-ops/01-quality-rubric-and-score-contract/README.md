# 01 품질 기준과 점수 계약

weighted score, grade band, critical override를 독립 패키지로 분리한 rubric contract pack이다.

## 이 단계에서 답할 질문

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: weighted rubric, critical override score contract
- 이 pack에 포함하지 않은 범위: LLM judge 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/src/stage01/rubric.py`
- `python/tests/test_rubric.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- v0~v2 모두 같은 scoring vocabulary를 사용한다.
- dashboard overview의 평균 점수와 grade 분포는 이 contract를 전제로 해석된다.
