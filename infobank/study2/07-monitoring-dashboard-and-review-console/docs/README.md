# Stage 07 Monitoring Console Docs

overview, failures, session review, eval runner, version compare를 보여주는 API와 React UI를 stage 단위로 집중 분리한 단계다.

## Concept Focus

- snapshot API
- dashboard information architecture
- session review trace surfacing
- baseline/candidate version compare

## Capstone Mapping

- v1 dashboard slice를 그대로 복제해 stage07에서 UI contract를 독립 학습할 수 있게 했다.
- v2 improvement proof가 결국 어떤 화면과 API에서 읽혀야 하는지 보여준다.

## Implementation Snapshot

- 구현됨: FastAPI snapshot endpoints, React dashboard pages and mocked tests
- staged/known gap: 실제 DB persistence 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
- `cd react && pnpm test --run`

## Notes

- Python pack은 snapshot endpoint contract를 테스트한다.
- React pack은 mocked Vitest로 overview, failures, session review, eval runner, compare UI를 검증한다.
