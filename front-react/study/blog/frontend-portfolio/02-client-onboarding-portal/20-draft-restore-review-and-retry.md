# Draft Restore, Review, And Retry

고객-facing onboarding에서 사용자가 정말 원하는 것은 stepper가 예쁜가보다, 중간에 저장하고 나갔다가 돌아와도 흐름이 이어지는가에 더 가깝다. 특히 회사 정보와 invite를 채우는 과정은 한 번에 끝나지 않는 경우가 많다. 그래서 이 프로젝트의 진짜 중심은 form validation보다 continuity에 있었다.

코드를 따라가 보면 그 연속성은 세 가지 장치가 같이 만든다. draft save 메시지, local storage 기반 복원, 그리고 submit failure 뒤의 retry surface다. 어느 하나만 있어서는 부족하다. 저장만 되고 다시 못 불러오면 끊기고, 복원은 되지만 실패 뒤 경로가 없으면 마지막 순간에 신뢰가 무너진다.

흥미로운 건 이 흐름이 검증에서도 그대로 드러난다는 점이다. 2026-03-13 replay에서 첫 `verify`는 draft save 메시지를 5초 안에 찾지 못해 실패했고, 같은 날 다시 돌린 `e2e`와 `verify`는 통과했다. 기능은 맞지만 feedback timing이 민감하다는 사실이 테스트 로그를 통해 정직하게 드러난 셈이다.

## 구현 순서를 먼저 짚으면

- workspace profile 저장과 checklist 진행을 같은 mutation으로 묶었다.
- local storage와 mock service를 이용해 reload 뒤에도 draft를 되살렸다.
- review step에서는 의도적 실패와 retry를 노출해 마지막 제출 surface를 검증했다.

## draft save는 localStorage 쓰기보다 더 큰 이벤트였다

`saveProfileMutation`을 보면 저장은 단순히 값을 쓰는 동작이 아니다. profile을 저장한 뒤 checklist를 진행시키고, 성공 메시지를 보여 주고, 관련 query를 모두 invalidate해 같은 세계를 다시 읽어 온다.

```tsx
const saveProfileMutation = useMutation({
  mutationFn: async (values: WorkspaceProfileSchema) => {
    const nextProfile = await saveWorkspaceProfile(values);
    await completeChecklistItem("profile");
    return nextProfile;
  },
  onSuccess: async () => {
    setSaveMessage("Draft saved to the local demo workspace.");
    await refreshPortalData();
  },
});
```

이 코드가 중요한 이유는 draft save를 단순한 persistence helper가 아니라 onboarding 이벤트로 다루기 때문이다. 저장 메시지와 checklist 진행이 같이 움직여야 사용자는 "지금 정말 다음 단계로 갈 준비가 되었구나"를 느낄 수 있다.

storage 계층도 같은 철학으로 잘게 나뉘어 있다. session, profile, invites, checklist, meta를 따로 저장하기 때문에, 어떤 정보가 복원되고 어떤 정보가 실패 제어용 메타데이터인지 분명하다.

```ts
const STORAGE_KEYS = {
  session: "front-react:onboarding:session",
  profile: "front-react:onboarding:profile",
  invites: "front-react:onboarding:invites",
  checklist: "front-react:onboarding:checklist",
  meta: "front-react:onboarding:meta",
};
```

이 구조 덕분에 reload restore와 submit retry가 서로 섞이지 않는다. 둘 다 continuity 문제이긴 하지만, 저장 범위와 책임은 다르다.

## 마지막 제출은 성공보다 재시도 surface가 더 중요했다

review step은 일부러 "next submit failure" 토글을 노출한다. 즉 이 프로젝트는 실패를 숨기지 않는다. `submitOnboarding()`도 meta에 저장된 `failNextSubmit`을 읽어 retryable error를 던지고, 그 뒤에는 다시 정상 제출이 가능하도록 상태를 정리한다.

```ts
export async function submitOnboarding(): Promise<SubmitResult> {
  await wait(120);

  const profile = readWorkspaceProfile();
  const invites = readInvites();
  const checklist = readChecklist();
  const meta = readMeta();

  if (meta.failNextSubmit) {
    setFailNextSubmit(false);
    throw createRetryableError("Submission failed. Retry after checking the review summary.");
  }
```

이 선택이 좋았던 이유는 마지막 submit을 happy path만으로 남겨 두지 않았기 때문이다. onboarding의 품질은 "제출 성공" 순간보다 실패했을 때 사용자가 어디로 돌아가야 하는지를 설명하는 surface에서 더 잘 드러난다.

Playwright 시나리오도 정확히 그 지점을 밟는다. sign-in 이후 workspace profile을 채우고, invalid email을 먼저 넣어 validation을 확인하고, 올바른 email로 저장한 뒤, reload 이후에도 값이 남아 있는지 본다. 그다음 invite를 추가하고, review step에서 의도적으로 한 번 실패시킨 뒤 다시 제출한다.

```ts
await page.getByRole("button", { name: "Save draft" }).click();
await expect(page.getByText("Draft saved to the local demo workspace.")).toBeVisible();

await page.reload();
await expect(page.getByLabel("Workspace name")).toHaveValue("Lattice Cloud");
...
await page.getByRole("button", { name: "Submit onboarding" }).click();
await expect(page.getByText(/Submission failed/i)).toBeVisible();
await page.getByRole("button", { name: "Submit onboarding" }).click();
await expect(page.getByText(/Submitted Lattice Cloud at/i)).toBeVisible();
```

이 흐름은 단순히 기능 목록을 재생하는 것이 아니다. 저장, 복원, 실패, 재시도가 하나의 연속된 경험으로 이어지는지를 검증한다.

## verify replay가 알려 준 작은 불안정성도 그대로 남겨 둔다

이 프로젝트는 2026-03-13 verify replay에서 솔직한 신호를 남겼다.

```bash
cd study
npm run verify --workspace @front-react/client-onboarding-portal
npm run e2e --workspace @front-react/client-onboarding-portal
npm run verify --workspace @front-react/client-onboarding-portal
```

첫 번째 `verify`에서는 Playwright가 `Draft saved to the local demo workspace.` 텍스트를 5초 안에 찾지 못해 실패했다. 같은 날 `npm run e2e`를 다시 실행했을 때는 2개 시나리오가 통과했고, 이어서 `npm run verify`도 다시 통과했다. 이 기록은 지우지 않는 편이 좋다. 기능이 완전히 틀렸다는 뜻은 아니지만, feedback timing이 테스트를 흔들 만큼 민감하다는 뜻이기 때문이다.

즉 이 프로젝트는 "검증 통과"만 남기지 않고, 어떤 surface가 아직 timing-sensitive 한지도 함께 남긴다. 포트폴리오 문서로서는 오히려 이 편이 더 정직하고 읽을 가치가 있다.

## 무엇이 아직 남았는가

이 앱은 여전히 실제 auth backend, 실제 DB, 이메일 발송까지 다루지 않는다. 하지만 여기까지 읽고 나면 무엇을 더해야 하는지는 꽤 분명하다. 기능 추가보다 먼저 draft save feedback과 replay stability를 더 단단하게 만드는 쪽이 우선이다.

고객-facing flow의 신뢰는 결국 continuity에서 나온다. 저장해도 되고, 돌아와도 되고, 실패해도 다시 시도할 수 있어야 한다. 이 프로젝트는 그 연속성을 이미 잘 보여 주지만, 동시에 어디가 아직 민감한지도 숨기지 않고 남겨 두었다.
