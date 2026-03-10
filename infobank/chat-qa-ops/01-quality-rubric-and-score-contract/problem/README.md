# 01 품질 기준과 점수 계약 문제 정의

상담 품질 평가의 점수 계약을 독립적으로 고정해 이후 judge와 dashboard가 같은 숫자 언어를 쓰도록 만드는 단계다.

## 문제 해석

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?

## 입력

- stage00에서 고정한 QA Ops 문제 정의
- 상담 품질 축인 correctness, groundedness, compliance, resolution, communication
- critical failure가 일반 가중 점수를 덮어써야 한다는 제출 요구

## 기대 산출물

- `python/src/stage01/rubric.py`의 weight/grade band/merge contract
- critical override를 포함한 deterministic tests

## 완료 기준

- weight 총합이 1.0으로 유지된다.
- critical failure는 어떤 점수보다 우선한다.
- grade band가 후속 stage와 capstone에서 재사용 가능하다.

## 현재 확인 가능한 증거

- `python/tests/test_rubric.py` 세 케이스가 점수 contract를 고정한다.
- critical override는 `CRITICAL` grade와 `0.0` total로 정규화된다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: weighted rubric, critical override score contract
- 이번 단계에서 일부러 제외한 범위: LLM judge 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
