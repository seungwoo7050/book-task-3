# MCP 추천 최적화 시리즈 맵

이 프로젝트를 한 줄로 줄이면 "MCP 추천 시스템"처럼 보이지만, 실제 소스와 검증을 따라가면 더 정확한 설명은 이렇다. 추천 대상의 metadata 계약을 먼저 단단하게 만들고, 그 계약에서 나온 explanation trace와 usage signal을 compare/gate로 묶고, 마지막에는 그 proof를 사람 손 CLI에서 operator job surface로 옮긴 프로젝트다. 따라서 이 시리즈는 ranking 모델을 중심에 두지 않는다. 오히려 ranking이 왜 metadata, release candidate, artifact export, 운영자 UI까지 같은 언어를 쓰게 되었는지를 추적한다.

## 이 프로젝트를 읽는 질문

- 왜 추천 알고리즘보다 catalog/manifest 계약이 먼저였는가
- rerank와 compare는 어떤 기준으로 "개선 증빙"이 되었는가
- release gate는 어떤 수치와 문서 조건을 같이 보고 있는가
- `v3` 확장은 새 알고리즘이 아니라 어떤 운영 표면을 추가한 것인가

## 이번에 사용한 근거

- 문제 정의: `projects/01-mcp-recommendation-demo/problem/README.md`
- 단계 지도: `docs/stage-catalog.md`, `docs/verification-matrix.md`
- 공식 답: `capstone/v2-submission-polish/README.md`
- 핵심 코드:
  - `capstone/v2-submission-polish/shared/src/catalog.ts`
  - `capstone/v2-submission-polish/node/src/services/recommendation-service.ts`
  - `capstone/v2-submission-polish/node/src/services/rerank-service.ts`
  - `capstone/v2-submission-polish/node/src/services/compare-service.ts`
  - `capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
  - `capstone/v2-submission-polish/node/src/scripts/export-artifact.ts`
  - `capstone/v3-oss-hardening/node/src/services/job-service.ts`
  - `capstone/v3-oss-hardening/react/components/mcp-dashboard.tsx`
- 실제 검증:
  - `pnpm db:up`
  - `pnpm migrate`
  - `pnpm seed`
  - `pnpm test`
  - `pnpm eval`
  - `pnpm compatibility rc-release-check-bot-1-5-0`
  - `pnpm release:gate rc-release-check-bot-1-5-0`
  - `pnpm artifact:export rc-release-check-bot-1-5-0`
  - `cd ../v3-oss-hardening && pnpm test`

## 이번 재실행에서 먼저 보인 사실

2026-03-14 재실행 기준으로 `v2`의 DB 준비와 seed는 정상적으로 끝났다. `eval`은 `top3Recall 0.9583333333333334`, `explanationCompleteness 1`, `forbiddenHitRate 0`를 기록했다. `compatibility`는 manifest/runtime/semver/deprecated field/한국어 metadata 5개 check를 모두 통과했다. `release:gate`는 `baselineNdcg3`와 `candidateNdcg3`가 둘 다 `0.9758684958518087`인데도 `uplift 0.11464081369730995`로 pass 했다. 이 수치는 `compare-service.ts`가 `uplift`를 ranking uplift만이 아니라 average score uplift까지 포함해 계산한다는 사실과 맞물린다. 즉 이 프로젝트의 proof는 "순위가 무조건 더 올라갔다"보다 "후보 점수 체계가 개선 threshold를 넘겼다"는 설계에 가깝다.

## 챕터 구성

1. [10-catalog-contracts-and-first-ranking-loop.md](./10-catalog-contracts-and-first-ranking-loop.md)
   - 추천 결과보다 먼저 어떤 metadata 계약을 고정했는지, baseline과 rerank가 같은 trace를 어떻게 공유하는지 본다.
2. [20-ranking-proof-and-release-gates.md](./20-ranking-proof-and-release-gates.md)
   - eval, compare, compatibility, release gate, artifact export가 어떻게 release proof 체인으로 묶이는지 본다.
3. [30-self-hosted-operator-surface.md](./30-self-hosted-operator-surface.md)
   - `v2` proof pipeline이 `v3`에서 RBAC와 async job이 있는 운영 표면으로 어떻게 이동하는지 본다.
