# Stage 01 Quality Rubric Problem

상담 품질 평가의 점수 계약을 독립적으로 고정해 이후 judge와 dashboard가 같은 숫자 언어를 쓰도록 만드는 단계다.

## Stage Question

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?

## Inputs

- stage00에서 고정한 QA Ops 문제 정의
- 상담 품질 축인 correctness, groundedness, compliance, resolution, communication
- critical failure가 일반 가중 점수를 덮어써야 한다는 제출 요구

## Required Output

- `python/src/stage01/rubric.py`의 weight/grade band/merge contract
- critical override를 포함한 deterministic tests

## Success Criteria

- weight 총합이 1.0으로 유지된다.
- critical failure는 어떤 점수보다 우선한다.
- grade band가 후속 stage와 capstone에서 재사용 가능하다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
