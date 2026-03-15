# 01-ops-triage-console 문제지

## 왜 중요한가

Ops Triage Console은 여러 채널에서 들어오는 이슈를 한 명의 운영자가 빠르게 정리하고 우선순위를 지정하며 적절한 팀으로 라우팅하는 콘솔이다. 이 문제의 핵심은 data-heavy queue에서도 읽기 흐름, bulk 작업, failure recovery가 무너지지 않게 만드는 것이다.

## 목표

시작 위치의 구현을 완성해 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다, 단일 운영자 시나리오를 기준으로 한다, 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/frontend-portfolio/01-ops-triage-console/next/app/case-study/page.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/app/layout.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/app/page.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/src/components/console/issue-detail-dialog.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/e2e/ops-triage.spec.ts`
- `../study/frontend-portfolio/01-ops-triage-console/next/tests/integration/ops-triage-console.test.tsx`
- `../study/frontend-portfolio/01-ops-triage-console/next/tsconfig.json`
- `../study/frontend-portfolio/01-ops-triage-console/package.json`

## starter code / 입력 계약

- `../study/frontend-portfolio/01-ops-triage-console/next/app/case-study/page.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다.
- 단일 운영자 시나리오를 기준으로 한다.
- 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다.
- dashboard summary
- searchable triage queue
- faceted filters
- saved views
- bulk actions
- issue detail panel
- operator note
- demo reset
- chaos/failure simulation
- next/에 실행 가능한 운영 콘솔 구현
- 제품 판단과 UX 흐름을 설명하는 공개 문서와 발표 자료
- typecheck, unit, integration, E2E를 포함한 검증 체계

## 제외 범위

- 실제 인증
- 실제 DB
- 멀티유저 실시간 협업

## 성공 체크리스트

- 핵심 흐름은 `sections`와 `metadata`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `rowForIssue`와 `tabTo`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/frontend-portfolio/01-ops-triage-console/next/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `cd study && npm run verify --workspace @front-react/ops-triage-console`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/ops-triage-console
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-ops-triage-console_answer.md`](01-ops-triage-console_answer.md)에서 확인한다.
