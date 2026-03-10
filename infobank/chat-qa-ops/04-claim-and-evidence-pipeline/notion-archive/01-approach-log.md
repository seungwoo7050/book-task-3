# Claim & Evidence Pipeline — 접근 방식: extraction과 verification의 분리

## 핵심 결정

### 1. claim extraction과 evidence verification을 별도 함수로 분리

`extract_claims()`는 답변 텍스트를 받아 claim 목록을 반환한다.
`verify_claims()`는 claim 목록과 KB를 받아 각 claim의 verdict를 반환한다.

왜 분리했는가? trace가 **어느 단계에서 생성되는지** 분리해야 디버깅과 교체가 쉽기 때문이다.
claim extraction 로직을 바꿔도 verification은 영향받지 않고, 반대도 마찬가지다.

실제로 capstone에서는 extraction을 더 정교하게(복합 문장 분리, 불필요한 인사말 제거) 바꿨지만,
verification의 trace schema는 이 stage에서 정한 것을 그대로 사용했다.

### 2. 근거 없는 claim도 결과에서 제거하지 않고 `not_found`로 남김

처음 구현에서는 matched docs가 없는 claim을 결과 리스트에서 빼버렸다.
논리적으로 "근거가 없으니 보여줄 것도 없다"고 생각했기 때문이다.

그런데 이렇게 하면 **왜 groundedness가 낮은지 설명할 수 없다**.
claim이 5개인데 결과가 3개만 나오면, "나머지 2개는 어디 갔지?"가 된다.
빠진 claim이 실은 가장 중요한 실패 원인일 수 있다.

그래서 모든 claim에 대해 verdict를 남기되, 근거가 없으면 `not_found` verdict와 빈 docs list를 포함하도록 바꿨다.

## 선택하지 않은 방향

- **답변 전체를 하나의 groundedness score로 압축하는 방식**: 어떤 문장이 문제인지 모르면 개선할 수 없다.
- **retrieval trace 없이 evidence doc id만 남기는 방식**: 왜 그 문서가 선택됐는지(어떤 query를 썼는지) 모르면 retrieval 품질 디버깅이 불가능하다.

## 이 선택이 후속 stage에 미친 영향

- session review 페이지가 보여주는 provenance 데이터의 핵심 구조는 이 stage에서 정의됐다.
- judge(stage 05)가 groundedness를 해석할 때, claim별 verdict를 aggregate하는 방식으로 사용한다.
- v1의 evidence verifier는 이 trace schema를 확장한 것이다.
