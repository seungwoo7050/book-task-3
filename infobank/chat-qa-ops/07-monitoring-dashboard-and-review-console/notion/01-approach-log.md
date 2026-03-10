# 07-monitoring-dashboard-and-review-console 접근 기록

## 이 stage의 질문

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## 선택한 방향

- UI를 새로 설계하지 않고 v1 dashboard slice를 stage pack으로 복제했다. 이유: stage 목표가 시각적 재창작이 아니라 운영 콘솔의 정보 구조를 분리 학습하는 데 있기 때문이다.
- backend는 snapshot payload를 반환하는 FastAPI app으로 축소했다. 이유: DB persistence 없이도 화면이 어떤 계약을 기대하는지 설명할 수 있어야 하기 때문이다.

## 제외한 대안

- frontend만 남기고 API contract는 문서로만 설명하는 방식
- stage07에서도 full DB-backed dashboard를 그대로 끌어오는 방식

## 선택 기준

- 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.
- backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.
- run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.

## 커리큘럼 안에서의 역할

- v1 dashboard slice를 그대로 복제해 stage07에서 UI contract를 독립 학습할 수 있게 했다.
- v2 improvement proof가 결국 어떤 화면과 API에서 읽혀야 하는지 보여준다.

## 아직 열어 둔 판단

stage07은 persistent storage 없이 snapshot payload를 보여주므로 실제 운영 데이터 규모나 latency를 검증하지는 않는다.
