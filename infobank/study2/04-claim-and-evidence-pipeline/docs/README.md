# Stage 04 Claim And Evidence Docs

답변에서 claim을 분리하고 각 claim에 retrieval trace와 verdict trace를 남기는 groundedness 검증 단계를 다룬다.

## Concept Focus

- claim extraction
- retrieval trace
- verdict trace와 evidence document linkage

## Capstone Mapping

- v1에서 추가한 claim trace, retrieval trace, verdict trace contract의 축소판이다.
- session review 페이지가 보여주는 provenance 데이터의 핵심 구조를 먼저 설명한다.

## Implementation Snapshot

- 구현됨: claim trace, retrieval trace and verdict trace
- staged/known gap: LLM provider 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 첫 claim이 `support` verdict와 예상 doc trace를 남기는지 확인한다.
- silent success보다 trace completeness를 더 중요하게 본다.
