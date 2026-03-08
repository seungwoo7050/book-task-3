# Stage 06 Golden Regression Problem

golden case, assertion, replay summary, compare manifest를 묶어 baseline과 candidate를 같은 데이터셋 위에서 비교하는 단계다.

## Stage Question

개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?

## Inputs

- required evidence doc ids를 가진 golden case
- baseline/candidate/dataset을 지정하는 compare manifest

## Required Output

- pass/fail assertion 결과
- reason code 기반 regression 설명
- compare input manifest

## Success Criteria

- golden case는 required evidence 문서를 명시한다.
- assertion 실패는 reason code로 설명된다.
- baseline과 candidate label을 manifest 파일로 고정한다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
