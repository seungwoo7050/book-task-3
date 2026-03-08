# Stage 01 Quality Rubric Docs

상담 품질 평가의 점수 계약을 독립적으로 고정해 이후 judge와 dashboard가 같은 숫자 언어를 쓰도록 만드는 단계다.

## Concept Focus

- weighted rubric 설계
- critical override와 grade band의 분리
- judge 출력과 final score merge 계약

## Capstone Mapping

- v0~v2 모두 같은 scoring vocabulary를 사용한다.
- dashboard overview의 평균 점수와 grade 분포는 이 contract를 전제로 해석된다.

## Implementation Snapshot

- 구현됨: weighted rubric, critical override score contract
- staged/known gap: LLM judge 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 weight sum, critical override, high-score grade band를 검증한다.
- 이 단계는 LLM judge 품질이 아니라 merge contract 안정성을 검증한다.
