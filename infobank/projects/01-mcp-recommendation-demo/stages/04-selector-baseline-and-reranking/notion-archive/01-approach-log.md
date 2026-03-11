> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Selector Baseline & Reranking — 접근 기록

## weighted baseline 구현

recommendation-service.ts에 baseline selector를 구현했다.

핵심 로직:
1. query를 토큰화 (공백 분리)
2. 각 도구에 대해 category/description 매칭 점수 계산
3. 가중치: category match(0.4) + description keyword match(0.3) + name match(0.3)
4. 점수 상위 N개 반환

이 방식의 한계는 알고 있었다: 키워드 매칭은 의미적 유사성을 포착하지 못한다.
하지만 seed 데이터가 deterministic이므로, 키워드 매칭만으로도 합리적인 결과를 낼 수 있다.

## signal-based reranker

v1에서 rerank-service.ts를 추가했다.

reranker가 사용하는 signal:
1. **usage_count**: 해당 도구가 실제로 사용된 횟수 → 많이 쓰이는 도구 우선
2. **avg_feedback**: 사용자 피드백 평균 점수 → 높은 피드백 도구 우선
3. **days_since_update**: 마지막 업데이트 이후 경과 일수 → 최신 도구 우선
4. **compat_score**: 사용자의 현재 도구 셋과의 호환성 → 호환되는 도구 우선

각 signal에 가중치를 곱하고 baseline 점수에 더한다:

```typescript
finalScore = baselineScore * 0.6 
  + usageSignal * 0.15 
  + feedbackSignal * 0.10 
  + recencySignal * 0.05 
  + compatSignal * 0.10;
```

## compare-service 구현

compare-service.ts에서 baseline과 reranker를 같은 eval case로 실행하고 결과를 비교한다.

출력 형태:
```json
{
  "baseline": { "relevance": 0.65, "rankAccuracy": 0.45 },
  "reranker": { "relevance": 0.78, "rankAccuracy": 0.62 },
  "delta": { "relevance": +0.13, "rankAccuracy": +0.17 }
}
```
