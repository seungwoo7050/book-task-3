> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Selection Rubric & Eval Contract — 회고

## 잘 된 것

### rubric이 버전 간 비교의 기준이 된다

v0, v1, v2를 같은 rubric으로 평가하면, 어떤 축이 개선되었고 어떤 축이 악화되었는지 명확하게 보인다.
이건 chat-qa-ops의 golden set과 같은 역할이다.

### threshold가 개선의 방향을 제시한다

"relevance 0.7을 넘기려면 어떻게 해야 하지?" → reranker 도입 → v1.
구체적인 숫자가 있으니 방향이 명확하다.

## 아쉬운 것

### 4축으로는 추천 품질의 모든 면을 포착하지 못한다

설명 품질(explanation quality)을 제거한 건 맞는 판단이었지만,
사용자 만족도와 관련된 축이 없다.
feedback loop(stage 05)에서 간접적으로 보완한다.
