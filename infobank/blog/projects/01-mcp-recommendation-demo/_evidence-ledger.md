# 01 MCP 추천 최적화 Evidence Ledger

이 문서는 현재 blog를 어떤 근거로 다시 세웠는지 남긴다. 기존 blog 문장을 다듬은 것이 아니라, 현재 소스와 2026-03-14 재실행 결과를 바탕으로 chronology를 다시 복원했다.

## 독립 프로젝트 판정

- front door가 분명하다: `projects/01-mcp-recommendation-demo/README.md`
- 공식 답이 분명하다: `capstone/v2-submission-polish`
- 확장 답이 분명하다: `capstone/v3-oss-hardening`
- 단계 지도와 검증 표가 따로 있다: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- blog 대상은 "추천 시스템 하나"가 아니라 "추천 proof pipeline 하나"로 읽는 편이 맞다.

## 이번에 읽은 핵심 자료

- 문제/범위: `problem/README.md`, `capstone/v2-submission-polish/README.md`
- 구조 지도: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 추천 계약: `capstone/v2-submission-polish/shared/src/catalog.ts`
- baseline/rerank/compare: `recommendation-service.ts`, `rerank-service.ts`, `compare-service.ts`
- release proof: `release-gate-service.ts`, `export-artifact.ts`
- 운영 확장: `capstone/v3-oss-hardening/node/src/services/job-service.ts`, `react/components/mcp-dashboard.tsx`

## Chronology Ledger

### 1. metadata contract를 먼저 세운다

- 기준 파일: `shared/src/catalog.ts`
- 핵심 신호: `runtime`, `compatibility`, `operational`, `freshnessScore`, `exposure.userFacingSummaryKo`
- 해석: recommendation만이 아니라 compatibility/release/operator surface까지 같은 metadata를 다시 읽는 구조를 먼저 만들었다.

### 2. baseline과 rerank를 explanation trace 위에 올린다

- 기준 파일: `recommendation-service.ts`, `rerank-service.ts`
- 핵심 신호: `breakdown.intent/capability/category/locale/compatibility/maturity/freshness`, `uplift = ctr * 14 + ...`
- 해석: opaque model보다 explainable weighted scoring을 택했고, 한국어 explanation과 usage signal uplift가 같은 흐름에 있다.

### 3. compare와 release gate로 submission proof를 닫는다

- 기준 파일: `compare-service.ts`, `release-gate-service.ts`, `export-artifact.ts`
- 핵심 신호:
  - compare uplift는 `Math.max(rankingUplift, scoreUplift)`
  - release gate 조건은 strict ranking improvement가 아니라 `candidateNdcg3 >= baselineNdcg3`와 `uplift >= 0.02`의 조합이다
  - release gate는 eval acceptance + compare uplift + required docs/artifacts + release note completeness를 모두 본다
  - artifact export는 latest eval/compare/compatibility/gate를 한 Markdown으로 묶는다
- 해석: 이 단계부터 프로젝트는 ranking demo보다 deterministic submission path에 가깝고, 현재 rerun도 "같은 nDCG라도 gate를 통과시키는 proof semantics"를 그대로 보여 준다.

### 4. 같은 proof를 job surface로 옮긴다

- 기준 파일: `v3 job-service.ts`, `v3 mcp-dashboard.tsx`
- 핵심 신호: `jobQueues = ["eval", "compare", "compatibility", "release-gate", "artifact-export"]`, `canOperate`, `isOwner`
- 해석: 새 알고리즘이 아니라 orchestration/RBAC/operator UX가 확장 포인트다.

## 이번 재실행 CLI 기록

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish
pnpm db:up
pnpm migrate
pnpm seed
pnpm test
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
cd ../v3-oss-hardening
pnpm test
```

## 이번 재실행 결과 요약

- `pnpm migrate`: `No changes detected`
- `pnpm seed`: 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, release candidates
- `pnpm test` v2: node 9 passed, react 1 passed
- `pnpm eval`: `top3Recall 0.9583333333333334`, `explanationCompleteness 1`, `forbiddenHitRate 0`
- `pnpm compatibility`: 5개 check 모두 pass
- `pnpm release:gate`: `passed true`, `reasons []`, `baselineNdcg3 == candidateNdcg3`, `uplift 0.11464081369730995`
- `pnpm artifact:export`: release-check-bot `v1.5.0` markdown 출력
- `pnpm test` v3: node 8 passed | 2 skipped, react 2 passed
