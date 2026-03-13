# 01 Ops Triage Console development timeline

`01-ops-triage-console`는 `frontend-portfolio` 트랙에서 가장 넓은 화면을 가진 프로젝트지만, source-first로 다시 읽으면 중심은 surprisingly 명확하다. `study/frontend-portfolio/01-ops-triage-console`의 README, query/mutation hooks, main console component, tests, 그리고 2026-03-13 재검증 결과를 나란히 두면 이 앱의 핵심은 "operator가 queue를 끝까지 triage할 수 있는가"라는 질문에 있다.

## 구현 순서 요약

1. README와 problem 문서로 dashboard, dense queue, bulk action, retry/undo가 public contract라는 점을 먼저 고정했다.
2. `useIssueMutation`에서 optimistic cache patch와 rollback/undo 경로를 읽고, `OpsTriageConsole`에서 deferred search와 table selection이 그 contract를 어떻게 소비하는지 확인했다.
3. 마지막에는 `npm run verify --workspace @front-react/ops-triage-console`로 typecheck, vitest, Playwright를 모두 다시 통과시켰다.

## 2026-03-08 / Phase 1 - 운영 콘솔의 workflow contract를 먼저 고정한다

- 당시 목표:
  컴포넌트 개수보다 operator workflow를 먼저 붙잡는다.
- 변경 단위:
  `README.md`, `problem/README.md`, `next/README.md`, `package.json`
- 처음 가설:
  대규모 UI라서 component tree를 먼저 파고들기 쉽지만, README를 보면 이 프로젝트의 본론은 dashboard -> queue -> detail -> retry/undo라는 triage flow였다.
- 실제 진행:
  README와 problem 문서를 읽어 포함 범위와 검증 surface를 먼저 고정했고, `git log --reverse --stat`로 app, hooks, tests, docs가 한 묶음으로 landing된 사실을 확인했다.

CLI:

```bash
$ git log --reverse --stat -- study/frontend-portfolio/01-ops-triage-console | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... next/src/hooks/use-ops-triage.ts
... next/src/components/console/ops-triage-console.tsx
... next/tests/integration/ops-triage-console.test.tsx
... next/tests/e2e/ops-triage.spec.ts
```

검증 신호:

- source tree가 app, hook, unit/integration/E2E를 모두 같은 경계에 담고 있어 포트폴리오 앱답게 검증 surface가 넓었다.

핵심 코드:

```ts
const mutation = useMutation({
  mutationFn: ({ issueId, patch }) => updateIssue(issueId, patch),
  onMutate: async ({ issueId, patch }) => {
    const issueLists = queryClient.getQueriesData<IssueListResult>({ queryKey: issueKeys.lists() });
```

왜 이 코드가 중요했는가:

운영 콘솔에서 가장 먼저 봐야 할 건 form field가 아니라 mutation contract다. `onMutate`에서 query snapshots를 먼저 잡는다는 사실만으로도, 이 앱이 optimistic UI를 데모 수준이 아니라 rollback까지 포함한 workflow로 보겠다는 의도를 드러낸다.

새로 배운 것:

- internal tool에서 optimistic update의 진짜 품질은 "빨라졌다"가 아니라 실패했을 때 operator를 어디까지 되돌려 줄 수 있는가에 있다.

다음:

- main console surface가 이 mutation contract를 어떻게 소비하는지 본다.

## 2026-03-08 / Phase 2 - optimistic mutation을 dense queue workflow에 붙인다

- 당시 목표:
  update/undo contract가 실제 operator flow로 이어지는 지점을 찾는다.
- 변경 단위:
  `next/src/hooks/use-ops-triage.ts`, `next/src/components/console/ops-triage-console.tsx`
- 처음 가설:
  detail dialog만 잘 만들면 될 것 같지만, triage는 list/detail/saved view/bulk action이 동시에 일관돼야 한다고 봤다.
- 실제 진행:
  `rg -n`으로 `useIssueMutation`, `useBulkIssueMutation`, `OpsTriageConsole`, `useDeferredValue` 위치를 다시 확인하고, deferred search와 selection table이 query hooks를 어떻게 묶는지 좁혔다.

CLI:

```bash
$ rg -n 'useIssueMutation|useBulkIssueMutation|OpsTriageConsole|useDeferredValue|useIssueList' \
  study/frontend-portfolio/01-ops-triage-console/next/src/hooks/use-ops-triage.ts \
  study/frontend-portfolio/01-ops-triage-console/next/src/components/console/ops-triage-console.tsx
use-ops-triage.ts:105:export function useIssueMutation(
use-ops-triage.ts:198:export function useBulkIssueMutation(
ops-triage-console.tsx:120:export function OpsTriageConsole()
ops-triage-console.tsx:129:  const deferredSearch = useDeferredValue(query.search);
ops-triage-console.tsx:137:  const issueListQuery = useIssueList(effectiveQuery);
```

검증 신호:

- main console component가 `useDeferredValue`, query hooks, mutations를 한 화면 흐름으로 묶고 있어, 성능 미세조정보다 operator continuity가 우선이라는 점이 분명했다.

핵심 코드:

```tsx
const deferredSearch = useDeferredValue(query.search);
const effectiveQuery = {
  ...query,
  search: deferredSearch,
};

const issueListQuery = useIssueList(effectiveQuery);
const detailQuery = useIssueDetail(selectedIssueId);
```

왜 이 코드가 중요했는가:

운영 콘솔에서 검색어를 칠 때마다 전체 queue가 흔들리면 operator 흐름이 망가진다. `useDeferredValue`로 immediate input과 effective query를 나누는 순간, 이 앱은 UI 반응성과 data-heavy filtering을 동시에 챙기는 방향으로 기운다.

새로 배운 것:

- 제품형 UI에서는 "빠르다"보다 "작업 흐름을 끊지 않는다"가 더 직접적인 품질 기준이 된다.

다음:

- verify가 undo, bulk update, retry, keyboard triage를 실제로 닫는지 본다.

## 2026-03-13 / Phase 3 - verify로 operator workflow를 닫는다

- 당시 목표:
  product contract를 현재 시점의 CLI 결과로 다시 고정한다.
- 변경 단위:
  `next/tests/unit/*`, `next/tests/integration/*`, `next/tests/e2e/*`, `next/tsconfig.json`
- 처음 가설:
  E2E 몇 개만 통과해도 충분해 보일 수 있지만, 이 프로젝트는 typecheck/unit/integration/E2E가 모두 있어야 portfolio signal이 설득력 있다고 봤다.
- 실제 진행:
  canonical verify를 다시 실행해 typecheck, `16`개 vitest, `4`개 E2E 시나리오를 모두 확보했다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/ops-triage-console
> tsc --noEmit -p next/tsconfig.json
Test Files  4 passed (4)
Tests  16 passed (16)
Running 4 tests using 1 worker
✓ updates an issue from detail and can undo the change
✓ applies a saved-view bulk update and clears the queue
✓ surfaces a simulated write error and retries successfully
✓ supports a keyboard-only triage path
4 passed (28.0s)
```

검증 신호:

- E2E 제목 네 개가 이 프로젝트의 public contract를 거의 그대로 요약한다.
- typecheck와 unit/integration tests가 있어서 UI 데모가 아니라 maintainable Next app으로서의 증거도 남는다.

핵심 코드:

```ts
onError: (error, variables, context) => {
  context?.issueLists.forEach(([key, value]) => {
    queryClient.setQueryData(key as QueryKey, value);
  });
  setToast({
    tone: "error",
    title: "Update failed",
    actionLabel: "Retry",
  });
}
```

왜 이 코드가 중요했는가:

이 블록이 있어야 optimistic update가 "잠깐 빨라 보이는 착시"가 아니라 실패 복구까지 포함한 workflow가 된다. query snapshots를 되돌리고 retry toast를 띄우는 순간, operator는 오류를 만난 뒤에도 흐름을 잃지 않는다.

새로 배운 것:

- portfolio-grade internal tool에서는 success path만큼 failure recovery path가 중요하다. 실제 현업에서 triage는 실패를 포함한 반복 작업이기 때문이다.

다음:

- 실제 auth, DB, multi-user collaboration은 아직 없다. 고객-facing flow는 다음 프로젝트 `02-client-onboarding-portal`이 이어받는다.

## 남은 경계

- 실제 인증과 실제 DB는 없다.
- multi-user real-time collaboration도 다루지 않는다.
- mock service와 local persistence 기준의 데모라는 점은 그대로 남는다.
