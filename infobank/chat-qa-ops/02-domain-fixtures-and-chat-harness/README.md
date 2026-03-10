# 02 도메인 픽스처와 리플레이 하니스

seeded KB, sample conversations, replay harness를 작은 deterministic harness로 재현한 stage pack이다.

## 이 단계에서 답할 질문

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: seeded KB loader, deterministic replay harness
- 이 pack에 포함하지 않은 범위: database 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/data/knowledge_base/`
- `python/data/replay_sessions.json`
- `python/src/stage02/harness.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- v0의 replay harness와 seeded KB를 축소한 학습용 집중 구현본이다.
- v1/v2의 golden replay도 입력 fixture 분리가 핵심이다.
