# 02 Client Onboarding Portal structure

## opening frame

- 한 줄 훅: 이 프로젝트의 핵심은 많은 form field가 아니라, sign-in부터 submit retry까지의 route continuity를 끊지 않는 데 있다.
- chronology 주의: 코드 양은 크지만 전환점은 route gate와 portal mutation 흐름 쪽에 모여 있다.
- 첫 질문: session gate, validation, draft restore, submit retry를 어떤 경계로 묶어 고객-facing onboarding 경험으로 만들었는가.

## chapter flow

1. README와 problem 문서로 onboarding flow의 public contract를 먼저 고정한다.
2. `OnboardingRoute`와 `coerceStep`로 route/session gate를 설명한다.
3. `ClientOnboardingPortal`과 verify 결과로 draft/save/retry 흐름을 닫는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log`
- 본문 1: `next/src/components/portal/onboarding-route.tsx`
- 본문 2: `next/src/components/portal/client-onboarding-portal.tsx`
- 본문 3: `npm run verify --workspace @front-react/client-onboarding-portal`, `next/tests/*`

## tone guardrails

- form field 나열보다 route continuity와 recovery path에 집중한다.
- validation, draft, retry를 separate checklist로 쓰지 않고 하나의 onboarding loop로 이어서 설명한다.
- notion과 새 blog는 입력 근거에서 제외한다.
