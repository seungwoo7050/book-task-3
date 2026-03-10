# 01-quality-rubric-and-score-contract 문제 정의

## 이 stage가 푸는 문제

상담 품질 평가의 점수 계약을 독립적으로 고정해 이후 judge와 dashboard가 같은 숫자 언어를 쓰도록 만드는 단계다.

## 성공 기준

- weight 총합이 1.0으로 유지된다.
- critical failure는 어떤 점수보다 우선한다.
- grade band가 후속 stage와 capstone에서 재사용 가능하다.

## 왜 지금 이 단계를 먼저 보는가

- v0~v2 모두 같은 scoring vocabulary를 사용한다.
- dashboard overview의 평균 점수와 grade 분포는 이 contract를 전제로 해석된다.

## 먼저 알고 있으면 좋은 것

- QA Ops의 목표가 상담 품질을 수치화하고 비교하는 것임을 알아야 한다.

## 확인할 증거

- `python/tests/test_rubric.py` 세 케이스가 점수 contract를 고정한다.
- critical override는 `CRITICAL` grade와 `0.0` total로 정규화된다.

## 아직 남아 있는 불확실성

weight 값 자체가 인간 평가자 합의로 교정된 것은 아니다. 이 단계는 calibration보다 contract freeze가 목적이다.
