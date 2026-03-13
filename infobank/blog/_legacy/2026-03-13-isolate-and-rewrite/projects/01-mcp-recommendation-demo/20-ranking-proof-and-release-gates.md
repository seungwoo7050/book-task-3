# Ranking Proof And Release Gates

이 글은 시리즈의 가운데 구간이다. `v1`에서 baseline/candidate compare가 생긴 뒤, `v2`가 왜 compatibility gate, release gate, artifact export까지 한 번에 묶어야 했는지를 따라간다. 핵심은 ranking uplift를 문서화하는 수준을 넘어서, release 판단도 같은 데이터에서 나오게 만드는 것이다.

구현 순서 요약:

- compare service가 baseline과 candidate를 같은 eval case 묶음으로 점수화한다.
- compatibility gate가 manifest, semver, tested client set, Korean metadata를 검사한다.
- release gate가 compare uplift와 docs/artifact presence를 함께 보고, 마지막에 artifact export가 그 상태를 그대로 Markdown으로 저장한다.

## Day 2

### Session 2

- 당시 목표: reranker가 만든 candidate를 "감각적 개선"이 아니라 `baseline vs candidate` 비교 보고서로 바꾼다.
- 변경 단위: `node/src/services/compare-service.ts`
- 처음 가설: candidate top-1이 baseline top-1보다 더 그럴듯해 보이면 충분할 줄 알았다.
- 실제 진행: 각 eval case마다 baseline과 candidate의 top ids를 동시에 계산하고, `candidateWins`일 때만 candidate score를 채택하도록 했다. 평균 nDCG@3와 top1 hit rate가 나중 단계의 입력이 된다.

핵심 코드:

```ts
const baseline = recommendCatalog(request, catalog);
const candidate = rerankCatalog(request, catalog, usageEvents, feedbackRecords);
const baselineIds = baseline.topCandidates.map((candidateRow) => candidateRow.catalogId);
const candidateIds = candidate.topCandidates.map((candidateRow) => candidateRow.catalogId);
const baselineScore = ndcgAt3(baselineIds, item.expectedTopIds);
const candidateScore = ndcgAt3(candidateIds, item.expectedTopIds);
const candidateWins = candidateScore >= baselineScore;
```

그리고 summary는 baseline과 candidate를 따로 보관한다.

```ts
metrics: {
  baselineNdcg3,
  candidateNdcg3,
  uplift: candidateNdcg3 - baselineNdcg3,
  baselineTop1HitRate,
  candidateTop1HitRate
}
```

왜 이 코드가 중요했는가:

`candidateWins` 한 줄이 중요했다. 이 프로젝트는 새 ranking이 baseline보다 나쁘면 그대로 baseline 값을 유지한다. compare는 "항상 candidate를 밀어 올리는 함수"가 아니라 "candidate가 이긴 만큼만 채택하는 검증 함수"가 됐다.

CLI:

```bash
$ pnpm test
node test:  Test Files  6 passed (6)
node test:       Tests  9 passed (9)
react test: Test Files  1 passed (1)
react test:      Tests  1 passed (1)
```

검증 신호:

- `compare-service.ts`는 compare snapshot의 숫자를 만들고,
- `routes.integration.test.ts`는 API가 그 보고서를 실제로 내보내는지 확인한다.

새로 배운 것:

compare는 모델 실험을 미화하는 문서가 아니라, baseline을 되돌릴 수 있는 안전장치 역할을 해야 했다.

## Day 3

### Session 1

- 당시 목표: compare가 좋아 보여도 실제 client/runtime과 부딪히면 못 나간다는 문제를 compatibility gate로 앞단에서 막는다.
- 변경 단위: `node/src/services/compatibility-service.ts`, `shared/src/contracts.ts`
- 처음 가설: manifest validation 정도만 통과하면 호환성도 설명 가능할 것 같았다.
- 실제 진행: compatibility gate가 `mcpManifestSchema`를 다시 읽고, semver 범위, tested client version, deprecated field usage, Korean metadata completeness를 모두 검사하게 했다.

핵심 코드:

```ts
const runtimeSupported =
  semver.valid(candidate.targetClientVersion) !== null &&
  semver.satisfies(candidate.targetClientVersion, runtimeRange) &&
  entry.compatibility.testedClientVersions.includes(candidate.targetClientVersion);

const koreanMetadataComplete =
  entry.summaryKo.length >= 10 &&
  entry.descriptionKo.length >= 20 &&
  entry.koreanUseCases.length >= 2 &&
  entry.differentiationPoints.length >= 2 &&
  entry.exposure.userFacingSummaryKo.length >= 10;
```

왜 이 코드가 중요했는가:

ranking project인데도 compatibility gate가 Korean metadata completeness를 본다는 점이 전환점이었다. 이 프로젝트에서 metadata는 README 장식이 아니라 release 조건이다.

CLI:

```bash
$ pnpm compatibility rc-release-check-bot-1-5-0
{
  "releaseCandidateId": "rc-release-check-bot-1-5-0",
  "candidateVersion": "1.5.0",
  "passed": true,
  "checks": [
    { "name": "manifest-schema", "passed": true },
    { "name": "runtime-range", "passed": true },
    { "name": "semver-consistency", "passed": true },
    { "name": "deprecated-fields", "passed": true },
    { "name": "korean-metadata", "passed": true }
  ]
}
```

검증 신호:

- 실제 출력이 check 목록을 JSON으로 남기기 때문에, compatibility pass/fail이 더 이상 슬라이드 메모가 아니다.

새로 배운 것:

semver와 metadata completeness를 같은 gate에서 보는 순간, 추천 품질과 release readiness는 분리된 트랙이 아니게 됐다.

### Session 2

- 당시 목표: compatibility, eval, compare, docs/artifact 존재 여부를 모두 합쳐 실제 release decision을 자동화한다.
- 변경 단위: `node/src/services/release-gate-service.ts`, `node/src/services/artifact-service.ts`, `docs/runbook.md`, `docs/release-gate-proof.md`
- 처음 가설: release note는 사람이 쓰고, 코드 쪽은 bool 하나만 내도 될 것 같았다.
- 실제 진행: release gate가 eval acceptance, compare uplift, required docs/artifacts, release note section completeness를 한 번에 검사하고, artifact export가 그 상태를 Markdown으로 굳힌다.

핵심 코드:

```ts
if (!(candidateNdcg3 >= baselineNdcg3 && uplift >= 0.02)) {
  reasons.push("candidate compare uplift가 임계값 0.02를 넘지 못했거나 baseline보다 낮습니다.");
}

if (!requiredPathsExist(candidate.requiredDocs) || !requiredPathsExist(candidate.requiredArtifacts)) {
  reasons.push("제출용 docs 또는 artifact 파일이 누락되었습니다.");
}

if (!releaseNotesComplete(candidate.releaseNotesKo)) {
  reasons.push("release note에 '변경 요약', '검증', '리스크' 섹션이 모두 들어 있지 않습니다.");
}
```

그리고 artifact export는 같은 수치를 다시 문서로 만든다.

```ts
"## Offline Eval",
`- top3 recall: ${(latestEval?.metrics.top3Recall ?? 0).toFixed(3)}`,
`- explanation completeness: ${(latestEval?.metrics.explanationCompleteness ?? 0).toFixed(3)}`,
`- forbidden hit rate: ${(latestEval?.metrics.forbiddenHitRate ?? 0).toFixed(3)}`,
"## Compare Snapshot",
`- baseline nDCG@3: ${(latestCompare?.metrics.baselineNdcg3 ?? 0).toFixed(3)}`,
`- candidate nDCG@3: ${(latestCompare?.metrics.candidateNdcg3 ?? 0).toFixed(3)}`,
`- uplift: ${(latestCompare?.metrics.uplift ?? 0).toFixed(3)}`,
```

왜 이 코드가 중요했는가:

release gate는 점수만 보지 않는다. docs path와 release note section까지 코드가 본다. 그래서 artifact export가 "결과를 정리한 글"이 아니라, 이미 통과한 상태를 그대로 덤프한 문서가 된다.

CLI:

```bash
$ pnpm release:gate rc-release-check-bot-1-5-0
{
  "releaseCandidateId": "rc-release-check-bot-1-5-0",
  "passed": true,
  "metrics": {
    "top3Recall": 0.9583333333333334,
    "explanationCompleteness": 1,
    "forbiddenHitRate": 0,
    "baselineNdcg3": 0.9758684958518087,
    "candidateNdcg3": 0.9758684958518087,
    "uplift": 0.11464081369730995
  }
}
```

```bash
$ pnpm artifact:export rc-release-check-bot-1-5-0
# release-check-bot v1.5.0
- compatibility passed: true
- release gate passed: true
- top3 recall: 0.958
- uplift: 0.115
```

새로 배운 것:

proof 문서는 사람이 따로 요약해서 쓰는 보조 산출물이 아니라, gate가 이미 본 데이터를 다시 출력하는 마지막 단계여야 했다.

다음:

이제 공식 제출 답은 닫혔다. 다음 글에서는 이 동기식 proof 흐름을 로그인된 운영자가 job queue로 굴리는 `v3` self-hosted surface로 옮긴다.
