# Stage 05 Judge And Score Problem

judge 결과와 rubric merge를 분리해 품질 판단과 점수 계산의 경계를 명확히 만드는 단계다.

## Stage Question

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?

## Inputs

- user message
- assistant response
- failure types
- groundedness와 compliance 서브스코어

## Required Output

- judge result dictionary
- weighted final score

## Success Criteria

- judge와 scorer가 별도 함수 계약을 가진다.
- failure types는 판단 결과와 최종 score 계산 모두에 반영된다.
- live provider가 없어도 deterministic 테스트가 가능하다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
