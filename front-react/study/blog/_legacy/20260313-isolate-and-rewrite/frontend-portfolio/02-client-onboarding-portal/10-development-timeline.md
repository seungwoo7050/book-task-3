# 02 Client Onboarding Portal development timeline

`02-client-onboarding-portal`을 source-first로 다시 읽으면, 보이는 것보다 훨씬 분명한 축이 있다. `study/frontend-portfolio/02-client-onboarding-portal`의 README, route wrapper, portal component, tests, 그리고 2026-03-13 재검증 결과를 함께 보면 이 프로젝트는 많은 입력 폼을 만드는 일보다 sign-in 이후 submit까지의 연속 경험을 끊지 않는 데 더 가깝다.

## 구현 순서 요약

1. README와 problem 문서로 session gate, onboarding wizard, draft restore, submit retry가 public contract라는 점을 먼저 고정했다.
2. `OnboardingRoute`에서 route/session 경계를 분리하고, `ClientOnboardingPortal`에서 profile/invite/review/submit mutations를 하나의 portal loop로 읽었다.
3. 마지막에는 `npm run verify --workspace @front-react/client-onboarding-portal`로 typecheck, vitest, Playwright를 다시 통과시켰다.

## 2026-03-08 / Phase 1 - onboarding flow의 public contract를 먼저 고정한다

- 당시 목표:
  form UI보다 route continuity를 먼저 붙잡는다.
- 변경 단위:
  `README.md`, `problem/README.md`, `next/README.md`, `package.json`
- 처음 가설:
  onboarding 프로젝트라서 schema validation이 중심처럼 보이지만, README를 보면 실제 본론은 session gate와 submit retry를 포함한 end-to-end flow였다.
- 실제 진행:
  README와 problem 문서를 읽으며 sign-in, wizard, draft restore, retry를 포함 범위로 먼저 고정했고, `git log --reverse --stat`로 route/app, portal component, tests가 한 묶음으로 landing된 사실을 확인했다.

CLI:

```bash
$ git log --reverse --stat -- study/frontend-portfolio/02-client-onboarding-portal | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... next/src/components/portal/onboarding-route.tsx
... next/src/components/portal/client-onboarding-portal.tsx
... next/tests/integration/client-onboarding-portal.test.tsx
... next/tests/e2e/client-onboarding.spec.ts
```

검증 신호:

- source tree가 route wrapper, portal component, unit/integration/E2E tests를 같이 가져서, 이 프로젝트가 multi-step flow contract를 중심으로 설계됐다는 점이 분명했다.

핵심 코드:

```tsx
export function OnboardingRoute() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const step = coerceStep(searchParams.get("step"));
```

왜 이 코드가 중요했는가:

route wrapper가 짧다고 중요하지 않은 건 아니다. `coerceStep`로 query param을 정규화한 뒤 `ClientOnboardingPortal`로 넘기는 순간, 이 프로젝트는 step state를 form internals가 아니라 URL-level navigation state로 다루기 시작한다.

새로 배운 것:

- 고객-facing flow에서는 step state를 컴포넌트 local state에만 두지 않는 편이 복원성과 직접 링크 공유 측면에서 훨씬 낫다.

다음:

- portal 내부에서 draft/save/retry가 어떤 mutation 흐름으로 붙는지 본다.

## 2026-03-08 / Phase 2 - portal 내부에 draft, invite, submit retry를 한 루프로 묶는다

- 당시 목표:
  multi-step flow가 여러 form 조각이 아니라 하나의 portal loop라는 점을 확인한다.
- 변경 단위:
  `next/src/components/portal/client-onboarding-portal.tsx`, `next/src/lib/guards.ts`, `next/src/lib/schemas.ts`, `next/src/lib/storage.ts`
- 처음 가설:
  step별 form만 잘 만들어도 될 것 같지만, 실제 제품 경험은 session query, profile query, invite query, checklist query, submit mutation이 계속 이어지는지에 달려 있다고 봤다.
- 실제 진행:
  `rg -n`으로 `ClientOnboardingPortal`, `saveProfileMutation`, `submitMutation` 위치를 확인하고, 여러 query와 mutation이 어떻게 `canSubmit`과 `refreshPortalData`로 이어지는지 읽었다.

CLI:

```bash
$ rg -n 'OnboardingRoute|ClientOnboardingPortal|saveProfileMutation|submitMutation' \
  study/frontend-portfolio/02-client-onboarding-portal/next/src/components/portal/onboarding-route.tsx \
  study/frontend-portfolio/02-client-onboarding-portal/next/src/components/portal/client-onboarding-portal.tsx
onboarding-route.tsx:7:export function OnboardingRoute()
client-onboarding-portal.tsx:35:export function ClientOnboardingPortal(
client-onboarding-portal.tsx:100:  const saveProfileMutation = useMutation({
client-onboarding-portal.tsx:129:  const submitMutation = useMutation({
```

검증 신호:

- route wrapper와 portal component가 step/navigation/submit 흐름의 가장 바깥 경계를 분명히 나눠 주고 있었다.

핵심 코드:

```ts
const submitMutation = useMutation({
  mutationFn: async () => {
    if (shouldFailNextSubmit) {
      setFailNextSubmit(true);
    }
    return submitOnboarding();
  },
  onError: (error: Error) => {
    setSubmitError(error.message);
  },
});
```

왜 이 코드가 중요했는가:

고객-facing onboarding에서 가장 중요한 건 성공 path만 매끈한 것이 아니다. 제출 실패를 일부러 surface에 올리고, 그 상태를 UI에서 다시 회복할 수 있게 만드는 순간 이 프로젝트는 단순 wizard demo를 넘어 제품형 flow가 된다.

새로 배운 것:

- multi-step flow의 설득력은 validation completeness보다 failure recovery와 draft continuity에서 더 크게 나온다.

다음:

- verify가 direct access guard와 draft restore/retry를 실제로 닫는지 본다.

## 2026-03-13 / Phase 3 - verify로 route와 recovery path를 닫는다

- 당시 목표:
  고객-facing onboarding contract를 현재 시점의 CLI 결과로 다시 고정한다.
- 변경 단위:
  `next/tests/unit/*`, `next/tests/integration/*`, `next/tests/e2e/*`, `next/tsconfig.json`
- 처음 가설:
  integration test만으로도 충분해 보일 수 있지만, direct access guard와 submit retry는 E2E까지 같이 봐야 한다고 판단했다.
- 실제 진행:
  canonical verify를 다시 실행해 typecheck, `7`개 tests, Playwright `2`개 시나리오를 모두 확보했다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/client-onboarding-portal
> tsc --noEmit -p next/tsconfig.json
Test Files  4 passed (4)
Tests  7 passed (7)
Running 2 tests using 1 worker
✓ guards direct onboarding access without a session
✓ supports sign-in, draft restore, and submit retry
2 passed (12.9s)
```

검증 신호:

- route guard와 full onboarding recovery path가 각각 별도 E2E 시나리오로 존재해 public contract가 선명했다.
- typecheck와 unit/integration tests가 form schema, storage, route guard correctness를 먼저 닫아 줬다.

핵심 코드:

```tsx
<ClientOnboardingPortal
  step={step}
  onStepChange={(nextStep) => {
    router.replace(`/onboarding?step=${nextStep}`);
  }}
/>
```

왜 이 코드가 중요했는가:

step 전환을 `router.replace`로 밀어 넣는 이 지점이 route continuity의 핵심이다. 사용자는 wizard를 넘긴다고 느끼지만, 코드 관점에서는 step state가 URL과 동기화되므로 새로고침과 direct link에서도 같은 흐름을 복원할 수 있다.

새로 배운 것:

- 고객-facing onboarding에서 route를 무시한 local wizard state는 금방 취약해진다. 복원성과 guard를 챙기려면 URL-level state가 필요하다.

다음:

- 실제 auth backend, database, email delivery는 아직 없다. 이 프로젝트는 onboarding domain을 좁게 유지한 제품형 데모로 끝난다.

## 남은 경계

- 실제 auth backend와 server database는 없다.
- email delivery와 multi-user collaboration도 다루지 않는다.
- onboarding domain 밖의 billing/admin 영역으로는 확장하지 않는다.
