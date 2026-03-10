# 06-golden-set-and-regression 문제 정의

## 이 stage가 푸는 문제

golden case, assertion, replay summary, compare manifest를 묶어 baseline과 candidate를 같은 데이터셋 위에서 비교하는 단계다.

## 성공 기준

- golden case는 required evidence 문서를 명시한다.
- assertion 실패는 reason code로 설명된다.
- baseline과 candidate label을 manifest 파일로 고정한다.

## 왜 지금 이 단계를 먼저 보는가

- v1 compare와 v2 improvement report의 최소 구조를 stage 단위로 축소한 것이다.
- evidence miss 감소를 수치로 논증하려면 manifest와 assertion이 함께 있어야 한다.

## 먼저 알고 있으면 좋은 것

- stage02 fixture/replay, stage04 evidence doc contract를 이해해야 한다.

## 확인할 증거

- `python/tests/test_regression.py`가 golden assertion과 compare manifest를 확인한다.

## 아직 남아 있는 불확실성

이 pack은 sample-size가 작아 통계적 의미를 주장하기보다 compare 구조를 설명하는 데 초점이 있다.
