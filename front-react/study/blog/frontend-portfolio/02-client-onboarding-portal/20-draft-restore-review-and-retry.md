# Draft Restore, Review, And Retry

session gate를 세운 뒤에 남는 더 어려운 질문은 이것이다. 사용자가 workspace profile을 채우다가 떠났을 때, 다시 돌아오면 어디서부터 이어지나. 그리고 마지막 submit이 실패했을 때, 이 onboarding은 신뢰를 잃지 않고 다시 시도할 surface를 남기고 있나. `Client Onboarding Portal`의 진짜 품질은 step 개수보다 이 두 질문에 대한 답에서 드러난다.

소스를 따라가 보니 이 프로젝트는 continuity를 세 층으로 풀었다. profile 저장과 checklist 진행을 같은 mutation에 묶는다. storage는 session/profile/invites/checklist/meta를 분리해서 저장한다. submit 단계는 성공만 보여 주지 않고, 일부러 한 번 실패시키는 토글과 retryable error path를 제품 surface에 올린다. 덕분에 "저장된다"와 "다시 시도할 수 있다"가 단순 helper 수준에 머물지 않는다.

## draft save는 persistence가 아니라 onboarding progression 이벤트다

workspace step의 저장 버튼은 값을 쓰는 것에서 끝나지 않는다.

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

여기에는 세 가지 의도가 같이 들어 있다.

1. `workspaceProfileSchema`를 통과한 값만 저장한다.
2. 저장 성공이 곧 checklist의 `profile` 완료로 이어진다.
3. 저장 메시지와 query invalidation으로 사용자는 "지금 저장되었고, 같은 세계를 다시 보고 있다"는 피드백을 받는다.

즉 save draft는 단순 autosave 대체물이 아니라 onboarding 진행 이벤트다. 문제 정의가 draft restore를 검증 가능한 시나리오로 요구했기 때문에, 저장 시점이 언제인지 사용자가 이해할 수 있어야 했다.

## 복원은 하나의 blob이 아니라 상태 책임을 잘게 나눠서 만든다

`storage.ts`는 저장소를 일부러 분리한다.

```ts
const STORAGE_KEYS = {
  session: "front-react:onboarding:session",
  profile: "front-react:onboarding:profile",
  invites: "front-react:onboarding:invites",
  checklist: "front-react:onboarding:checklist",
  meta: "front-react:onboarding:meta",
};
```

이 분리가 중요한 이유는 continuity 문제를 한 덩어리로 묶지 않기 때문이다.

- `session`: route guard를 열고 닫는 인증 문맥
- `profile`: workspace draft 복원 대상
- `invites`: review summary와 submit readiness에 영향을 주는 목록
- `checklist`: step progression이 아니라 완료 증거
- `meta`: `failNextSubmit`, `submittedAt` 같은 제어/기록 정보

이 구조 덕분에 reload 뒤 `profileQuery.data`가 들어오면 form은 `workspaceForm.reset(profileQuery.data)`로 값만 복원하고, submit failure 제어는 별도의 meta 경로에 남는다. draft와 retry가 서로 간섭하지 않는다.

테스트도 그 지점을 그대로 밟는다. Playwright는 invalid compliance email로 한 번 막히는지 본 뒤, 올바른 값으로 저장하고, 새로고침 후 `Workspace name` 필드가 그대로 복원되는지 확인한다. integration test도 sign-in 이후 workspace 저장, invite 추가, review submit retry를 한 흐름으로 고정한다. 즉 이 앱은 단순히 localStorage를 쓴다는 사실보다 "복원이 onboarding continuity를 정말 살리는가"를 검증하고 있다.

다만 이 continuity는 single-browser, single-tab 범위에 머문다. `storage.ts`는 브라우저 한 곳의 `localStorage`를 읽고 쓸 뿐이고, background autosave나 cross-tab merge는 없다. 이번 보강에서는 그래서 "draft restore"를 server-backed durability처럼 포장하지 않았다.

## 마지막 review는 성공 버튼이 아니라 failure surface까지 포함해야 완성된다

review step은 가장 솔직한 부분이다. summary 카드 두 개와 checklist, 그리고 "다음 submit 실패를 시뮬레이션"하는 토글이 한 화면에 있다.

```tsx
<input
  type="checkbox"
  checked={shouldFailNextSubmit}
  onChange={(event) => setShouldFailNextSubmit(event.target.checked)}
/>
...
<button
  type="button"
  onClick={() => submitMutation.mutate()}
  disabled={!canSubmit || submitMutation.isPending}
>
  Submit onboarding
</button>
```

submit는 `canSubmitOnboarding()`을 통과해야만 활성화된다. 여기서 step 이동과 제출 가능 여부가 분리된다. review 화면까지는 미완성 상태로도 들어올 수 있지만, 실제 제출은 profile completeness, invite 존재, checklist 3개 완료가 모두 있어야 가능하다. 이게 이 프로젝트가 택한 "loose navigation, strict submission gate"다.

서비스 계층은 retry를 더 명확하게 드러낸다.

```ts
if (meta.failNextSubmit) {
  setFailNextSubmit(false);
  throw createRetryableError(
    "Submission failed. Retry after checking the review summary.",
  );
}
```

실패는 숨겨진 test helper가 아니라 공개된 데모 기능이다. 한 번 실패하면 `failNextSubmit` 플래그는 바로 꺼지고, 사용자는 같은 화면에서 다시 제출할 수 있다. 즉 retry는 실패 후 새 route로 보내는 복구가 아니라, 같은 review surface 안에서 신뢰를 회복하는 방식이다.

## 2026-03-14 검증으로 다시 고정한 사실

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study
npm run verify --workspace @front-react/client-onboarding-portal
```

이번 재실행 결과는 다음과 같았다.

- `typecheck`: 통과
- `vitest`: unit 3개 파일 + integration 1개 파일, 총 7개 테스트 통과
- `playwright`: 2개 시나리오 통과

특히 E2E는 아래 흐름을 실제 브라우저에서 다시 확인했다.

- `/`에서 sign-in 후 `/onboarding?step=workspace` 진입
- invalid compliance email에서 validation 에러 노출
- 유효한 값 저장 후 success message 노출
- 새로고침 뒤 draft restore 확인
- invite 추가 후 review 이동
- `Simulate the next submit failure` 체크 후 첫 submit 실패
- 두 번째 submit 성공

## 지금 남는 한계는 무엇인가

이 앱은 실제 backend나 multi-user 협업을 다루지 않는다. invite도 메일 발송이나 acceptance lifecycle 없이 pending row로만 남는다. 또 draft 저장은 명시적 save 버튼 중심이라 background autosave나 conflict handling은 아직 없다. submit retry 역시 같은 browser state 안에서의 재시도 surface이지, 서버 큐 재처리나 네트워크 복구를 시뮬레이션하는 것은 아니다. 하지만 현재 범위 안에서는 오히려 이 단순함이 장점이다. 사용자가 왜 저장되었고, 왜 막혔고, 왜 다시 시도할 수 있는지를 화면과 코드가 같은 언어로 설명하기 때문이다.

이 프로젝트를 high-quality onboarding 사례로 보이게 만드는 건 멋진 stepper가 아니다. 저장-복원-재시도가 실제 검증과 함께 한 흐름으로 묶여 있다는 점이다.
