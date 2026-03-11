> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Selection Rubric & Eval Contract — 접근 기록

## rubric 축 선정 과정

처음에는 축이 6개였다: relevance, rank, coverage, diversity, latency, explanation quality.
이 중 latency와 explanation quality를 제거했다.

latency 제거 이유: seed 데이터 기반이라 실제 응답 시간을 측정할 수 없다.
explanation quality 제거 이유: 주관적 평가가 개입되어 자동화가 어렵다.

최종 4축: relevance, rank accuracy, coverage, diversity.

## Zod schema에서 eval contract 정의

contracts.ts에 `offlineEvalCaseSchema`를 정의했다:

```typescript
const offlineEvalCaseSchema = z.object({
  id: z.string(),
  query: z.string(),
  context: z.record(z.string(), z.unknown()).optional(),
  expected: z.array(z.object({
    toolId: z.string(),
    rank: z.number()
  }))
});
```

이 schema가 곧 eval contract다.
schema를 지키는 한, eval case를 누구든 추가할 수 있고, 평가 로직은 동일하게 동작한다.

## eval-service.ts 구현

v0 capstone에서 eval-service.ts를 구현했다.
핵심 로직:

1. eval case 배열을 순회
2. 각 case의 query로 recommendation-service 호출
3. 반환된 추천 목록의 toolId를 expected와 비교
4. relevance: expected toolId가 추천 목록에 포함되어 있는지
5. rank accuracy: expected rank 1 도구가 실제 1순위인지

결과를 `{ caseId, passed, scores: { relevance, rankAccuracy } }` 형태로 반환한다.

## threshold 결정

v0 baseline selector의 실행 결과를 먼저 확인한 뒤 threshold를 설정했다.
baseline이 이미 통과하는 수준으로 설정하면 의미가 없고,
baseline이 약간 못 미치는 수준으로 설정하면 v1 개선의 동기가 된다.

최종: relevance ≥ 0.7, rank accuracy ≥ 0.5로 설정.
v0 baseline 결과: relevance 0.65, rank accuracy 0.45 — threshold 바로 아래.
