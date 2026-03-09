# 01 — 접근 기록: 대시보드 설계에서 통합 콘솔까지

## v1 — 단일 컴포넌트 대시보드

### 왜 하나의 컴포넌트인가

처음에는 "대시보드 페이지, 실험 페이지, 카탈로그 페이지"를 분리하려 했다.  
하지만 MCP 추천 시스템의 운영 흐름은 선형적이다:

1. Catalog에서 MCP를 확인하고
2. Recommendation을 baseline/candidate로 실행하고
3. Compare로 결과를 비교하고
4. Feedback을 남기고
5. Experiment를 생성·토글한다

이 흐름이 한 화면에 있어야 운영자가 "왔다 갔다" 하지 않는다.  
결국 `MpcDashboard`라는 단일 컴포넌트로 모든 섹션을 담았다.

### 상태 관리: useState 14개

v1 기준으로 `MpcDashboard` 컴포넌트의 상태 변수만 14개다:

```
catalog, experiments, baselineRecommendation, candidateRecommendation,
latestEval, latestCompare, usageSummary, query, desiredCapabilities,
selectedCatalogId, catalogSummaryDraft, catalogFreshnessDraft,
experimentName, experimentHypothesis, feedbackCatalogId, feedbackNote,
feedbackDelta, loading, error
```

Redux나 Zustand를 도입할까 고민했지만, 이 앱은 운영 콘솔이지 사용자 앱이 아니다.  
상태 간 의존이 `loadAll()` 호출 한 번으로 해결되기 때문에 `useState`로 충분했다.

### apiFetch 유틸

모든 API 호출이 `apiFetch<T>()` 하나로 통일된다:

```typescript
async function apiFetch<T>(path: string, init?: RequestInit) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    cache: "no-store"
  });
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return (await response.json()) as T;
}
```

`cache: "no-store"`가 핵심이다.  
대시보드에서 "방금 Catalog를 수정했는데 목록이 안 바뀐다" 같은 이슈를 원천 차단한다.

### loadAll() — 병렬 fetch

페이지 마운트 시 `loadAll()`이 `Promise.all`로 5개 API를 동시에 호출한다:

```
/api/catalog, /api/evals/latest, /api/compare/latest, /api/experiments, /api/usage-events
```

CRUD 동작(저장, 삭제, 토글) 후에도 항상 `await loadAll()`을 호출해서 화면을 갱신한다.  
낙관적 업데이트(optimistic update) 대신 "서버 상태가 진실"이라는 원칙을 택한 것이다.

## v2 — Release Console 확장

### 추가된 상태와 API

v2에서는 Release Candidate 관련 상태가 더해진다:

- `releaseCandidates`, `selectedReleaseCandidateId`
- `releaseVersionDraft`, `releaseOwnerDraft`, `releaseNotesDraft`
- `latestCompatibility`, `latestGate`, `latestArtifact`

`loadAll()`도 9개 API를 호출하는 것으로 늘어난다:

```
/api/catalog, /api/evals/latest, /api/compare/latest, /api/experiments,
/api/usage-events, /api/release-candidates, /api/compatibility/latest,
/api/release-gate/latest, /api/submission/latest
```

### Release Candidate 빌더

`buildSampleReleaseCandidate()`는 catalog seed에서 RC를 생성한다.  
주목할 점은 `requiredDocs`와 `requiredArtifacts` 배열이 하드코딩되어 있다는 것이다:

```typescript
requiredDocs: [
  "docs/README.md", "docs/runbook.md", "docs/eval-proof.md",
  "docs/compare-report.md", "docs/compatibility-report.md",
  "docs/release-gate-proof.md", "docs/korean-market-fit.md"
],
requiredArtifacts: [
  ".changeset/config.json",
  ".changeset/study1-v2-demo.md",
  "../../../.github/workflows/study1-v2-dry-run.yml"
]
```

이것은 "릴리즈 게이트에서 어떤 문서와 아티팩트를 검사하는지"를 사람이 읽을 수 있게 명시하는 역할을 한다.  
gate가 FAIL일 때 "무엇이 빠졌는지"를 RC 객체 자체에서 역추적할 수 있다.

### Compatibility & Release Gate 버튼

대시보드에 "Compatibility 실행", "Release Gate 실행" 버튼이 추가되었다.  
각각 POST → `loadAll()` 패턴으로 결과를 갱신하고, 통과 여부를 `PASS/FAIL`로 표시한다.

### Artifact Export Preview

v2의 가장 큰 변화.  
"Submission Artifact Preview" 섹션에서 JSON 증빙 전체를 미리보기할 수 있다.  
이것은 stage 06의 artifact export API를 대시보드에서 소비하는 것이다.

## 섹션 배치 전략

대시보드는 CSS Grid 기반 레이아웃을 쓴다:

```
┌──────────────────────────────────────────┐
│              Hero / 제목                  │
├────────────────────┬─────────────────────┤
│  추천 실험         │  Usage / Compare    │
│  (baseline/cand)   │  Feedback Loop      │
├────────────────────┼─────────────────────┤
│  Experiment Console│  Catalog CRUD       │
├────────────────────┴─────────────────────┤
│  Release Console (v2에서 추가)            │
└──────────────────────────────────────────┘
```

왼쪽 열은 "실행하는 것" (추천, 실험), 오른쪽 열은 "확인하는 것" (지표, 피드백, 카탈로그).  
이 배치는 운영자의 눈이 "실행 → 결과 확인" 순서로 자연스럽게 흐르도록 설계된 것이다.

## e2e 테스트 전략

Playwright로 실제 대시보드의 핵심 흐름을 검증한다:

```typescript
test("runs candidate recommendation and release gate flow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "MCP 제출 운영 콘솔" })).toBeVisible();
  await page.getByRole("button", { name: "Candidate 실행" }).click();
  // candidate 설명 텍스트 노출 확인
  await page.getByRole("button", { name: "Release Gate 실행" }).click();
  await expect(page.getByRole("heading", { name: "Release Quality" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Submission Artifact Preview" })).toBeVisible();
});
```

이 테스트는 "Candidate 실행 → Release Gate 실행 → 결과 확인"이라는 운영자 핵심 동선을 커버한다.  
Happy path 하나지만, 대시보드가 API와 올바르게 연결되어 있는지 증명하기에 충분하다.
