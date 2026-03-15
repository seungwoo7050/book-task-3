# 02-client-onboarding-portal 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다, route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다, draft restore와 submit retry가 검증 가능한 시나리오여야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `sections`와 `metadata`, `stepTitles` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다.
- route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다.
- draft restore와 submit retry가 검증 가능한 시나리오여야 한다.
- 첫 진입점은 `../study/frontend-portfolio/02-client-onboarding-portal/next/app/case-study/page.tsx`이고, 여기서 `sections`와 `metadata` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/case-study/page.tsx`: 화면 진입점에서 최상위 composition과 초기 시연 흐름을 고정하는 파일이다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/layout.tsx`: 앱 레이아웃과 메타데이터 경계를 고정하는 파일이다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/onboarding/page.tsx`: 핵심 구현을 담는 파일이다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/page.tsx`: 화면 진입점에서 최상위 composition과 초기 시연 흐름을 고정하는 파일이다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/src/components/portal/client-onboarding-portal.tsx`: `stepTitles`, `ClientOnboardingPortal`, `Field`, `SummaryCard`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/e2e/client-onboarding.spec.ts`: `guards direct onboarding access without a session`, `supports sign-in, draft restore, and submit retry`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/integration/client-onboarding-portal.test.tsx`: `renderPortal`, `ClientOnboardingPortal`, `shows the route guard when no session exists`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/setup.ts`: DOM/브라우저 테스트 환경 shim과 전역 hook을 고정하는 파일이다.

## 정답을 재구성하는 절차

1. `../study/frontend-portfolio/02-client-onboarding-portal/next/app/case-study/page.tsx`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `guards direct onboarding access without a session` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/client-onboarding-portal`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/client-onboarding-portal
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/02-client-onboarding-portal && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/02-client-onboarding-portal && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `guards direct onboarding access without a session`와 `supports sign-in, draft restore, and submit retry`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/client-onboarding-portal`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/case-study/page.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/layout.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/onboarding/page.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/app/page.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/src/components/portal/client-onboarding-portal.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/e2e/client-onboarding.spec.ts`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/integration/client-onboarding-portal.test.tsx`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tests/setup.ts`
- `../study/frontend-portfolio/02-client-onboarding-portal/next/tsconfig.json`
- `../study/frontend-portfolio/02-client-onboarding-portal/package.json`
