# Turning Sign-In Into An Onboarding Gate

고객-facing onboarding을 만들 때 흔한 유혹은 바로 wizard 화면부터 만드는 것이다. 하지만 이 프로젝트를 읽다 보면 실제 첫 번째 문제는 step이 아니라 gate였다는 사실이 보인다. 인증 문맥이 없는 상태에서 onboarding 화면을 보여 주면, route도 데이터 로딩도 결국 같은 예외를 계속 반복해서 떠안아야 하기 때문이다.

그래서 이 앱은 sign-in을 단순한 전 단계로 두지 않고 onboarding의 첫 번째 문턱으로 만들었다. 사용자가 왜 막혔는지 이해할 수 있어야 하고, 동시에 세션이 생긴 뒤에는 wizard가 그 문맥을 당연한 전제로 받아들일 수 있어야 했다. 이 순서 덕분에 뒤의 draft restore와 submit retry도 더 단순하게 설명된다.

즉 이 글의 주제는 로그인 화면이 아니라 경계 설정이다. onboarding은 어디서부터 시작하는가, 그리고 그 시작점을 누가 책임지는가.

## 구현 순서를 먼저 짚으면

- sign-in panel과 onboarding route를 분리해 인증 없는 진입을 먼저 차단했다.
- `sessionQuery`를 기준으로 나머지 query를 켜고 끄며 route guard와 데이터 로딩 규칙을 맞췄다.
- typecheck와 테스트로 이 gate가 뒤 단계의 기본 전제가 되도록 고정했다.

## wizard보다 먼저 필요한 건 "왜 여기서 막히는가"를 설명하는 문턱이었다

`ClientOnboardingPortal`은 세션이 없으면 onboarding UI를 아예 렌더하지 않는다. 대신 sign-in이 먼저 필요하다는 카드를 보여 준다. 그리고 profile, invites, checklist query도 세션이 있을 때만 활성화된다.

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
...
if (!sessionQuery.data) {
  return (
    <main>
      <section>Sign in before opening the onboarding flow</section>
    </main>
  );
}
```

이 코드가 중요한 이유는 route guard와 data loading이 같은 규칙을 공유하기 때문이다. 인증이 없는 상태에서는 onboarding용 query를 괜히 돌리지 않고, 사용자는 왜 review step에 바로 못 들어가는지도 즉시 이해할 수 있다.

여기서 얻은 감각은 단순했다. 고객-facing wizard의 첫 invariant는 step 순서가 아니라 session gate였다. 인증 문맥을 먼저 세우지 않으면 이후의 form과 route가 모두 예외 처리 코드로 부풀기 쉽다.

## sign-in panel은 onboarding으로 들어가는 손잡이여야 했다

`SignInPanel`도 같은 철학으로 읽힌다. sign-in 성공 후에는 세션 query를 invalidate하고 곧바로 `/onboarding?step=workspace`로 이동한다. 즉 login은 독립된 세계가 아니라 onboarding gate를 여는 동작이다.

```tsx
const signInMutation = useMutation({
  mutationFn: signIn,
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ["session"] });
    router.push("/onboarding?step=workspace");
  },
});
```

이 흐름은 사소해 보이지만 onboarding 경험을 자연스럽게 만든다. 사용자는 로그인에 성공한 뒤 다시 시작점을 고르지 않는다. 곧바로 workspace step으로 들어간다. 반대로 세션이 살아 있으면 `Continue onboarding` 버튼이 같은 route로 되돌려 보낸다.

즉 sign-in panel은 멋진 landing screen이 아니라 onboarding 진입 손잡이다. 이걸 일찍 분명히 해 두었기 때문에, 뒤의 wizard는 인증 예외를 거의 의식하지 않고 순수한 step 흐름에 집중할 수 있다.

## 이 gate를 먼저 세웠기 때문에 뒤 단계의 연속성도 설명 가능해졌다

이 단계의 검증은 화려하지 않다. 하지만 중요하다.

```bash
cd study
npm run typecheck --workspace @front-react/client-onboarding-portal
npm run test --workspace @front-react/client-onboarding-portal
```

2026-03-13 replay 기준으로 typecheck가 통과했고, `vitest` 7개 테스트가 green이었다. 이 중에는 route guard와 validation, storage 복원, integration flow가 함께 들어 있다. 즉 이 앱의 첫 번째 신뢰는 로그인 자체가 아니라, 인증이 onboarding의 전제로 잘 정리돼 있다는 사실에서 나온다.

다음 글로 넘어가면 초점이 바뀐다. gate가 세워진 뒤에는 사용자가 저장하고 떠났다 돌아오고, 제출이 실패하면 다시 시도하는 긴 흐름을 어떻게 유지할 것인가가 더 중요해진다.
