# Making Optimistic Actions Reversible

운영 도구에서 빠른 UI는 분명 중요하다. 하지만 빠르기만 한 UI는 금방 신뢰를 잃는다. 방금 바꾼 상태가 실패하면 어떻게 되는지, 목록과 상세가 서로 다른 값을 보여 주지는 않는지, 한 번의 bulk action을 잘못 눌렀을 때 되돌릴 수 있는지까지 같이 설명되어야 한다. Ops Triage Console의 진짜 중심은 바로 여기 있었다.

이 프로젝트가 흥미로운 이유는 optimistic update를 "빨리 보이게 만드는 트릭"으로 다루지 않는다는 점이다. 오히려 snapshot을 얼마나 넓게 잡고, 실패했을 때 어떤 surface로 복구를 보여 줄 것인가에 훨씬 더 무게를 둔다.

그래서 이 글은 internal tool의 두 번째 핵심 축, 즉 reversible mutation이 어떻게 만들어졌는지를 따라간다.

## 구현 순서를 먼저 짚으면

- single issue mutation부터 list/detail snapshot을 함께 잡는 방식으로 만들었다.
- 그 규칙을 bulk mutation에도 확장해 selected rows 전체를 같은 방식으로 되돌릴 수 있게 했다.
- integration 테스트로 summary, queue, detail이 같이 움직이는지 확인했다.

## 낙관적 업데이트의 핵심은 빠른 반응이 아니라 snapshot 범위였다

`useIssueMutation()`의 `onMutate`를 보면 이 프로젝트가 어디에 신경을 썼는지 분명히 드러난다. 목록 query만 고치는 것이 아니라, 현재 열려 있는 detail query snapshot도 같이 잡는다.

```ts
onMutate: async ({ issueId, patch }) => {
  setPendingIds([issueId]);

  const issueLists = queryClient.getQueriesData<IssueListResult>({
    queryKey: issueKeys.lists(),
  });
  const detailSnapshot = queryClient.getQueryData<Issue | undefined>(
    issueKeys.detail(issueId),
  );

  for (const [key, listResult] of issueLists) {
    queryClient.setQueryData<IssueListResult>(key, {
      ...listResult,
      items: listResult.items.map((issue) =>
        issue.id === issueId ? applyIssuePatch(issue, patch) : issue,
      ),
    });
  }
  return { issueLists, detailSnapshot };
}
```

이 코드는 낙관적 업데이트를 단순히 "먼저 바꿔 보여 준다"로 두지 않는다. 나중에 실패하거나 Undo 할 때 정확히 어디로 돌아가야 하는지를 같이 저장해 둔다. internal tool에서 이 차이는 치명적이다. 목록은 바뀌었는데 상세는 안 바뀌거나, 반대로 상세만 복구되고 queue는 그대로 남아 있으면 operator는 시스템을 신뢰할 수 없게 된다.

## bulk action도 같은 철학으로 설계돼야 했다

이 원칙은 bulk mutation에서도 그대로 반복된다. 오히려 bulk action이기 때문에 더 엄격해야 했다. 여러 row를 한 번에 바꾸는 순간, 실패와 복구도 같은 범위로 다뤄져야 하기 때문이다.

```ts
onMutate: async ({ issueIds, patch }) => {
  setPendingIds(issueIds);

  const issueLists = queryClient.getQueriesData<IssueListResult>({
    queryKey: issueKeys.lists(),
  });

  for (const [key, listResult] of issueLists) {
    queryClient.setQueryData<IssueListResult>(key, {
      ...listResult,
      items: applyBulkPatch(listResult.items, issueIds, patch),
    });
  }
  return { issueLists, detailSnapshot };
}
```

그리고 실패했을 때는 그대로 rollback surface를 드러낸다. 사용자는 "실패했다"는 사실만 듣는 것이 아니라, 선택한 rows가 되돌려졌고 다시 시도할 수 있다는 메시지를 바로 받는다.

```ts
setToast({
  tone: "error",
  title: "Bulk update failed",
  description: "The selected rows were rolled back. Retry the bulk action.",
  actionLabel: "Retry",
  onAction: async () => {
    mutation.mutate(variables);
  },
});
```

여기서 새로 분명해진 건 optimistic UI의 품질이 success toast보다 rollback surface에서 드러난다는 점이었다. 빠른 화면은 매력적이지만, 실패했을 때 무슨 일이 벌어졌는지 설명하지 못하면 internal tool로서는 절반짜리다.

## 이 단계의 verify는 data consistency를 계속 물고 늘어진다

이 프로젝트의 테스트가 단순히 "변경 버튼이 잘 눌린다"를 확인하지 않는 이유도 여기에 있다. integration harness는 query가 바뀌면 visible row set이 바뀌는지, single mutation 뒤에 list와 detail이 같이 맞춰지는지, bulk mutation 뒤에 summary count까지 따라오는지를 본다.

```bash
cd study
npm run test --workspace @front-react/ops-triage-console
```

2026-03-13 replay 기준으로 `vitest` 16개 테스트가 통과했다. 이 중 상당수는 optimistic helper와 simulation helper만이 아니라, query cache와 detail snapshot이 같은 방향으로 움직이는지 확인한다.

즉 이 글의 주제는 React Query 사용법이 아니다. 여러 surface가 동시에 존재하는 internal tool에서, mutation 하나가 어디까지 일관되어야 하는가를 정의하는 일에 더 가깝다.

다음 글에서는 이 reversible mutation이 실제 failure와 e2e 시나리오를 만나면 어떻게 읽히는지 본다. 결국 포트폴리오 결과물로서 결정적인 건 실패했을 때도 이 도구가 믿을 만하다는 사실을 보여 주는 쪽이기 때문이다.
