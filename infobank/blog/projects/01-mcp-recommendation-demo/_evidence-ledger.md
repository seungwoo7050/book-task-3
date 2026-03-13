# 01 MCP 추천 최적화 Evidence Ledger

이 문서는 이 시리즈를 어떤 근거로 복원했는지 보여 주는 기록이다. 예전 blog를 다시 다듬은 것이 아니라, 현재 소스와 CLI 결과를 바탕으로 "이 프로젝트가 어떤 순서로 자랐는가"를 다시 세웠다.

## 독립 프로젝트 판정

- 문제 범위: `catalog -> recommendation -> compare -> compatibility/release gate -> operator surface`
- 진입점: `projects/01-mcp-recommendation-demo/README.md`
- 검증 표면: `pnpm db:up`, `pnpm migrate`, `pnpm seed`, `pnpm test`, `pnpm eval`, `pnpm compatibility`, `pnpm release:gate`, `pnpm artifact:export`
- 복원 근거: `docs/stage-catalog.md`와 `docs/verification-matrix.md`가 버전 흐름과 검증 순서를 따로 보여 준다.

## 어떤 자료를 읽었는가

- stage map: `docs/stage-catalog.md`
- verification map: `docs/verification-matrix.md`
- front door 문서: `capstone/v2-submission-polish/README.md`, `capstone/v3-oss-hardening/README.md`
- 핵심 코드: `shared/src/catalog.ts`, `shared/src/eval.ts`, `node/src/services/recommendation-service.ts`, `node/src/services/rerank-service.ts`, `node/src/services/release-gate-service.ts`, `node/src/scripts/export-artifact.ts`, `v3 node/src/services/job-service.ts`, `v3 react/components/mcp-dashboard.tsx`
- git anchor: `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## Chronology Ledger

### 1. Phase 1 - catalog와 manifest 계약을 먼저 세운다

한 줄 요약: 이 프로젝트의 출발점은 추천 알고리즘이 아니라, 추천 대상이 어떤 정보를 가져야 하는지 정하는 일이다.

- 당시 목표: 추천 품질을 올리기 전에 `무엇을 추천할 수 있는가`를 안정적인 데이터 계약으로 고정한다.
- 변경 단위: `shared/src/catalog.ts`, `shared/src/contracts.ts`, `docs/stage-catalog.md`
- 처음 가설: ranking logic부터 손대면 한국어 설명, 호환성 정보, release metadata가 뒤늦게 덧붙어 흔들릴 가능성이 크다.
- 실제 조치: seeded catalog entry에 `compatibility`, `operational`, `exposure`, `summaryKo` 같은 운영 메타데이터를 함께 넣었다.
- CLI: `pnpm seed`
- 검증 신호: `Seeded 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, and release candidates.`

이 단계에서 중요한 코드는 아래 조각이다. 이 블록은 단순한 데이터 예시가 아니라, 나중에 recommendation, compatibility gate, release gate가 함께 읽을 공통 계약 역할을 한다.

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

- 새로 배운 것: 이 프로젝트의 첫 구현은 추천 모델이 아니라, release 판단까지 버틸 수 있는 metadata 계약이었다.
- 다음: baseline scoring과 한국어 explanation을 같은 trace 안으로 묶는다.

### 2. Phase 2 - baseline scoring과 candidate rerank를 하나의 흐름으로 묶는다

한 줄 요약: 추천 결과를 설명 가능하게 만들고, 그 위에 실사용 신호 기반 rerank를 덧붙인다.

- 당시 목표: capability, locale, compatibility를 기준으로 설명 가능한 baseline을 만들고, 그 위에 usage signal rerank를 얹는다.
- 변경 단위: `node/src/services/recommendation-service.ts`, `node/src/services/rerank-service.ts`, `shared/src/eval.ts`
- 처음 가설: 한국어 explanation과 offline eval은 따로 자라면 흔들리기 쉬우니, 같은 metadata를 함께 읽어야 안정적이다.
- 실제 조치: baseline은 score breakdown과 `explanationKo`를 만들고, candidate는 CTR, accept, feedback, freshness를 반영해 top-k를 다시 정렬했다.
- CLI: `pnpm test`, `pnpm eval`
- 검증 신호:
  - node tests `9 passed`
  - react tests `1 passed`
  - `top3Recall 0.9583333333333334`
  - `explanationCompleteness 1`
  - `forbiddenHitRate 0`

이 단계의 전환점은 아래 두 코드 조각이다. 첫 번째는 baseline이 어떤 근거로 점수를 계산하는지 보여 주고, 두 번째는 candidate가 왜 순서를 바꾸는지 설명해 준다.

```ts
const breakdown = {
  intent: calculateIntentScore(queryTokens, entry),
  capability: calculateCapabilityScore(request, entry),
  category: calculateCategoryScore(request, entry),
  locale: calculateLocaleScore(request, entry),
  compatibility: calculateCompatibilityScore(request, entry),
```

```ts
const uplift =
  ctr * 14 + acceptRate * 18 + feedbackAverage * 5 + explanationQuality * 4 + freshness * 2;
```

- 새로 배운 것: recommendation trace와 evaluation fixture가 같은 필드를 읽어야 compare와 gate까지 같은 언어로 이어진다.
- 다음: compare, compatibility, release gate를 실제 제출 proof로 닫는다.

### 3. Phase 3 - 점수 개선을 release 판단까지 연결한다

한 줄 요약: 이 단계에서 추천 시스템은 단순 데모를 넘어, 제출 가능한 릴리즈 후보를 판정하는 도구가 된다.

- 당시 목표: `좋아 보이는 추천`이 아니라 `릴리즈 가능한 추천 candidate`를 판정하는 체계를 만든다.
- 변경 단위: `docs/compare-report.md`, `node/src/services/release-gate-service.ts`, `node/src/scripts/export-artifact.ts`, `docs/release-gate-proof.md`
- 처음 가설: compare uplift만으로는 제출 마감 판단이 약하므로, required docs/artifacts와 release note completeness까지 함께 검사해야 한다.
- 실제 조치: release gate가 eval acceptance, compare uplift, compatibility pass, 파일 존재 여부, release note 섹션까지 한 번에 검사하게 만들었다.
- CLI: `pnpm compatibility rc-release-check-bot-1-5-0`, `pnpm release:gate rc-release-check-bot-1-5-0`, `pnpm artifact:export rc-release-check-bot-1-5-0`
- 검증 신호:
  - compatibility `passed: true`
  - release gate `passed: true`
  - `uplift: 0.11464081369730995`
  - artifact markdown export 생성

이 코드가 중요한 이유는, 점수 비교만으로 끝내지 않고 실제 제출에 필요한 문서와 산출물까지 함께 확인하기 때문이다.

```ts
if (!(candidateNdcg3 >= baselineNdcg3 && uplift >= 0.02)) {
  reasons.push("candidate compare uplift가 임계값 0.02를 넘지 못했거나 baseline보다 낮습니다.");
}

if (!requiredPathsExist(candidate.requiredDocs) || !requiredPathsExist(candidate.requiredArtifacts)) {
  reasons.push("제출용 docs 또는 artifact 파일이 누락되었습니다.");
}
```

- 새로 배운 것: 운영 승인처럼 읽히는 proof는 모델 점수와 문서 completeness를 같이 볼 때 만들어진다.
- 다음: 이 gate들을 로그인과 job UI 안으로 다시 감싼다.

### 4. Phase 4 - self-hosted 운영 표면으로 확장한다

한 줄 요약: 이미 만든 proof pipeline을 버리지 않고, 역할과 작업 큐를 가진 운영 화면으로 다시 배치한다.

- 당시 목표: `v2`의 동기식 gate 흐름을 `v3`에서 owner/operator/viewer가 다루는 self-hosted surface로 바꾼다.
- 변경 단위: `capstone/v3-oss-hardening/node/src/services/job-service.ts`, `capstone/v3-oss-hardening/react/components/mcp-dashboard.tsx`
- 처음 가설: productization의 핵심은 새 ranking 로직이 아니라 async job, audit log, role-aware UI다.
- 실제 조치: `eval`, `compare`, `compatibility`, `release-gate`, `artifact-export`를 queue로 나누고, 대시보드에서 polling으로 작업 완료를 기다리게 했다.
- CLI: `cd capstone/v3-oss-hardening && pnpm test`
- 검증 신호:
  - node `8 passed | 2 skipped`
  - react `2 passed`

이 코드 조각은 `v2`에서 사람이 순서대로 실행하던 proof가, `v3`에서 운영 작업 목록으로 바뀌는 순간을 보여 준다.

```ts
const jobQueues = [
  "eval",
  "compare",
  "compatibility",
  "release-gate",
  "artifact-export"
] satisfies JobName[];
```

```ts
const canOperate = session?.user.role === "owner" || session?.user.role === "operator";

async function waitForJob(jobId: string) {
  for (let attempt = 0; attempt < 20; attempt += 1) {
    const response = await apiFetch<{ item: JobRun }>(`/api/jobs/${jobId}`);
```

- 새로 배운 것: self-hosted 확장은 기존 proof를 지우는 단계가 아니라, 같은 proof를 운영자가 기다리고 확인할 수 있는 표면으로 옮기는 단계였다.

## 최신 CLI 발췌

```bash
pnpm seed
pnpm test
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
cd ../v3-oss-hardening && pnpm test
```

```text
Seeded 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, and release candidates.
Tests 9 passed (node) + 1 passed (react)
top3Recall 0.9583333333333334 / explanationCompleteness 1 / forbiddenHitRate 0
compatibility passed: true
release gate passed: true
uplift: 0.11464081369730995
v3 tests: 8 passed | 2 skipped (node), 2 passed (react)
```
