# 05 judge 결과와 점수 병합

judge output와 weighted score merge를 분리한 pack이다.

## 이 단계에서 답할 질문

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: heuristic judge, score merge contract
- 이 pack에 포함하지 않은 범위: LLM adapter 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/src/stage05/judge.py`
- `python/tests/test_judge.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- v1의 LLM judge trace와 stage01 rubric contract 사이를 잇는 중간 단계다.
- 추후 provider가 바뀌어도 merge contract는 유지된다는 점을 보여준다.
