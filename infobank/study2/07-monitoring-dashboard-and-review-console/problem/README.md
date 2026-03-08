# Stage 07 Monitoring Console Problem

overview, failures, session review, eval runner, version compare를 보여주는 API와 React UI를 stage 단위로 집중 분리한 단계다.

## Stage Question

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## Inputs

- overview/failure/session/version compare snapshot payload
- React dashboard pages와 mocked tests

## Required Output

- FastAPI snapshot endpoints
- React pages for overview, failures, session review, eval runner
- version compare UI and mocked integration tests

## Success Criteria

- 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.
- backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.
- run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`, `cd react && pnpm test --run`
