# 07-monitoring-dashboard-and-review-console 문제 정의

## 이 stage가 푸는 문제

overview, failures, session review, eval runner, version compare를 보여주는 API와 React UI를 stage 단위로 집중 분리한 단계다.

## 성공 기준

- 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.
- backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.
- run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.

## 왜 지금 이 단계를 먼저 보는가

- v1 dashboard slice를 그대로 복제해 stage07에서 UI contract를 독립 학습할 수 있게 했다.
- v2 improvement proof가 결국 어떤 화면과 API에서 읽혀야 하는지 보여준다.

## 먼저 알고 있으면 좋은 것

- run label, retrieval version, failure taxonomy, score contract를 이미 알고 있어야 콘솔이 읽힌다.

## 확인할 증거

- `python/tests/test_api.py`가 overview, failures, conversation detail, golden run, version compare endpoint를 검증한다.
- `react` pack은 copied mocked tests로 주요 화면을 검증한다.

## 아직 남아 있는 불확실성

stage07은 persistent storage 없이 snapshot payload를 보여주므로 실제 운영 데이터 규모나 latency를 검증하지는 않는다.
