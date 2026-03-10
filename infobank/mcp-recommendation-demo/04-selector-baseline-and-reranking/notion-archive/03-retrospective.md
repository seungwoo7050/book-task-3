# Selector Baseline & Reranking — 회고

## 잘 된 것

### baseline → reranker 분리가 점진적 개선을 가능하게 했다

v0에서 baseline만으로 데모를 보여주고,
v1에서 reranker를 추가하면서 relevance +0.13, rankAccuracy +0.17 개선을 수치로 증명했다.
이건 "코드를 바꿨더니 좋아졌다"를 eval이 보여주는 것이다.

### compare runner가 의사결정 근거가 된다

"reranker를 도입할까?"라는 질문에 compare 결과로 답할 수 있다.
숫자 없이는 판단이 주관적이 되지만, compare가 있으면 객관적이다.

## 아쉬운 것

### keyword 매칭의 근본적 한계

"스키마 확인"이라고 했을 때 "postgres-schema-mapper"는 잡히지만,
"테이블 구조 분석"이라고 하면 keyword가 안 맞아서 놓친다.
embedding 기반 semantic search가 이상적이지만, 이 프로젝트 범위 밖이다.

### signal 데이터가 seed에 의존한다

실제 usage, feedback 데이터가 없으므로 signal의 효과를 현실적으로 검증하기 어렵다.
