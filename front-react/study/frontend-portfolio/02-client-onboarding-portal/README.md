# 02 Client Onboarding Portal

상태: `verified`

## 무슨 문제인가

고객-facing onboarding flow에서는 sign-in, session gate, workspace validation, draft restore, member invite, review, submit retry가 하나의 연속된 경험으로 이어져야 한다. 이 프로젝트는 multi-step onboarding을 제품처럼 설계하고 검증하는 문제를 푼다.

## 왜 필요한가

`Ops Triage Console`이 내부도구형 UI에 강하다면, 이 프로젝트는 고객-facing form과 route flow를 보여 준다. 두 축이 함께 있어야 "내부도구 + 고객-facing 제품" 포트폴리오가 완성된다.

## 내가 만든 답

sign-in, onboarding wizard, workspace profile, invite, review and submit 흐름을 갖춘 Next.js App Router 기반 포털을 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [next/README.md](next/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `next/src/components/portal/client-onboarding-portal.tsx`에서 전체 onboarding 상태와 화면 구성을 묶는다.
- `next/src/components/portal/onboarding-route.tsx`, `sign-in-panel.tsx`에서 session gate와 route step 전환을 분리한다.
- `next/src/lib/guards.ts`, `schemas.ts`, `storage.ts`, `service.ts`에서 guard, validation, draft, mock service 경계를 나눈다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/client-onboarding-portal
npm run verify --workspace @front-react/client-onboarding-portal
```

- 검증 기준일: 2026-03-08
- `typecheck`: `next/tsconfig.json` 기준 타입 검사 통과
- `vitest`: schema validation, draft storage, route guard, onboarding integration 확인
- `playwright`: sign-in -> validation -> draft restore -> retry -> success 흐름 확인

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [next/README.md](next/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 실제 auth backend, server database, email delivery는 다루지 않는다.
- 도메인 범위는 onboarding에 집중하며, billing이나 organization admin까지 확장하지 않는다.
- 포트폴리오 폭은 충분하므로 이후 확장은 새 앱보다 문서와 polish를 다듬는 쪽이 더 중요하다.
