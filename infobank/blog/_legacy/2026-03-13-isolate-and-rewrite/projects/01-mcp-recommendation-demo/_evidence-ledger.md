# 01 MCP 추천 최적화 evidence ledger

## 독립 프로젝트 판정 근거

- 자기 문제 범위: MCP catalog, recommendation, compare, release gate, self-hosted operator surface를 한 제품 질문으로 설명할 수 있다.
- 자기 검증 명령: `pnpm db:up`, `pnpm migrate`, `pnpm seed`, `pnpm test`, `pnpm eval`, `pnpm compatibility`, `pnpm release:gate`, `pnpm artifact:export`, `pnpm test:integration`.
- 자기 구현 흐름: `v0 -> v1 -> v2 -> v3` 버전 디렉터리와 `docs/stage-catalog.md`가 독립 chronology를 제공한다.

## Day 1 / Session 1

- 시간 표지: Day 1 / Session 1
- 당시 목표: catalog와 manifest를 "추천에 쓰일 메타데이터"가 아니라 "검증 가능한 계약"으로 먼저 고정한다.
- 변경 단위: `capstone/v0-initial-demo/shared/src/contracts.ts`, `capstone/v0-initial-demo/node/src/services/recommendation-service.ts`, `capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`
- 처음 가설: baseline selector는 간단한 keyword match만 있으면 바로 시작할 수 있을 것이라고 봤다.
- 실제 조치: `mcpManifestSchema`, `catalogEntrySchema`, `recommendationRequestSchema`, `recommendationTraceSchema`를 먼저 세우고 그 위에서만 점수 계산이 돌도록 만들었다.
- CLI:

```bash
$ pnpm db:up
Container study1-v2-postgres Started

$ pnpm migrate
[i] No changes detected

$ pnpm seed
Seeded 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, and release candidates.
```

- 검증 신호: seed 단계에서 catalog entry, eval case, usage signal, release candidate가 한 번에 채워졌고, 이후 `manifest-validation.test.ts`가 이 구조를 깨지 않게 지켜 준다.
- 핵심 코드 앵커: `shared/src/contracts.ts`의 `mcpManifestSchema`, `node/src/services/recommendation-service.ts`의 `scoreCatalogEntry`
- 새로 배운 것: 추천 시스템의 시작점은 "점수 함수"가 아니라 "무엇을 manifest에 적게 할 것인가"라는 계약 설계였다.
- 다음: 계약이 고정됐으면 각 후보를 왜 추천했는지 한국어 설명까지 같은 trace 안에 넣어야 한다.

## Day 1 / Session 2

- 시간 표지: Day 1 / Session 2
- 당시 목표: baseline recommendation을 offline eval과 한국어 explanation까지 연결해서 "데모가 돈다"가 아니라 "설명 가능한 추천이 나온다"를 증명한다.
- 변경 단위: `capstone/v0-initial-demo/node/src/services/recommendation-service.ts`, `capstone/v0-initial-demo/shared/src/eval.ts`, `capstone/v0-initial-demo/react/components/mcp-dashboard.tsx`
- 처음 가설: top-N 결과만 맞으면 demo 관점에서는 충분할 것이라고 봤다.
- 실제 조치: 점수 breakdown과 `reasons` 배열을 trace에 남기고, `buildExplanationKo`로 UI와 eval이 같은 설명 문자열을 읽게 했다.
- CLI:

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

- 검증 신호: acceptance가 `top3RecallPass`, `explanationPass`, `forbiddenPass` 세 항목으로 분리돼서, ranking과 explanation을 따로 놓칠 수 없게 됐다.
- 핵심 코드 앵커: `node/src/services/recommendation-service.ts`의 `buildExplanationKo`, `shared/src/eval.ts`
- 새로 배운 것: recommendation output은 "정답 id 목록"만으로는 부족했고, 한국어 추천 이유도 acceptance criterion으로 승격돼야 했다.
- 다음: baseline이 설명 가능해졌으니, 이제 실사용 신호를 점수에 끼워 넣어 baseline/candidate compare를 만들 차례다.

## Day 2 / Session 1

- 시간 표지: Day 2 / Session 1
- 당시 목표: baseline selector 위에 reranker, usage log, feedback loop, compare snapshot을 올려 candidate가 baseline보다 실제로 좋아졌는지 보여 준다.
- 변경 단위: `capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`, `capstone/v1-ranking-hardening/node/src/services/compare-service.ts`, `capstone/v1-ranking-hardening/node/src/db/schema.ts`, `capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- 처음 가설: baseline 점수만 잘 다듬으면 추천 품질 개선도 설명될 것이라고 봤다.
- 실제 조치: impression/click/accept/dismiss와 feedback delta를 모아 uplift를 만들고, `runCompare()`에서 nDCG@3와 top1 hit를 baseline과 candidate로 병렬 계산하게 했다.
- CLI:

```bash
$ pnpm test
node test:  Test Files  6 passed (6)
node test:       Tests  9 passed (9)
react test: Test Files  1 passed (1)
react test:      Tests  1 passed (1)
```

- 검증 신호: `rerank-service.test.ts`, `routes.integration.test.ts`, `mcp-dashboard.test.tsx`가 동시에 살아 있어서 ranking logic과 operator surface를 따로 떼지 않는다.
- 핵심 코드 앵커: `node/src/services/rerank-service.ts`의 `aggregateSignals()`와 `rerankCatalog()`, `node/src/services/compare-service.ts`의 `runCompare()`
- 새로 배운 것: 운영 로그는 단순 analytics가 아니라 candidate promotion을 위한 scoring signal이 될 수 있었다.
- 다음: candidate가 baseline보다 좋아 보인다는 감각만으로는 release를 열 수 없으니, compatibility와 release gate를 도입해야 한다.

## Day 3 / Session 1

- 시간 표지: Day 3 / Session 1
- 당시 목표: compare 결과를 제출 가능한 release 판단으로 바꾸고, docs/artifact까지 같은 흐름에 묶는다.
- 변경 단위: `capstone/v2-submission-polish/node/src/services/compatibility-service.ts`, `capstone/v2-submission-polish/node/src/services/release-gate-service.ts`, `capstone/v2-submission-polish/node/src/services/artifact-service.ts`, `capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`, `capstone/v2-submission-polish/node/tests/release-gate-service.test.ts`
- 처음 가설: offline eval과 compare 점수만 있으면 release 설명은 문서로 수동 정리해도 될 것이라고 봤다.
- 실제 조치: compatibility gate가 manifest, semver, tested client set, Korean metadata를 검사하게 하고, release gate가 compare uplift, docs/artifact presence, release note 섹션까지 함께 보게 만들었다. 마지막에는 같은 데이터를 Markdown artifact로 export했다.
- CLI:

```bash
$ pnpm compatibility rc-release-check-bot-1-5-0
{
  "releaseCandidateId": "rc-release-check-bot-1-5-0",
  "passed": true
}

$ pnpm release:gate rc-release-check-bot-1-5-0
{
  "releaseCandidateId": "rc-release-check-bot-1-5-0",
  "passed": true,
  "metrics": {
    "top3Recall": 0.9583333333333334,
    "uplift": 0.11464081369730995
  }
}

$ pnpm artifact:export rc-release-check-bot-1-5-0
# release-check-bot v1.5.0
- compatibility passed: true
- release gate passed: true
```

- 검증 신호: release gate가 `docs/runbook.md`, `docs/release-gate-proof.md`, compare/eval outputs를 같은 판단 경로 안으로 끌어오고, artifact export가 그 상태를 바로 문서로 굳힌다.
- 핵심 코드 앵커: `node/src/services/compatibility-service.ts`의 `runCompatibilityGate()`, `node/src/services/release-gate-service.ts`의 `runReleaseGate()`, `node/src/services/artifact-service.ts`의 `buildSubmissionArtifact()`
- 새로 배운 것: release proof는 ranking 코드를 잘 짰다는 말이 아니라, metadata, docs, compare, eval, artifact가 같은 candidate id를 가리키는지 확인하는 일이다.
- 다음: 공식 제출 답이 끝났다면, 이제 이 흐름을 로그인된 운영자가 직접 설치해 쓰는 self-hosted surface로 옮겨야 한다.

## Day 4 / Session 1

- 시간 표지: Day 4 / Session 1
- 당시 목표: `v2`의 sync demo를 `v3` self-hosted operator product로 확장한다.
- 변경 단위: `capstone/v3-oss-hardening/node/src/services/auth-service.ts`, `capstone/v3-oss-hardening/node/src/app.ts`, `capstone/v3-oss-hardening/node/src/services/job-service.ts`, `capstone/v3-oss-hardening/node/src/worker.ts`, `capstone/v3-oss-hardening/docker-compose.yml`, `capstone/v3-oss-hardening/react/components/mcp-dashboard.tsx`
- 처음 가설: eval/compare/release gate도 요청 한 번에 동기적으로 돌려도 operator console에서는 충분할 것이라고 봤다.
- 실제 조치: cookie session과 RBAC를 먼저 넣고, eval/compare/compatibility/release-gate/artifact-export를 모두 queue job으로 바꿨다. API는 job id와 status를 돌려주고 worker가 상태를 업데이트하도록 경계를 바꿨다.
- CLI:

```bash
$ pnpm migrate
[✓] Changes applied

$ pnpm bootstrap:owner
{
  "ownerEmail": "owner@study1.local",
  "role": "owner"
}

$ pnpm test
node test:  Test Files  5 passed | 1 skipped (6)
node test:       Tests  8 passed | 2 skipped (10)
react test: Test Files  1 passed (1)
react test:      Tests  2 passed (2)
```

- 검증 신호: default suite가 DB route integration을 opt-in으로 남겨 두면서도, auth/session, queued export, release-gate job flow는 component test와 unit test로 유지한다.
- 핵심 코드 앵커: `node/src/app.ts`의 `resolveAuth()`, `node/src/services/job-service.ts`의 `performJob()` / `enqueueJob()` / `startJobWorker()`
- 새로 배운 것: productization은 기능을 더 붙이는 일이 아니라, "누가 어떤 권한으로 어떤 job을 언제 재실행할 수 있는가"를 API 경계 자체에 새기는 일이다.
- 다음: 최종 blog는 이 버전 사다리를 `10 / 20 / 30` 세 글로 나눠 읽게 만든다.
