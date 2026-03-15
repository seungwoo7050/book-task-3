# catalog contract와 첫 ranking loop

이 프로젝트를 ranking demo로만 읽으면 가장 중요한 출발점을 놓치게 된다. 실제 코드와 stage catalog는 추천 알고리즘보다 먼저 "무엇을 추천할 수 있는가"의 계약을 세운다. 이 선택이 왜 중요했는지는 `shared/src/catalog.ts`와 `recommendation-service.ts`를 나란히 보면 분명해진다. baseline scoring이 사용하는 almost every field가 catalog metadata에서 출발하기 때문이다.

## 처음 세운 것은 점수 함수가 아니라 나중의 모든 판단이 기대는 metadata였다

`shared/src/catalog.ts`의 entry는 단순한 name/description 목록이 아니다. `runtime`, `compatibility`, `operational`, `freshnessScore`, `exposure.userFacingSummaryKo`까지 함께 갖고 있다.

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

이 구조가 중요한 이유는 나중 단계의 거의 모든 판단이 여기를 다시 읽기 때문이다.

- baseline recommendation은 capability/locale/compatibility를 읽는다.
- compatibility gate는 runtime/semver/testedClientVersions를 읽는다.
- release gate는 release candidate와 docs/artifact completeness를 읽지만, 그 전제에는 already validated manifest/candidate 관계가 있다.
- operator surface는 결국 같은 release candidate와 compare/gate 결과를 job으로 재실행한다.

즉 catalog contract는 추천 결과의 재료가 아니라, 전체 proof chain의 공용 언어다.

## baseline은 점수만 만드는 게 아니라 설명 가능한 trace를 남긴다

`recommendation-service.ts`는 query를 tokenization한 뒤 `intent`, `capability`, `category`, `locale`, `compatibility`, `maturity`, `freshness`로 점수를 나눈다.

```ts
const breakdown = {
  intent: calculateIntentScore(queryTokens, entry),
  capability: calculateCapabilityScore(request, entry),
  category: calculateCategoryScore(request, entry),
  locale: calculateLocaleScore(request, entry),
  compatibility: calculateCompatibilityScore(request, entry),
```

좋았던 점은 total score만 반환하지 않는다는 것이다. 같은 함수가 `reasons`와 `buildExplanationKo()`를 통해 한국어 explanation을 만든다. 그래서 추천 품질과 설명 가능성이 갈라지지 않는다. `eval`이 `explanationCompleteness`를 별도 지표로 보는데도, 그 기반 데이터는 이미 baseline trace에 들어 있다.

이 구조 덕분에 2026-03-14 재실행한 `pnpm eval`도 단순 accuracy report가 아니었다. 출력은 `top3Recall 0.9583333333333334`, `explanationCompleteness 1`, `forbiddenHitRate 0`였다. 즉 지금 시스템은 추천 적중률과 설명 completeness를 같이 pass하는 상태다.

## rerank는 새 모델보다 usage signal을 deterministic하게 붙이는 쪽에 가깝다

`rerank-service.ts`는 baseline top-k를 완전히 버리지 않는다. baseline 결과를 가져온 다음 CTR, accept rate, feedback average, explanation quality, freshness를 더한 uplift로 score를 다시 만든다.

```ts
const uplift =
  ctr * 14 + acceptRate * 18 + feedbackAverage * 5 + explanationQuality * 4 + freshness * 2;
```

여기서 중요한 건 "candidate model"이 black-box가 아니라 여전히 explainable weighted rerank라는 점이다. baseline이 어떤 metadata에서 출발했는지, usage signal이 얼마나 score를 밀어 올렸는지, explanationKo가 왜 더 강화되었는지 모두 trace 문장으로 남는다.

즉 이 프로젝트의 첫 ranking loop는 모델 sophistication보다 auditability를 우선한다. 나중에 release gate가 compare uplift를 읽을 수 있는 것도, rerank가 opaque하지 않기 때문이다.

## 이번 단계의 검증 신호

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish
pnpm migrate
pnpm seed
pnpm test
pnpm eval
```

재실행 결과는 다음과 같았다.

- `pnpm migrate`: `No changes detected`
- `pnpm seed`: catalog 12개, eval case 12개, usage signal, feedback, experiments, release candidates 적재
- `pnpm test`: node 9 passed, react 1 passed
- `pnpm eval`: `top3Recall 0.9583333333333334`, `explanationCompleteness 1`, `forbiddenHitRate 0`

이 단계의 결론은 단순하다. 이 프로젝트의 첫 승부는 추천 순위를 멋지게 바꾸는 데 있지 않았다. release proof까지 버틸 metadata contract와 explanation trace를 먼저 세운 데 있었다.
