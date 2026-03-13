# 01 Ops Triage Console

support, QA, customer feedback, monitoring에서 올라온 이슈를 한 명의 운영자가 빠르게 triage하도록 만든 Next.js internal tool이다. 이 프로젝트는 화면 밀도만 높은 데모가 아니라, optimistic update와 rollback, retry, keyboard path까지 포함한 "운영 surface"를 만드는 데 초점이 맞춰져 있다.

## 왜 글을 세 편으로 나눴는가

이 프로젝트는 구현 축이 세 갈래로 뚜렷하게 갈린다. 먼저 운영자가 실제로 머무는 화면 surface를 만들고, 그다음 낙관적 변경을 되돌릴 수 있게 만들고, 마지막에 failure와 e2e 시나리오로 그 선택을 증명한다. 한 편에 모두 넣으면 화면 설계와 상태 복구 이야기가 서로를 가리기 쉬워서 본문을 분리했다.

## 근거로 사용한 자료

- `frontend-portfolio/01-ops-triage-console/README.md`
- `frontend-portfolio/01-ops-triage-console/docs/concepts/ux-and-state-flow.md`
- `frontend-portfolio/01-ops-triage-console/next/src/components/console/ops-triage-console.tsx`
- `frontend-portfolio/01-ops-triage-console/next/src/hooks/use-ops-triage.ts`
- `frontend-portfolio/01-ops-triage-console/next/src/lib/simulate.ts`
- `frontend-portfolio/01-ops-triage-console/next/tests/integration/ops-triage-console.test.tsx`
- `frontend-portfolio/01-ops-triage-console/next/tests/e2e/ops-triage.spec.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/ops-triage-console`
- 2026-03-13 replay 기준 typecheck 통과, `vitest` 16개, Playwright 4개 시나리오 통과

## 읽는 순서

1. [10-building-the-triage-surface.md](10-building-the-triage-surface.md)
   - 운영자가 실제로 머무는 dense surface를 어떻게 구성했는지
2. [20-making-optimistic-actions-reversible.md](20-making-optimistic-actions-reversible.md)
   - 빠른 UI보다 rollback 가능한 mutation이 더 중요했던 이유
3. [30-proving-the-console-under-failure.md](30-proving-the-console-under-failure.md)
   - failure simulation, retry, keyboard-only path를 검증으로 증명한 기록
