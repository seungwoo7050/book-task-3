# 01-ops-triage-console 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다, 단일 운영자 시나리오를 기준으로 한다, 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `sections`와 `metadata`, `arraysEqual` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다.
- 단일 운영자 시나리오를 기준으로 한다.
- 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다.
- 첫 진입점은 `../study/frontend-portfolio/01-ops-triage-console/next/app/case-study/page.tsx`이고, 여기서 `sections`와 `metadata` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/frontend-portfolio/01-ops-triage-console/next/app/case-study/page.tsx`: 화면 진입점에서 최상위 composition과 초기 시연 흐름을 고정하는 파일이다.
- `../study/frontend-portfolio/01-ops-triage-console/next/app/layout.tsx`: 앱 레이아웃과 메타데이터 경계를 고정하는 파일이다.
- `../study/frontend-portfolio/01-ops-triage-console/next/app/page.tsx`: 화면 진입점에서 최상위 composition과 초기 시연 흐름을 고정하는 파일이다.
- `../study/frontend-portfolio/01-ops-triage-console/next/src/components/console/issue-detail-dialog.tsx`: `arraysEqual`, `IssueDetailDialog`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-portfolio/01-ops-triage-console/next/src/components/console/ops-triage-console.tsx`: `issueTone`, `priorityTone`, `slaTone`, `toggleFacetValue`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/e2e/ops-triage.spec.ts`: `rowForIssue`, `tabTo`, `updates an issue from detail and can undo the change`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/integration/ops-triage-console.test.tsx`: `IntegrationHarness`, `renderHarness`, `ops triage hooks integration`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/setup.ts`: DOM/브라우저 테스트 환경 shim과 전역 hook을 고정하는 파일이다.

## 정답을 재구성하는 절차

1. `../study/frontend-portfolio/01-ops-triage-console/next/app/case-study/page.tsx`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `rowForIssue` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/ops-triage-console`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/ops-triage-console
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `rowForIssue`와 `tabTo`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/ops-triage-console`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/frontend-portfolio/01-ops-triage-console/next/app/case-study/page.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/app/layout.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/app/page.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/src/components/console/issue-detail-dialog.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/src/components/console/ops-triage-console.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/e2e/ops-triage.spec.ts`
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/integration/ops-triage-console.test.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/setup.ts`
- `../study/frontend-portfolio/01-ops-triage-console/next/tsconfig.json`
- `../study/frontend-portfolio/01-ops-triage-console/package.json`
