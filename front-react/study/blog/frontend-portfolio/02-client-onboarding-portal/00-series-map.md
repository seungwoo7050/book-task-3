# 02 Client Onboarding Portal

이 프로젝트의 핵심은 "폼이 많은 onboarding"이 아니라 "로그인부터 제출 재시도까지 흐름이 안 끊기는가"를 검증하는 데 있다. 실제 구현을 읽어 보면 route guard, step query enable 조건, `localStorage` 기반 draft 복원, review 단계의 의도적 submit failure 토글이 같은 문제를 다른 면에서 다룬다. 사용자가 어디서 들어와도 왜 막히는지 설명되고, 저장했다가 돌아왔을 때 이전 상태를 다시 잡을 수 있어야 하며, 마지막 제출 실패도 데모 가능한 surface로 남겨야 한다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다. 문제 정의는 `front-react/study/frontend-portfolio/02-client-onboarding-portal/problem/README.md`, 구현 경계는 `README.md`, `next/README.md`, `next/src/components/portal/client-onboarding-portal.tsx`, `next/src/components/portal/sign-in-panel.tsx`, `next/src/components/portal/onboarding-route.tsx`, `next/src/lib/guards.ts`, `next/src/lib/schemas.ts`, `next/src/lib/service.ts`, `next/src/lib/storage.ts`, 검증 근거는 `next/tests/unit/*.test.ts`, `next/tests/integration/client-onboarding-portal.test.tsx`, `next/tests/e2e/client-onboarding.spec.ts`, 그리고 2026-03-14 재실행한 `npm run verify --workspace @front-react/client-onboarding-portal`이다.

## 이 프로젝트를 읽는 질문

- onboarding wizard보다 먼저 해결해야 하는 경계는 무엇이었는가
- 저장과 복원은 단순 persistence가 아니라 어떤 UX 약속을 만들었는가
- 마지막 submit은 성공 path보다 어떤 실패/retry surface를 보여 주는가

## 문서 순서

1. [10-turning-sign-in-into-an-onboarding-gate.md](10-turning-sign-in-into-an-onboarding-gate.md)
   - session gate, query enable 조건, URL step coercion이 어떻게 같은 경계를 만든는지 정리한다.
2. [20-draft-restore-review-and-retry.md](20-draft-restore-review-and-retry.md)
   - draft save, reload restore, checklist gating, retryable submit error가 어떻게 이어지는지 따라간다.

## 이번에 다시 확인한 검증 상태

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study
npm run verify --workspace @front-react/client-onboarding-portal
```

- `typecheck`: 통과
- `vitest`: 4개 파일, 7개 테스트 통과
- `playwright`: 2개 시나리오 통과

## 지금 문서에서 분명히 남기는 한계

- 실제 auth backend, server database, email delivery는 없다.
- sign-in은 실제 계정 조회가 아니라 `signInSchema`를 통과한 값을 브라우저 session으로 적는 local demo 경로다.
- session과 onboarding draft는 전부 브라우저 `localStorage`에 머문다.
- step 이동은 일부러 loose하고, 최종 submit gate만 엄격하다.
- 이번 검증은 single-browser 흐름의 sign-in, guard, draft restore, retry를 잠그지만 multi-tab conflict, background autosave, server sync는 다루지 않는다.
- collaborative onboarding, invite acceptance 이후의 org admin 흐름은 범위 밖이다.
