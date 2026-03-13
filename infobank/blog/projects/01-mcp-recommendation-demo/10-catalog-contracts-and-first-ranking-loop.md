# catalog contract와 첫 ranking loop

이 글은 `01-mcp-recommendation-demo` 시리즈의 첫 번째 본문이다. 여기서 따라갈 질문은 단순하다. 왜 이 프로젝트는 추천 알고리즘부터 시작하지 않고, catalog와 manifest 계약부터 먼저 세웠을까? 이 질문을 이해하면 이후의 rerank, compare, release gate도 훨씬 자연스럽게 읽힌다.

앞선 `00-series-map.md`가 전체 경로를 보여 줬다면, 이 글은 그중에서도 `v0 -> v1` 구간에 집중한다. 즉 추천 시스템의 "출발점"이 어디였는지, 그리고 그 출발점이 왜 나중의 proof와 운영 흐름까지 받쳐 주게 되었는지를 본다.

먼저 기준이 되는 문서는 `docs/stage-catalog.md`다. 이 문서에 `01-selection-rubric-and-eval-contract`, `02-registry-catalog-and-manifest-schema`, `03-differentiation-and-exposure-design`, `04-selector-baseline-and-reranking`이 차례로 적혀 있다는 건, 이 프로젝트가 추천 결과를 바로 뽑기보다 먼저 평가 기준과 catalog 구조를 고정했다는 뜻이다. 좋은 점은 이 순서가 코드에서도 그대로 보인다는 데 있다.

그 출발점이 드러나는 파일이 `shared/src/catalog.ts`다. 여기서는 추천 후보 하나가 이름과 설명만 가진 항목이 아니라, runtime, compatibility, operational, exposure 메타데이터까지 함께 품고 있다.

아래 블록이 중요한 이유는, 나중에 `compatibility gate`, `release gate`, 한국어 explanation, offline eval이 모두 이 메타데이터를 다시 읽기 때문이다. 다시 말해 이 프로젝트의 첫 구현은 "점수를 잘 매기는 함수"가 아니라, 나중의 모든 판단이 기대게 될 공용 계약이었다.

```ts
compatibility: {
  minimumClientVersion: "1.0.0",
  maximumClientVersion: "2.0.0",
  testedClientVersions: ["1.0.0", "1.1.0", "1.2.0"],
  deprecatedClientVersions: [],
  breakingChanges: []
},
exposure: {
  userFacingSummaryKo: "코드 변경 이유와 근거를 바로 보여주는 저장소 분석기",
```

이제 baseline recommendation으로 내려가면, `node/src/services/recommendation-service.ts`가 이 metadata를 실제 점수와 설명으로 바꾸는 역할을 한다. 여기서 baseline은 query를 토큰화하고, capability, category, locale, compatibility, maturity, freshness를 한 번에 계산한다.

이 블록이 중요한 이유는 점수 그 자체보다, "왜 이 후보가 올라왔는가"를 나중에 설명할 수 있게 만든다는 점에 있다. 사용자가 보는 추천 이유와 offline evaluation이 같은 데이터를 근거로 삼는 구조가 여기서 시작된다.

```ts
const breakdown = {
  intent: calculateIntentScore(queryTokens, entry),
  capability: calculateCapabilityScore(request, entry),
  category: calculateCategoryScore(request, entry),
  locale: calculateLocaleScore(request, entry),
  compatibility: calculateCompatibilityScore(request, entry),
```

특히 좋았던 점은 score만 남기지 않고 `reasons`와 `explanationKo`를 같이 만든 것이다. 그래서 `shared/src/eval.ts`의 offline case도 top-k 적중률만 보는 데서 끝나지 않고, explanation completeness까지 함께 본다. "추천 품질"과 "설명 가능성"이 따로 자라지 않고 같은 metadata를 읽는 구조라는 뜻이다.

그다음 단계가 `node/src/services/rerank-service.ts`다. 여기서 candidate는 baseline top-k를 버리지 않고, usage CTR, accept rate, operator feedback, explanation quality, freshness를 더해 순서를 다시 조정한다.

아래 식이 바로 그 전환점이다. 여기서부터 추천 시스템은 정적인 schema demo를 넘어, 실제 사용 신호를 반영해 우선순위를 바꾸는 구조를 갖게 된다.

```ts
const uplift =
  ctr * 14 + acceptRate * 18 + feedbackAverage * 5 + explanationQuality * 4 + freshness * 2;
```

중요한 이유는 이 프로젝트가 품질 개선을 "새 모델을 붙였다"가 아니라 "실사용 신호가 어떤 방식으로 순위를 밀어 올렸는가"로 설명하게 만들었기 때문이다. `docs/compare-report.md`가 baseline을 `weighted-baseline-v0`, candidate를 `signal-rerank-v1`로 부르는 것도 같은 맥락이다.

이 흐름은 실제 CLI 출력에서도 그대로 확인된다.

```bash
pnpm seed
pnpm test
pnpm eval
```

```text
Seeded 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, and release candidates.
node tests: 9 passed
react tests: 1 passed
top3Recall: 0.9583333333333334
explanationCompleteness: 1
forbiddenHitRate: 0
```

이 출력이 증명하는 것은 단순히 "정답률이 높다"가 아니다. 더 중요한 건 seeded catalog와 offline eval case가 같은 계약을 읽고 있고, 설명 completeness까지 포함해 같은 기준으로 검증되고 있다는 점이다. 그래서 이후에 release gate가 docs 파일 존재 여부까지 검사하더라도, 그 출발점이 흔들리지 않는다.

다음 글에서는 이 ranking loop가 compare, compatibility, release gate, artifact export까지 어떻게 넓어졌는지 본다. 즉 추천 결과를 `운영 승인 가능한 릴리즈 후보`로 바꾸는 과정으로 넘어간다.
