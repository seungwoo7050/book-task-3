# Usage Logs, Metrics & Feedback Loop — 회고

## 잘 된 것

### feedback loop가 reranker signal을 실제 데이터로 채운다

stage 04에서 reranker가 사용하는 usage_count, avg_feedback이
이 stage에서 기록된 데이터에서 온다.
파이프라인이 연결된 것이다.

### experiment 메타데이터가 A/B 비교를 가능하게 한다

같은 기간에 baseline과 reranker를 동시에 실행하고,
experiment 단위로 feedback을 분리해서 비교하면
"reranker가 실제로 사용자 만족도를 높이는가?"에 답할 수 있다.

## 아쉬운 것

### 실제 사용 데이터가 없다

모든 데이터가 seed이다. 실제 usage pattern이나 feedback 분포를 반영하지 못한다.
v3에서 실제 사용자 인증을 추가했지만, 여전히 시뮬레이션 수준이다.

### metrics 집계가 실시간이 아니다

도구별 usage/feedback 요약은 API 호출 시점에 DB를 쿼리한다.
사용량이 많아지면 성능 문제가 될 수 있다.
캐싱이나 materialized view는 범위 밖이다.
