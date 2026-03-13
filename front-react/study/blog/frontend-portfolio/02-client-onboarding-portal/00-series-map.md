# 02 Client Onboarding Portal

sign-in, session gate, workspace profile, invite, review, submit retry를 하나의 고객-facing onboarding flow로 묶은 Next.js App Router 프로젝트다. 이 앱의 핵심은 기능 개수보다 저장, 복원, 재시도가 끊기지 않는 경험을 만드는 데 있다.

## 왜 글을 두 편으로 나눴는가

이 프로젝트는 흐름이 두 갈래로 나뉜다. 하나는 sign-in과 route gate를 먼저 세워 onboarding을 인증 문맥 위에 올리는 과정이고, 다른 하나는 draft save, reload restore, submit retry처럼 연속성과 복구 가능성을 다루는 과정이다. 둘을 한 편에 넣으면 긴장이 섞여서 읽기 어렵기 때문에 본문을 둘로 나눴다.

## 근거로 사용한 자료

- `frontend-portfolio/02-client-onboarding-portal/README.md`
- `frontend-portfolio/02-client-onboarding-portal/docs/concepts/validation-and-draft-flow.md`
- `frontend-portfolio/02-client-onboarding-portal/next/src/components/portal/sign-in-panel.tsx`
- `frontend-portfolio/02-client-onboarding-portal/next/src/components/portal/client-onboarding-portal.tsx`
- `frontend-portfolio/02-client-onboarding-portal/next/src/lib/storage.ts`
- `frontend-portfolio/02-client-onboarding-portal/next/src/lib/service.ts`
- `frontend-portfolio/02-client-onboarding-portal/next/tests/e2e/client-onboarding.spec.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/client-onboarding-portal`
- 2026-03-13 replay 기준 typecheck 통과, `vitest` 7개, Playwright 2개 시나리오 통과
- 같은 날짜 첫 verify replay에서는 `Draft saved to the local demo workspace.` 메시지를 5초 안에 찾지 못해 실패했고, 같은 날 재실행에서는 통과했다

## 읽는 순서

1. [10-turning-sign-in-into-an-onboarding-gate.md](10-turning-sign-in-into-an-onboarding-gate.md)
   - 왜 wizard보다 session gate를 먼저 세웠는지
2. [20-draft-restore-review-and-retry.md](20-draft-restore-review-and-retry.md)
   - draft save와 reload restore, submit retry, flaky feedback note까지 어떻게 읽어야 하는지
