# Catalog Contracts And First Ranking Loop

프로젝트 전체에서 보면 이 글은 가장 앞쪽 구간이다. 아직 release gate나 self-hosted 얘기로 가지 않고, `v0`가 왜 manifest contract와 explanation trace를 먼저 고정했는지, 그리고 `v1`가 왜 usage signal을 점수로 끌어오기 시작했는지까지 따라간다.

구현 순서 요약:

- catalog entry를 그냥 JSON 덩어리로 두지 않고 `mcpManifestSchema`와 `recommendationTraceSchema`로 먼저 묶었다.
- 그 계약 위에서 baseline scoring과 한국어 explanation을 같은 함수 묶음 안에서 만들었다.
- 이후 `v1`에서 usage/feedback를 rerank uplift로 합쳐 baseline/candidate compare 질문을 열었다.

## Day 1

### Session 1

- 당시 목표: 어떤 MCP를 추천할지 계산하기 전에, catalog가 반드시 가져야 할 필드와 trace 포맷을 먼저 고정한다.
- 변경 단위: `shared/src/contracts.ts`, `node/src/services/recommendation-service.ts`
- 처음 가설: baseline selector는 keyword score만 있으면 바로 돌릴 수 있을 것 같았다.
- 실제 진행: `mcpManifestSchema`와 `catalogEntrySchema`가 summary, differentiation, compatibility, tested client versions, Korean exposure를 모두 강제하게 했다. 즉 추천 로직보다 먼저 "추천에 써도 되는 metadata가 무엇인가"를 계약으로 만들었다.

CLI:

```bash
$ pnpm db:up
Container study1-v2-postgres Started

$ pnpm migrate
[i] No changes detected

$ pnpm seed
Seeded 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, and release candidates.
```

이 seed 출력이 중요한 이유는, 추천 코드만 채운다고 끝나는 프로젝트가 아니라는 걸 바로 보여 주기 때문이다. catalog entry, eval case, usage signal, release candidate가 한 번에 같이 들어가야 뒤 단계가 살아난다.

핵심 코드는 여기서 시작한다.

```ts
export const mcpManifestSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  summaryKo: z.string().min(10),
  differentiationPoints: z.array(z.string().min(8)).min(2),
  compatibility: z.object({
    minimumClientVersion: z.string().min(1),
    maximumClientVersion: z.string().min(1),
    testedClientVersions: z.array(z.string().min(1)).min(1)
  })
});
```

왜 이 코드가 중요했는가:

추천 시스템을 "점수 함수"로만 보면 나중에 compatibility나 release gate를 붙일 때 metadata가 부족해진다. 이 schema는 `v0`에서 이미 `v2`의 compatibility gate가 읽을 필드를 미리 선언해 둔다는 점에서 전환점이었다.

새로 배운 것:

- catalog metadata는 부가 설명이 아니라 later-stage verification이 다시 읽을 계약이었다.
- Korean summary와 differentiation도 UI copy가 아니라 추천 acceptance의 일부였다.

### Session 2

- 당시 목표: baseline recommendation이 결과 id 목록만 뱉지 않고, 왜 그런 순서가 나왔는지 같은 trace 안에서 설명하게 만든다.
- 변경 단위: `node/src/services/recommendation-service.ts`, `shared/src/eval.ts`
- 처음 가설: top-3 candidate만 맞으면 demo에서는 충분하다고 생각했다.
- 실제 진행: 점수 breakdown과 `reasons` 배열을 trace에 넣고, `buildExplanationKo()`가 capability, differentiation, compatibility를 한 문장으로 이어 붙이게 했다. 그 덕분에 offline eval도 explanation completeness를 별도 acceptance로 볼 수 있게 됐다.

핵심 코드:

```ts
const breakdown = {
  intent: calculateIntentScore(queryTokens, entry),
  capability: calculateCapabilityScore(request, entry),
  category: calculateCategoryScore(request, entry),
  locale: calculateLocaleScore(request, entry),
  compatibility: calculateCompatibilityScore(request, entry),
  maturity: calculateMaturityScore(entry),
  freshness: calculateFreshnessScore(entry)
};

return {
  totalScore: breakdown.intent + breakdown.capability + breakdown.category +
    breakdown.locale + breakdown.compatibility + breakdown.maturity + breakdown.freshness,
  breakdown,
  reasons
};
```

그리고 설명 문자열도 trace에 기대어 만든다.

```ts
return `${entry.name}는 ${capabilityReason} ${differentiationReason} ${compatibilityReason}`;
```

왜 이 코드가 중요했는가:

여기서 추천 결과는 "점수 합"과 "Korean explanation"으로 갈라지지 않는다. 같은 trace를 읽어 둘 다 만든다. 그래서 나중에 `explanationCompleteness`를 eval metric으로 걸 수 있었다.

CLI:

```bash
$ pnpm eval
{
  "metrics": {
    "top3Recall": 0.9583333333333334,
    "explanationCompleteness": 1,
    "forbiddenHitRate": 0
  },
  "acceptance": {
    "top3RecallPass": true,
    "explanationPass": true,
    "forbiddenPass": true
  }
}
```

검증 신호:

- `top3Recall`만 보는 게 아니라 `explanationCompleteness`와 `forbiddenHitRate`가 같이 붙는다.
- 즉 "잘 맞춘 추천"과 "말하면 안 될 걸 안 한 추천"을 한꺼번에 검증한다.

새로 배운 것:

추천 품질은 ranking accuracy만으로 끝나지 않는다. operator가 읽을 explanation이 acceptance에 들어오는 순간, recommendation service는 ranking engine이 아니라 communication contract도 함께 책임지는 코드가 된다.

## Day 2

### Session 1

- 당시 목표: baseline score 위에 실사용 신호를 얹어 candidate ranking을 만들고, baseline과 candidate를 정량적으로 비교한다.
- 변경 단위: `node/src/services/rerank-service.ts`, `node/src/services/compare-service.ts`, `react/components/mcp-dashboard.tsx`
- 처음 가설: baseline 가중치만 조금 다듬으면 개선 여부도 설명할 수 있다고 봤다.
- 실제 진행: usage event와 feedback record를 모아 CTR, acceptRate, feedbackAverage를 만들고, 이 값을 uplift로 합산하는 reranker를 추가했다. compare는 nDCG@3과 top1 hit를 baseline/candidate로 나란히 계산했다.

핵심 코드:

```ts
const ctr = signal.clicks / impressions;
const acceptRate = signal.accepts / impressions;
const feedbackAverage =
  signal.feedbackCount > 0 ? signal.feedbackTotal / signal.feedbackCount : 0;
const uplift =
  ctr * 14 + acceptRate * 18 + feedbackAverage * 5 + explanationQuality * 4 + freshness * 2;

const trace: RecommendationTrace = {
  candidateId: candidate.catalogId,
  totalScore: rescored.totalScore + uplift,
  breakdown: rescored.breakdown,
  reasons: [
    ...candidate.trace.reasons,
    {
      type: "maturity",
      label: "rerank-signal",
      score: uplift,
      detailKo: `실사용 신호(CTR ${(ctr * 100).toFixed(0)}%, accept ${(acceptRate * 100).toFixed(0)}%, feedback ${feedbackAverage.toFixed(1)})가 candidate 점수를 끌어올립니다.`
    }
  ]
};
```

왜 이 코드가 중요했는가:

`v1`의 핵심은 새 모델을 들여오는 게 아니라, 기존 baseline trace를 버리지 않고 그 위에 운영 신호를 덧입힌다는 점이었다. recommendation logic이 두 개로 갈라지는 대신 baseline과 candidate가 같은 contract를 공유하게 됐다.

CLI:

```bash
$ pnpm test
node test:  Test Files  6 passed (6)
node test:       Tests  9 passed (9)
react test: Test Files  1 passed (1)
react test:      Tests  1 passed (1)
```

검증 신호:

- `rerank-service.test.ts`와 `routes.integration.test.ts`가 candidate ranking path를 지키고,
- `mcp-dashboard.test.tsx`가 compare snapshot이 UI 표면에도 연결되는지 확인한다.

새로 배운 것:

실사용 신호를 recommendation logic에 넣는다고 해서 baseline을 버리는 건 아니다. 오히려 baseline trace를 남겨 둬야 compare가 "어디서 얼마만큼 좋아졌는가"를 설명할 수 있다.

다음:

candidate ranking이 생긴 순간부터는 "더 좋아 보인다"만으로는 release를 열 수 없게 된다. 다음 글에서는 compare uplift를 compatibility, release gate, artifact export까지 이어 붙이는 구간으로 넘어간다.
