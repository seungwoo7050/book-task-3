# 디버그 기록 — Client Onboarding Portal에서 마주친 문제들

## draft restore 후 폼 값이 비어 있음

### 증상

workspace 프로필을 저장하고 페이지를 새로고침했는데, 폼 필드가 모두 빈값으로 보였다.

### 원인

React Hook Form의 `defaultValues`로 `defaultWorkspaceProfile`(빈 문자열)을 넣었다. `profileQuery.data`가 로드되기 전에 폼이 먼저 렌더링되면서 빈값이 보인다. `useForm`의 `defaultValues`는 최초 한 번만 적용되므로, 이후에 데이터가 도착해도 폼이 자동으로 갱신되지 않는다.

### 해결

`useEffect`에서 `profileQuery.data`가 변경되면 `workspaceForm.reset(profileQuery.data)`를 호출한다:

```typescript
useEffect(() => {
  if (profileQuery.data) {
    workspaceForm.reset(profileQuery.data);
  }
}, [profileQuery.data, workspaceForm]);
```

이렇게 하면 첫 로드와 새로고침 모두에서 저장된 draft가 폼에 채워진다.

## coerceStep이 잘못된 step을 그대로 통과시킴

### 증상

`/onboarding?step=admin` 같은 존재하지 않는 step을 URL에 입력하면, 빈 화면이 렌더링됐다.

### 원인

초기 구현에서 `coerceStep`이 `onboardingSteps.includes(value)` 체크만 하고, 실패 시 undefined를 반환했다. `step`이 undefined이면 workspace/invites/review 어떤 조건문에도 걸리지 않는다.

### 해결

```typescript
export function coerceStep(value: string | null | undefined): OnboardingStep {
  if (value === "workspace" || value === "invites" || value === "review") {
    return value;
  }
  return "workspace"; // 안전한 기본값
}
```

명시적 리터럴 비교 3개로 타입을 좁히고, 나머지는 모두 `"workspace"`로 떨어뜨린다.

## 세션이 있는데 route guard가 표시됨

### 증상

로그인 후 `/onboarding`으로 이동하면, 잠깐 route guard 화면이 보였다가 onboarding 콘텐츠로 바뀌었다.

### 원인

`sessionQuery`의 초기 상태가 `isLoading`인 동안에는 `sessionQuery.data`가 undefined다. 원래 코드에서는 loading 상태를 별도 처리하지 않고 `!sessionQuery.data`로 바로 guard를 보여 줬다.

### 해결

loading 상태를 먼저 처리한다:

```typescript
if (sessionQuery.isLoading) {
  return <main>Loading session...</main>;
}

if (!sessionQuery.data) {
  return <section>Sign in before opening the onboarding flow</section>;
}
```

이렇게 하면 세션 쿼리가 완료될 때까지 loading 표시가 보이고, guard는 실제로 세션이 없을 때만 나타난다.

## Zod validation 에러가 폼에 표시되지 않음

### 증상

complianceEmail에 잘못된 형식을 입력하고 Save draft를 눌렀는데, 에러 메시지가 보이지 않았다.

### 원인

`zodResolver`가 에러를 `formState.errors`에 넣지만, 컴포넌트에서 에러 메시지를 렌더링하는 부분이 누락되었다.

### 해결

`Field` 컴포넌트에 error prop을 추가:

```tsx
function Field({ label, error, children }) {
  return (
    <label className="grid gap-2 text-sm font-semibold text-stone-800">
      {label}
      {children}
      {error ? <span className="text-sm text-red-700">{error}</span> : null}
    </label>
  );
}
```

각 필드에 `error={workspaceForm.formState.errors.fieldName?.message}`를 전달한다.

## submit 실패 후 에러 메시지가 사라지지 않음

### 증상

"Simulate the next submit failure"를 켜고 submit → 에러 발생 → 체크박스를 끄고 다시 submit → 성공했는데, 에러 메시지가 여전히 보였다.

### 원인

submitMutation의 onSuccess에서 `setSubmitError("")`를 호출하기 전에 `setSubmitResult(result)`를 호출했는데, 두 setState가 같은 렌더 사이클에서 배치 처리되지 않는 경우가 있었다.

### 해결

onSuccess에서 에러를 먼저 clear한 뒤 결과를 설정하도록 순서를 맞추고, onError에서도 결과를 clear한다:

```typescript
onSuccess: async (result) => {
  setSubmitResult(result);
  setSubmitError("");
  setShouldFailNextSubmit(false);
  await refreshPortalData();
},
onError: (error: Error) => {
  setSubmitError(error.message);
  setSubmitResult(null);
  setShouldFailNextSubmit(false);
},
```

실제로 React 19에서는 자동 배치가 되므로 순서가 크게 상관없지만, 명시적으로 양쪽을 모두 정리하는 것이 의도를 드러낸다.

## invite 추가 후 목록에 즉시 반영되지 않음

### 증상

invite를 추가하는 mutation이 성공했는데, pending invites 목록에 새 invite가 보이지 않았다.

### 원인

addInviteMutation의 onSuccess에서 `inviteForm.reset()`만 호출하고 `refreshPortalData()`를 빠뜨렸다. React Query 캐시가 갱신되지 않았으므로 `invitesQuery.data`는 이전 값을 유지했다.

### 해결

onSuccess에서 폼 리셋 후 반드시 `refreshPortalData()`를 호출한다. 이 함수가 invites 쿼리를 포함한 모든 관련 쿼리를 invalidate하므로, 목록이 다시 fetch되어 새 invite가 표시된다.

## router.push로 step 전환 시 히스토리가 과도하게 쌓임

### 증상

workspace → invites → review → invites → workspace 순서로 step을 전환했더니, 뒤로가기를 5번 눌러야 sign-in 화면으로 돌아갔다.

### 원인

`router.push`로 step을 전환하면 매번 새 히스토리 엔트리가 생긴다.

### 해결

`router.replace`로 변경:

```typescript
onStepChange={(nextStep) => {
  router.replace(`/onboarding?step=${nextStep}`);
}}
```

step 전환은 같은 페이지 내의 탭 이동과 같으므로, 히스토리에 쌓이지 않는 것이 자연스럽다.
