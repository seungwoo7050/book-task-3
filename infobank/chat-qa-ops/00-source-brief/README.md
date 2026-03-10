# 00 문제 정의와 방향 고정

문제 정의, reference spine, scope contract를 코드 객체로 정리한 source brief pack이다.

## 이 단계에서 답할 질문

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: reference source manifest, project selection rationale snapshot
- 이 pack에 포함하지 않은 범위: capstone runtime 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/src/stage00/source_brief.py`
- `python/tests/test_source_brief.py`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## 포트폴리오로 가져갈 포인트

- `08/v0`를 기준점으로 삼는 이유를 stage 단위에서 먼저 고정한다.
- 이후 모든 README와 verification 문서는 이 source brief를 따라야 한다.
