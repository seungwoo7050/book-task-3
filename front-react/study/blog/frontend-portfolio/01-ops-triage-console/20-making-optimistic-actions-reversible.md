# Making Optimistic Actions Reversible

이 콘솔의 진짜 기술 포인트는 테이블이 아니라 mutation 경로다. 운영자는 queue에서 결정을 빨리 내려야 하므로, status/route/label 변화가 느리게 반영되면 도구 자체가 답답해진다. 하지만 optimistic update를 넣는 순간 rollback과 undo까지 같이 설계해야 한다. 이 프로젝트는 그 부분을 꽤 정직하게 드러낸다.

## optimistic patch는 activity log까지 같이 바꾼다

[`next/src/lib/optimistic.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console/next/src/lib/optimistic.ts)의 `applyIssuePatch()`는 단순 필드 overwrite가 아니라 activity entry까지 같이 쌓는다.

```ts
if (patch.status && patch.status !== issue.status) {
  nextIssue = pushActivity(
    { ...nextIssue, status: patch.status },
    `Status set to ${patch.status}.`,
    "status_changed",
  );
}
```

이 점이 중요한 이유는 optimistic UI가 "겉으로만 빨라 보이는 상태"가 아니라, detail panel과 activity timeline까지 함께 일관되게 보여 주려는 시도라는 뜻이기 때문이다. status, priority, label, route, operator note가 모두 같은 helper 위에서 바뀌므로, list와 detail이 다른 세계를 보지 않게 된다.

## rollback과 retry는 React Query cache 전체를 되돌리는 쪽으로 설계됐다

[`next/src/hooks/use-ops-triage.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console/next/src/hooks/use-ops-triage.ts)의 `useIssueMutation()`은 `onMutate`에서 list queries와 detail snapshot을 모두 저장한 뒤 optimistic patch를 넣는다.

에러가 나면 그 snapshot으로 다시 되돌린다.

```ts
context?.issueLists.forEach(([key, value]) => {
  queryClient.setQueryData(key as QueryKey, value);
});

if (context?.detailSnapshot) {
  queryClient.setQueryData(
    issueKeys.detail(variables.issueId),
    context.detailSnapshot,
  );
}
```

그리고 toast action으로 retry를 직접 붙인다. 성공했을 때는 반대로 undo action을 건다. 즉 이 콘솔의 optimistic update는 "빠르게 반영"에서 끝나지 않고, "실패하면 복구, 성공하면 되돌리기"까지 한 세트로 설계돼 있다.

bulk mutation도 같은 방식으로 list/detail snapshot을 저장하고, 성공 시 row selection과 bulk draft를 비운다. 내부도구형 UI에서 이 부분이 중요한 이유는, bulk action이 한번 꼬이면 운영자가 무엇이 실제로 적용됐는지 잃기 쉽기 때문이다.

## 실패 시뮬레이션이 제품 surface에 직접 연결돼 있다는 점이 좋다

[`next/src/lib/simulate.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console/next/src/lib/simulate.ts)는 `stable`/`chaos`, `failureRate`, `failNextRequest`를 제공한다. 이게 좋은 이유는 테스트용 helper가 UI 밖에만 머물지 않고, runtime controls를 통해 제품 surface와 직접 연결된다는 점이다.

즉 실패는 "개발자만 아는 설정"이 아니라, case study에서 보여 줄 수 있는 운영 시나리오가 된다. 사용자는 실패를 재현하고, toast에서 retry를 누르고, rollback이 실제로 눈앞에서 일어나는 것을 확인할 수 있다.

다만 이 runtime도 서버 플래그가 아니라 브라우저 쪽 state다. `readRuntimeConfig()`와 `writeRuntimeConfig()`는 `localStorage`와 in-memory clone을 함께 쓰므로, chaos/fail-next-request는 현재 탭/브라우저 데모 문맥에 묶인다. 이번 보강에서는 그래서 retry/rollback을 distributed backend recovery처럼 읽히지 않게 조정했다.

그래서 이 프로젝트의 두 번째 편에서 중요한 건 optimistic update 자체보다, 그 optimistic update를 되돌릴 수 있게 만들었다는 사실이다. 빠른 내부도구는 많지만, reversible optimistic workflow를 끝까지 설계한 내부도구는 훨씬 적다. 다만 그 rollback/undo도 single-operator, single-browser cache 문맥 안의 일관성을 보여 주는 수준이라는 점은 같이 기억해야 한다.
