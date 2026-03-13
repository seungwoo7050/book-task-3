# 02 Render Pipeline development timeline

`02-render-pipeline`는 VDOM foundation 위에 "무엇이 바뀌었는지"와 "언제 바꿀지"를 분리해 올리는 단계다. `study/react-internals/02-render-pipeline`의 README, `diff.ts`, `patch.ts`, `scheduler.ts`, tests, 그리고 2026-03-13 재검증 결과를 따라가면 이 프로젝트가 왜 render phase와 commit phase를 갈라야 했는지 선명해진다.

## 구현 순서 요약

1. README와 problem 문서로 diff, patch, scheduler, `flushSync`까지가 이 단계의 public contract라는 점을 먼저 고정했다.
2. `diff.ts`에서 patch calculation 범위를, `scheduler.ts`에서 render/commit split과 interrupted work handling을 읽었다.
3. 마지막에는 `npm run verify --workspace @front-react/render-pipeline`로 diff/patch/scheduler tests와 typecheck를 다시 통과시켰다.

## 2026-03-08 / Phase 1 - pipeline 범위를 먼저 고정한다

- 당시 목표:
  이 단계가 "조금 더 나은 render"가 아니라 phase separation 문제라는 점을 먼저 선언한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `problem/original/README.md`, `ts/README.md`
- 처음 가설:
  foundation 위에 patch 함수 몇 개가 추가되는 정도라고 보기 쉬웠지만, README는 render/commit split과 cooperative work loop까지 포함하고 있었다.
- 실제 진행:
  adapted/original problem 문서와 README를 읽으며 diff/patch/scheduler 세 층을 먼저 나눴다.

CLI:

```bash
$ git log --reverse --stat -- study/react-internals/02-render-pipeline | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... ts/src/diff.ts
... ts/src/patch.ts
... ts/src/scheduler.ts
... ts/tests/scheduler.test.ts
```

검증 신호:

- source tree 자체가 pipeline을 세 파일로 분리하고 있어서, "무엇을 계산할까"와 "언제 commit할까"를 별개 개념으로 다뤄야 한다는 점이 보였다.

핵심 코드:

```ts
function diffChildrenByKey(oldChildren: VNode[], newChildren: VNode[]): Patch[] {
  const oldMap = new Map<string, { node: VNode; index: number }>();
  const patches: Patch[] = [];
  const visitedKeys = new Set<string>();
```

왜 이 코드가 중요했는가:

render pipeline의 첫 전환점은 keyed child를 따로 다뤄야 한다는 결정이다. child diff를 단순 index 비교로만 밀어붙이면 reorder와 remove/create가 뒤엉켜 버린다. `oldMap`과 `visitedKeys`는 그 혼선을 끊기 위한 최소 장치다.

새로 배운 것:

- reconciliation은 DOM을 곧바로 만지는 문제가 아니라 patch를 계산하는 데이터 변환 문제로 먼저 보는 편이 명확하다.

다음:

- 계산된 patch가 언제 DOM에 반영되는지 scheduler 쪽으로 내려간다.

## 2026-03-08 / Phase 2 - render phase와 commit phase를 분리한다

- 당시 목표:
  interrupted work를 설명할 수 있는 최소 scheduler를 읽는다.
- 변경 단위:
  `ts/src/patch.ts`, `ts/src/scheduler.ts`, `ts/tests/scheduler.test.ts`
- 처음 가설:
  patch application만 있으면 될 것 같지만, commit 시점이 섞여 있으면 cooperative work loop를 설명할 수 없다고 봤다.
- 실제 진행:
  `rg -n`으로 `commitRoot`, `workLoop`, `flushSync` 위치를 먼저 잡고, `workLoop`가 unit of work를 수행하다가 마지막에만 `commitRoot`를 호출한다는 점을 중심으로 읽었다.

CLI:

```bash
$ rg -n 'commitRoot|workLoop|flushSync' \
  study/react-internals/02-render-pipeline/ts/src/scheduler.ts
study/.../scheduler.ts:55:function commitRoot()
study/.../scheduler.ts:79:export function workLoop(deadline: IdleDeadlineLike)
study/.../scheduler.ts:94:export function flushSync()
```

검증 신호:

- scheduler symbol 세 개만 봐도 이 프로젝트가 "patch 함수 모음"이 아니라 phase-aware runtime이라는 점이 분명해졌다.

핵심 코드:

```ts
export function workLoop(deadline: IdleDeadlineLike): void {
  let shouldYield = false;
  while (nextUnitOfWork && !shouldYield) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork, (fiber) => {
      deletions.push(fiber);
    });
    shouldYield = deadline.timeRemaining() < 1;
  }
  if (!nextUnitOfWork && wipRoot) {
    commitRoot();
  }
}
```

왜 이 코드가 중요했는가:

이 블록이 pipeline이라는 이름을 실체로 만든다. render phase에서는 unit of work만 진행하고, 모든 계산이 끝난 뒤에만 `commitRoot`를 호출하니 DOM mutation 시점을 통제할 수 있다. interrupted work를 설명하려면 바로 이 분리가 필요하다.

새로 배운 것:

- scheduler의 핵심은 똑똑한 우선순위가 아니라, DOM mutation 시점을 render 계산과 떼어 놓는 데 있다.

다음:

- verify가 diff/patch/scheduler를 각각 어떻게 확인하는지 본다.

## 2026-03-13 / Phase 3 - verify로 pipeline contract를 닫는다

- 당시 목표:
  diff/patch/scheduler correctness를 현재 시점에 다시 고정한다.
- 변경 단위:
  `ts/tests/diff.test.ts`, `ts/tests/patch.test.ts`, `ts/tests/scheduler.test.ts`, `tsconfig.json`
- 처음 가설:
  성능 수치 같은 건 없더라도, patch ordering과 interrupted work correctness만 명확하면 이 단계는 충분히 닫힌다고 봤다.
- 실제 진행:
  canonical verify를 다시 실행해 `8 passed`와 `tsc --noEmit` 통과를 확보했다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/render-pipeline
✓ ts/tests/diff.test.ts (4 tests)
✓ ts/tests/patch.test.ts (1 test)
✓ ts/tests/scheduler.test.ts (3 tests)
Test Files  3 passed (3)
Tests  8 passed (8)
> tsc --noEmit
```

검증 신호:

- diff, patch, scheduler가 별도 test file로 분리돼 있어 pipeline 설명과 test 구조가 일치했다.
- typecheck 통과가 `@front-react/render-pipeline` 패키지의 import surface를 다시 보증했다.

핵심 코드:

```ts
function commitRoot(): void {
  deletions.forEach((fiber) => commitWork(fiber));
  deletions = [];
  commitWork(wipRoot?.child ?? null);
  currentRoot = wipRoot;
  wipRoot = null;
}
```

왜 이 코드가 중요했는가:

`commitRoot`는 계산이 끝난 뒤에만 DOM mutation이 일어난다는 사실을 가장 짧게 보여 준다. delete/create/update가 모두 여기로 모이기 때문에, phase separation이 말뿐이 아니라 실제 code path라는 점이 분명해진다.

새로 배운 것:

- render pipeline을 설명할 때 중요한 건 "얼마나 빨랐는가"보다 "어느 시점에 DOM을 만지기로 했는가"다.

다음:

- 함수 컴포넌트 state와 effect, delegated event는 다음 단계 `03-hooks-and-events`에서 같은 runtime으로 합쳐진다.

## 남은 경계

- function component state와 effect는 아직 없다.
- event delegation도 아직 없다.
- React의 priority/lanes 모델 전체는 다루지 않는다.
