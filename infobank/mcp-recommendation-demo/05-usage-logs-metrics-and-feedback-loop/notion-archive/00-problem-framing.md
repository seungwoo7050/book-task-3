# Usage Logs, Metrics & Feedback Loop — 문제 정의

## 풀어야 하는 문제

stage 04에서 reranker의 signal로 usage_count와 avg_feedback을 사용한다.
그런데 이 데이터는 어디서 오는가?

현재까지 추천 결과가 실제로 사용되었는지, 사용자가 만족했는지를 기록하는 메커니즘이 없다.
**feedback loop가 없으면 reranker는 허공에 떠 있는 것이다.**

## 세 가지 데이터 흐름

1. **Usage event**: 도구가 실제로 선택/실행된 기록
   - 누가, 언제, 어떤 도구를, 어떤 추천에서 선택했는지

2. **Feedback**: 도구 사용 후 만족도 평가
   - 1~5점 스케일, 선택적 코멘트

3. **Experiment metadata**: A/B 테스트나 알고리즘 변경 시 실험 정보
   - 어떤 selector/reranker 조합인지, 실험 기간, 대상 그룹

## 왜 experiment를 따로 관리하는가

같은 기간에 baseline과 reranker를 같이 쓰면,
어떤 추천 결과가 어떤 알고리즘에서 나온 건지 분리해야 한다.

experiment는 이 분리를 가능하게 하는 메타데이터다.
대시보드에서 experiment 단위로 필터링하면,
"A 알고리즘의 feedback 평균"과 "B 알고리즘의 feedback 평균"을 비교할 수 있다.
