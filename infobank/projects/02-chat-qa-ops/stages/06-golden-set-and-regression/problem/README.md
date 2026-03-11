# 06 골든셋과 회귀 검증 문제 정의

golden case, assertion, replay summary, compare manifest를 묶어 baseline과 candidate를 같은 데이터셋 위에서 비교하는 단계다.

## 문제 해석

개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?

## 입력

- required evidence doc ids를 가진 golden case
- baseline/candidate/dataset을 지정하는 compare manifest

## 기대 산출물

- pass/fail assertion 결과
- reason code 기반 regression 설명
- compare input manifest

## 완료 기준

- golden case는 required evidence 문서를 명시한다.
- assertion 실패는 reason code로 설명된다.
- baseline과 candidate label을 manifest 파일로 고정한다.

## 현재 확인 가능한 증거

- `python/tests/test_regression.py`가 golden assertion과 compare manifest를 확인한다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: golden assertion, replay summary and compare manifest
- 이번 단계에서 일부러 제외한 범위: DB-backed dashboard 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
