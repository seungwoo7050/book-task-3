# 02-client-onboarding-portal 문제지

## 왜 중요한가

Client Onboarding Portal은 SaaS 고객이 첫 로그인 이후 workspace profile을 채우고, 팀원을 초대하고, 최종 제출까지 마치는 onboarding 앱이다. 이 문제의 핵심은 session gate, validation, draft restore, retry를 포함한 multi-step flow를 자연스럽게 연결하는 것이다.

## 목표

시작 위치의 구현을 완성해 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다, route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다, draft restore와 submit retry가 검증 가능한 시나리오여야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/case-study/page.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/layout.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/onboarding/page.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/page.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/e2e/client-onboarding.spec.ts`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/integration/client-onboarding-portal.test.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tsconfig.json`
- `../study/frontend-portfolio/02-client-onboarding-portal/package.json`

## starter code / 입력 계약

- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/case-study/page.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다.
- route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다.
- draft restore와 submit retry가 검증 가능한 시나리오여야 한다.
- sign-in / session gate
- onboarding wizard
- workspace profile/settings
- member invite
- review and submit
- draft save and restore
- submit failure and retry
- next/에 실행 가능한 onboarding 포털 구현
- route와 validation 흐름을 설명하는 공개 문서와 발표 자료
- typecheck, unit, integration, E2E를 포함한 검증 체계

## 제외 범위

- 실제 auth backend
- 실제 DB와 email delivery
- organization admin 전반

## 성공 체크리스트

- 핵심 흐름은 `sections`와 `metadata`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `guards direct onboarding access without a session`와 `supports sign-in, draft restore, and submit retry`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `cd study && npm run verify --workspace @front-react/client-onboarding-portal`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/client-onboarding-portal
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/02-client-onboarding-portal && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/02-client-onboarding-portal && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-client-onboarding-portal_answer.md`](02-client-onboarding-portal_answer.md)에서 확인한다.
