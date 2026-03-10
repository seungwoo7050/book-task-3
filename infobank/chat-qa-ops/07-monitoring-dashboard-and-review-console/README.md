# 07 운영 대시보드와 리뷰 콘솔

overview/failures/session review/eval runner/version compare를 보여주는 focused API + React pack이다.

## 이 단계에서 답할 질문

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## 지금 구현된 범위

- 실제로 확인할 수 있는 구현: FastAPI snapshot endpoints, React dashboard pages and mocked tests
- 이 pack에 포함하지 않은 범위: 실제 DB persistence 없음
- `problem/`은 문제 해석과 완료 기준을 고정한다.
- `docs/`는 오래 남길 개념과 검증 메모를 정리한다.

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `python/src/stage07/app.py`
- `python/tests/test_api.py`
- `react/src/pages/Overview.tsx`
- `react/src/pages/SessionReview.tsx`

## 실행 및 검증

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
- `cd react && pnpm test --run`

## 포트폴리오로 가져갈 포인트

- v1 dashboard slice를 그대로 복제해 stage07에서 UI contract를 독립 학습할 수 있게 했다.
- v2 improvement proof가 결국 어떤 화면과 API에서 읽혀야 하는지 보여준다.
