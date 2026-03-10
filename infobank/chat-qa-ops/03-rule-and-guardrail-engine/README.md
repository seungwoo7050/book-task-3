# 03 규칙 엔진과 가드레일

mandatory notice, forbidden promise, PII, escalation rule을 독립 룰 엔진으로 분리한 stage pack이다.

## 이 단계에서 답할 질문

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: rule matcher, deterministic guardrail tests
- 이 pack에 포함하지 않은 범위: YAML loader 대신 JSON 사용
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/data/rules.json`
- `python/src/stage03/guardrails.py`
- `python/tests/test_guardrails.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- v0에서 추가한 escalation rule과 MP2 guardrail tests를 축소한 pack이다.
- failure codes는 dashboard failures 페이지와 golden set assertion의 공통 언어가 된다.
