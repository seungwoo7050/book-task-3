# 07 운영 대시보드와 리뷰 콘솔 문제 정의

overview, failures, session review, eval runner, version compare를 보여주는 API와 React UI를 stage 단위로 집중 분리한 단계다.

## 문제 해석

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## 입력

- overview/failure/session/version compare snapshot payload
- React dashboard pages와 mocked tests

## 기대 산출물

- FastAPI snapshot endpoints
- React pages for overview, failures, session review, eval runner
- version compare UI and mocked integration tests

## 완료 기준

- 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.
- backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.
- run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.

## 현재 확인 가능한 증거

- `python/tests/test_api.py`가 overview, failures, conversation detail, golden run, version compare endpoint를 검증한다.
- `react` pack은 copied mocked tests로 주요 화면을 검증한다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: FastAPI snapshot endpoints, React dashboard pages and mocked tests
- 이번 단계에서 일부러 제외한 범위: 실제 DB persistence 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`, `cd react && pnpm test --run`
