# Stage 04 Claim And Evidence Problem

답변에서 claim을 분리하고 각 claim에 retrieval trace와 verdict trace를 남기는 groundedness 검증 단계를 다룬다.

## Stage Question

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?

## Inputs

- assistant response text
- seeded knowledge base 또는 doc_id -> content 매핑

## Required Output

- claim list
- claim별 `support` 또는 `not_found` verdict
- retrieval trace와 evidence_doc_ids

## Success Criteria

- 각 claim 결과에 retrieval query와 matched docs가 남는다.
- 근거가 없는 문장도 `not_found`로 기록되어 silent drop이 없다.
- 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
