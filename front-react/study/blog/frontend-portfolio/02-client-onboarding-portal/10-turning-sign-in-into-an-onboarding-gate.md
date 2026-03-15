# Turning Sign-In Into An Onboarding Gate

이 프로젝트를 처음 읽으면 multi-step wizard가 중심처럼 보이지만, 실제 소스는 다른 순서를 보여 준다. 먼저 세운 것은 step UI가 아니라 "세션이 없으면 onboarding 자체를 열지 않는다"는 경계다. 이 선택이 없으면 `/onboarding?step=review` 같은 직접 진입, query 실행 범위, submit readiness 계산이 모두 각자 예외 처리를 안고 가야 한다.

내가 다시 확인한 흐름은 세 단계였다. 문제 정의 문서가 sign-in, session gate, validation, draft restore, retry를 하나의 경험으로 묶어 달라고 요구한다. `sign-in-panel.tsx`는 성공 즉시 `/onboarding?step=workspace`로 보낸다. `client-onboarding-portal.tsx`는 `sessionQuery.data`가 없으면 onboarding UI를 렌더하지 않고 guard card를 보여 준다. 이 세 조각이 합쳐져서 "로그인 화면 다음에 wizard가 있는 것"이 아니라 "로그인이 onboarding gate 그 자체인 것"으로 구조가 굳어진다.

## 첫 번째 단계는 route를 예쁘게 나누는 게 아니라 session rule을 하나로 만드는 일이었다

`OnboardingRoute`는 URL에서 `step`을 읽지만, 무슨 값이 들어와도 그대로 믿지 않는다.

```tsx
const step = coerceStep(searchParams.get("step"));
```

`coerceStep()`은 `workspace | invites | review`만 허용하고 나머지는 `workspace`로 되돌린다. 여기서 첫 번째 안정성이 생긴다. direct link가 들어와도 step state가 깨지지 않는다. 그다음 실제 gate는 `ClientOnboardingPortal`이 만든다.

```tsx
const sessionQuery = useQuery({
  queryKey: ["session"],
  queryFn: getSession,
});
const profileQuery = useQuery({
  enabled: Boolean(sessionQuery.data),
  queryKey: ["workspace-profile"],
  queryFn: getWorkspaceProfile,
});
```

이 구조가 중요한 이유는 "세션이 없으면 화면만 막는다"에서 끝나지 않기 때문이다. profile, invites, checklist query 모두 세션 존재 여부를 같은 규칙으로 공유한다. 즉 guard와 data loading이 서로 다른 두 장치가 아니라 동일한 boundary를 두 번 표현한 셈이다.

## sign-in panel은 시작 페이지가 아니라 onboarding 진입 핸들이다

`SignInPanel`은 별도 auth 시스템을 흉내 내지 않는다. `signInSchema`로 email/password 최소 조건만 검증하고, `signIn()`은 브라우저 저장소에 session을 적은 뒤 즉시 onboarding route로 넘긴다.

```tsx
const signInMutation = useMutation({
  mutationFn: signIn,
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ["session"] });
    router.push("/onboarding?step=workspace");
  },
});
```

여기서 중요한 건 "로그인 성공 후 어디로 보내는가"다. 별도 dashboard나 menu를 거치지 않고 workspace step으로 직행한다. 반대로 세션이 이미 있으면 sign-in form 대신 active session 카드와 `Continue onboarding` 버튼을 보여 준다. 즉 로그인 화면은 독립 제품이 아니라 onboarding funnel의 입구다.

동시에 이 sign-in이 무엇을 하지 않는지도 같이 적어 두는 편이 정확하다. 이 프로젝트는 서버에 계정을 확인하지 않는다. `owner@latticecloud.dev` 같은 기본값은 데모 편의를 위한 것이고, 실제 계약은 "유효한 work email + 8자 이상 password를 local session으로 저장한다"에 가깝다. 그래서 여기서 검증되는 것은 real auth correctness가 아니라 onboarding gate shape다.

문제 정의가 요구한 것도 이 구조와 맞다. 범위는 sign-in, session gate, workspace validation, member invite, review, retry까지다. login만 예쁘게 만드는 프로젝트가 아니라, 고객-facing onboarding을 세션 문맥 위에 올리는 프로젝트다.

## guard를 먼저 세웠기 때문에 뒤 단계의 책임도 분명해졌다

guard가 먼저 생기면 나머지 step은 더 단순한 책임을 진다.

- `workspace`: launch-ready profile 입력과 저장
- `invites`: 첫 운영자 초대
- `review`: checklist 완료와 submit 실행

이 단순화 덕분에 `canSubmitOnboarding()`도 비교적 정직하다. 완성된 profile, 초대 1건 이상, checklist 3개 완료가 submit 가능 조건의 전부다. "어떤 step에 있느냐"보다 "준비가 되었느냐"가 submit gate가 된다.

또 하나 눈에 띈 점은 현재 구현이 "입장 제한"까지만 한다는 것이다. step 간 이동 자체는 강한 linear enforcement가 아니다. 사용자는 workspace를 저장하지 않아도 `Go to invites`, `Continue to review` 버튼으로 이동할 수 있다. 대신 마지막 submit 버튼만 `canSubmit`으로 잠긴다. 즉 이 앱은 wizard navigation을 엄격히 차단하는 대신, review 시점에서 readiness를 보여 주는 쪽을 택했다. 이건 source를 보고 확인한 현재 제품 선택이다.

## 테스트가 실제로 고정해 주는 것은 무엇인가

2026-03-14에 다시 돌린 검증은 아래 한 줄이었다.

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study
npm run verify --workspace @front-react/client-onboarding-portal
```

이 검증이 보장하는 핵심은 세 가지다.

- unit test: `coerceStep()`과 `canSubmitOnboarding()`이 URL fallback과 submit readiness 규칙을 고정한다.
- integration test: 세션이 없을 때 guard 카드가 보이고, sign-in 이후 step progression이 이어진다.
- E2E test: `/onboarding?step=review` 직접 진입이 실제 브라우저에서 sign-in gate로 되돌아간다.

반대로 테스트가 아직 직접 잠그지 않는 것도 있다. "step을 순서대로만 밟아야 한다"는 강한 선형 규칙은 현재 구현 자체가 채택하지 않았고, multi-tab session 충돌이나 server-backed auth 회복도 범위 밖이다.

즉 이 문서의 결론은 단순하다. 이 프로젝트의 첫 문제는 wizard가 아니라 boundary였다. session 문맥을 선명하게 세워 두었기 때문에, 뒤 글에서 다룰 draft restore와 retry도 "이미 onboarding 안에 들어온 사용자"라는 전제 위에서 집중해서 설명할 수 있다.
