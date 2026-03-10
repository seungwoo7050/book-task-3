# 06 골든셋과 회귀 검증

golden case, replay runner, version compare input manifest를 분리한 regression pack이다.

## 이 단계에서 답할 질문

개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: golden assertion, replay summary and compare manifest
- 이 pack에 포함하지 않은 범위: DB-backed dashboard 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/data/golden_cases.json`
- `python/data/compare_manifest.json`
- `python/src/stage06/regression.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- v1 compare와 v2 improvement report의 최소 구조를 stage 단위로 축소한 것이다.
- evidence miss 감소를 수치로 논증하려면 manifest와 assertion이 함께 있어야 한다.
