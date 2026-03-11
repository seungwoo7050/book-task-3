> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Selection Rubric & Eval Contract — 디버그 기록

## eval case 순위 매칭 로직 오류

### 상황

eval에서 expected rank 1 도구가 실제 추천 목록의 2번째에 있을 때,
이걸 "partially correct"로 처리해야 하는지, "incorrect"로 처리해야 하는지 혼란이 있었다.

### 해결

rank accuracy는 strict 매칭으로 결정했다:
- expected rank 1 도구가 실제 1순위 → 1.0
- expected rank 1 도구가 실제 2순위 → 0.0 (rank accuracy 기준)
- 단, relevance 축에서는 "목록에 포함" 여부만 보므로 1.0

이렇게 축별로 기준을 분리하면 "관련은 있지만 순위가 틀린" 케이스를 정확히 포착할 수 있다.

## threshold를 너무 낮게 잡아서 모든 버전이 통과하는 문제

### 상황

초기 threshold를 relevance ≥ 0.5로 설정했더니,
v0 baseline도 쉽게 통과해서 개선 동기가 없어졌다.

### 해결

v0 baseline 결과를 기반으로 threshold를 상향 조정했다:
- relevance: 0.5 → 0.7 (v0이 0.65로 약간 못 미치는 수준)
- rank accuracy: 0.3 → 0.5

이제 v0은 threshold를 통과하지 못하고, v1 reranker 추가 후 통과하게 된다.
