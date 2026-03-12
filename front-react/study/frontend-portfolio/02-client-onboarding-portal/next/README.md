# Next.js 구현

상태: `verified`

## 이 구현이 답하는 범위

- sign-in과 session gate
- onboarding wizard와 workspace profile
- member invite, review, submit retry
- unit, integration, E2E 검증

## 핵심 파일

- `app/`: App Router 엔트리와 route 구조
- `src/components/portal/client-onboarding-portal.tsx`: onboarding main UI
- `src/lib/guards.ts`, `schemas.ts`, `storage.ts`, `service.ts`: guard, validation, draft, service 경계
- `tests/`: unit, integration, E2E 검증

## 실행과 검증

```bash
cd study
npm run dev --workspace @front-react/client-onboarding-portal
npm run verify --workspace @front-react/client-onboarding-portal
```

## 현재 한계

- 실제 auth backend와 server database는 없다.
- multi-user collaboration과 email delivery는 다루지 않는다.
- form flow는 제품형이지만 도메인 범위는 onboarding에 한정된다.
