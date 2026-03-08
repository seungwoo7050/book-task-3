# Stage 05 Judge And Score Docs

judge 결과와 rubric merge를 분리해 품질 판단과 점수 계산의 경계를 명확히 만드는 단계다.

## Concept Focus

- judge output schema
- heuristic scoring
- quality axes merge

## Capstone Mapping

- v1의 LLM judge trace와 stage01 rubric contract 사이를 잇는 중간 단계다.
- 추후 provider가 바뀌어도 merge contract는 유지된다는 점을 보여준다.

## Implementation Snapshot

- 구현됨: heuristic judge, score merge contract
- staged/known gap: LLM adapter 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 failure가 없는 응답의 total score와 empty failure types를 검증한다.
- 이 stage는 live provider 품질보다 interface boundary를 보는 것이 목적이다.
