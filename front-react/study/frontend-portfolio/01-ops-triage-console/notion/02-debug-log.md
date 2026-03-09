# 디버그 기록 — Ops Triage Console에서 마주친 문제들

## optimistic update 후 캐시 불일치

### 증상

이슈의 status를 변경한 직후 queue 목록에서는 갱신되었지만, 같은 이슈의 detail dialog에서는 이전 상태가 보였다.

### 원인

onMutate에서 issue list 캐시만 교체하고, detail 캐시는 건드리지 않았다. React Query는 queryKey 별로 캐시가 독립적이므로, `["issues", query]`와 `["issue", issueId]`는 서로 다른 캐시다.

### 해결

onMutate에서 두 캐시를 모두 교체한다:

```typescript
// list 캐시 교체
const issueLists = queryClient.getQueriesData({ queryKey: issueKeys.lists() });
for (const [key, listResult] of issueLists) {
  queryClient.setQueryData(key, {
    ...listResult,
    items: listResult.items.map(issue =>
      issue.id === issueId ? applyIssuePatch(issue, patch) : issue
    ),
  });
}

// detail 캐시 교체
if (detailSnapshot) {
  queryClient.setQueryData(issueKeys.detail(issueId), applyIssuePatch(detailSnapshot, patch));
}
```

onError에서도 두 캐시를 모두 복원한다.

## rollback 후 summary가 갱신되지 않음

### 증상

mutation 실패 → rollback 후 queue 목록은 이전 상태로 돌아갔지만, dashboard summary(health, priority counts 등)는 변경된 상태를 보여 주고 있었다.

### 원인

list/detail 캐시는 onMutate에서 snapshot을 저장하고 onError에서 복원했지만, summary 캐시는 별도 query key(`["dashboard-summary"]`)이므로 rollback 대상에 포함되지 않았다.

### 해결

onError에서 list/detail 복원 후 `invalidateOpsQueries(queryClient)`를 호출해 summary를 포함한 모든 관련 캐시를 강제 refetch한다. onSuccess에서도 같은 함수를 호출해 서버 상태와 동기화한다.

```typescript
async function invalidateOpsQueries(queryClient) {
  await Promise.all([
    queryClient.invalidateQueries({ queryKey: issueKeys.lists() }),
    queryClient.invalidateQueries({ queryKey: ["issue"] }),
    queryClient.invalidateQueries({ queryKey: issueKeys.summary() }),
  ]);
}
```

## Undo 후 activity가 남아 있음

### 증상

이슈를 수정하고 Undo를 누르면 status, priority 등은 복원됐지만, activity 타임라인에 변경 기록이 남아 있었다.

### 원인

Undo가 `applyIssuePatch(current, originalPatch)`를 다시 적용하는 방식이었다. 이 경우 "원래 값으로 변경"이라는 새 activity가 추가된다.

### 해결

Undo를 `restoreIssuesSnapshot([result.previousIssue])`로 변경했다. mutation 성공 시 반환되는 `previousIssue`(변경 전 전체 스냅샷)를 storage에 직접 쓰면, activity를 포함한 전체 상태가 복원된다.

## bulk action에서 row selection이 안 풀림

### 증상

다수 row를 선택하고 bulk update를 실행한 후, 성공 toast가 뜨지만 checkbox가 여전히 선택 상태로 남았다.

### 원인

useBulkIssueMutation의 onSuccess에서 rowSelection을 초기화하는 콜백이 누락되었다.

### 해결

useBulkIssueMutation에 `onClearSelection` 콜백을 전달하고, onSuccess에서 호출한다:

```typescript
const bulkMutation = useBulkIssueMutation(selectedIssueId, setToast, () => {
  setRowSelection({});
  setBulkDraft({});
});
```

## saved view 전환 시 이전 page 번호가 유지됨

### 증상

page 2를 보고 있는 상태에서 saved view를 누르면, 새 필터가 적용되지만 page: 2가 유지되어 결과가 비어 보였다.

### 원인

`mergeSavedView`에서 page를 리셋하지 않았다. saved view의 query를 merge할 때 현재 query의 page가 그대로 유지됐다.

### 해결

```typescript
export function mergeSavedView(query: IssueQuery, view: SavedView): IssueQuery {
  return {
    ...defaultIssueQuery,
    ...query,
    ...view.query,
    page: 1,  // 항상 첫 페이지로 리셋
  };
}
```

## SSR에서 localStorage 접근 에러

### 증상

Next.js SSR 시 `window is not defined` 에러가 발생했다.

### 원인

storage.ts의 read/write 함수가 `window.localStorage`에 직접 접근하고 있었다. SSR에서는 window가 없다.

### 해결

`canUseStorage()` 가드를 추가:

```typescript
function canUseStorage(): boolean {
  return typeof window !== "undefined" && !!window.localStorage;
}
```

SSR에서는 메모리 캐시(모듈 레벨 변수)만 사용하고, 클라이언트에서는 localStorage와 동기화한다.

## useDeferredValue로 인한 검색 결과 깜빡임

### 증상

검색어를 빠르게 타이핑하면, queue가 이전 검색 결과와 새 검색 결과 사이를 오가며 깜빡였다.

### 원인

query.search를 직접 React Query의 queryKey에 넣으면, 타이핑할 때마다 새 쿼리가 실행된다. useDeferredValue는 렌더를 지연시키지만, queryKey가 바뀌면 React Query가 즉시 refetch한다.

### 해결

`deferredSearch = useDeferredValue(query.search)`를 만들고, `effectiveQuery = { ...query, search: deferredSearch }`를 React Query에 전달한다. React가 deferredSearch를 업데이트하는 타이밍에만 새 쿼리가 실행되므로, 중간 상태의 불필요한 요청이 줄어든다.

## Zod 검증 에러 메시지가 사용자에게 노출됨

### 증상

잘못된 형식의 patch를 보내면 Zod 에러가 raw 메시지로 콘솔에 표시됐다.

### 원인

service.ts에서 Zod validation 에러를 catch하지 않고 그대로 mutation의 onError로 전달했다.

### 해결

service.ts에서 `issuePatchSchema.parse(patch)`를 호출하되, 이 에러는 개발자 실수(잘못된 코드)이므로 일반 에러와 구분 없이 "Update failed" 메시지로 표시한다. Zod의 에러 메시지(`Keep notes short enough to scan from the timeline.`)는 noteSchema에 설정한 커스텀 메시지로 제어한다.
