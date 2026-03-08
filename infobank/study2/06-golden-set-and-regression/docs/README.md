# Stage 06 Golden Regression Docs

golden case, assertion, replay summary, compare manifest를 묶어 baseline과 candidate를 같은 데이터셋 위에서 비교하는 단계다.

## Concept Focus

- golden set assertion
- reason code 기반 regression
- version compare input manifest

## Capstone Mapping

- v1 compare와 v2 improvement report의 최소 구조를 stage 단위로 축소한 것이다.
- evidence miss 감소를 수치로 논증하려면 manifest와 assertion이 함께 있어야 한다.

## Implementation Snapshot

- 구현됨: golden assertion, replay summary and compare manifest
- staged/known gap: DB-backed dashboard 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 golden assertion success와 manifest labels를 함께 검증한다.
- stage 범위는 데이터셋 계약까지이며 dashboard 저장소는 포함하지 않는다.
