# When Render Stops Being Commit

이 프로젝트를 다시 읽으면서 가장 중요하게 보였던 건 "다시 그린다"라는 말이 더 이상 하나의 단계가 아니라는 점이었다. 앞 단계에서는 `render()`가 VNode를 곧바로 DOM으로 append했다. 여기서는 그 말이 둘로 쪼개진다. 먼저 무엇이 바뀌었는지를 계산하는 render phase가 있고, 나중에야 DOM을 건드리는 commit phase가 있다.

## diff는 바뀐 것을 찾되, 아직 DOM을 만지지 않는다

첫 번째 고정점은 [`ts/src/diff.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline/ts/src/diff.ts)다. 여기서 중요한 건 patch 종류보다 계산 범위다.

- `diffProps`: `set` / `remove`
- `diffChildren`: keyed 또는 index-based child diff
- `diff`: `CREATE`, `REMOVE`, `REPLACE`, `UPDATE`

예를 들어 keyed child diff는 "같은 key면 비교, 없으면 create, 사라졌으면 remove"까지만 한다.

```ts
if (!oldMatch) {
  patches.push({
    type: "CREATE",
    newNode: child,
    index,
  });
  return;
}
...
if (typeof key === "string" && !visitedKeys.has(key)) {
  patches.push({
    type: "REMOVE",
    oldNode: child,
    index,
  });
}
```

중요한 건 여기서 reorder 자체를 표현하지 않는다는 점이다. 이 프로젝트의 diff는 최소 patch 범위를 만들지만, full keyed reconciliation engine처럼 이동 비용까지 계산하지는 않는다. 테스트도 딱 그 범위만 고정한다. keyed children에서 create/remove가 생기는지, index-based children에서는 위치별 UPDATE가 생기는지 정도만 본다.

unkeyed 쪽은 더 단순하다. `diffChildrenByIndex()`는 child identity를 추적하지 않고 같은 index끼리 바로 `diff()`를 건다. 그래서 앞에 새 child를 끼워 넣는 변화도 "뒤 child들을 move한다"가 아니라 "각 index의 old/new를 비교해서 UPDATE/CREATE를 만든다"는 식으로 해석된다. 즉 이 단계의 파이프라인은 render/commit 분리에는 성공했지만, React가 key 없이도 어느 정도 유지하려는 child identity semantics까지 재현하지는 않는다.

## render phase는 fiber를 만들고 effect를 붙이지만 DOM은 아직 비어 있다

render/commit 분리의 핵심은 [`ts/src/fiber.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline/ts/src/fiber.ts)와 [`ts/src/scheduler.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline/ts/src/scheduler.ts)에 있다.

`reconcileChildren()`는 old fiber와 새 element를 비교해서 각 fiber에 `effectTag`를 붙인다.

```ts
if (sameType && oldFiber) {
  nextFiber = {
    ...
    alternate: oldFiber,
    effectTag: "UPDATE",
  };
}

if (element && !sameType) {
  nextFiber = {
    ...
    effectTag: "PLACEMENT",
  };
}

if (oldFiber && !sameType) {
  oldFiber.effectTag = "DELETION";
  deletions.push(oldFiber);
}
```

즉 render phase의 역할은 "무엇을 할지 기록하는 것"이지 "지금 바로 DOM을 바꾸는 것"이 아니다. `scheduler.test.ts`의 첫 테스트가 컨테이너 child count가 여전히 0인지 확인하는 이유가 여기에 있다. render가 끝나기 전까지는 DOM이 비어 있어야 한다.

## commit은 나중에 한 번에, 그리고 제거는 뒤에서부터 처리한다

실제 DOM mutation은 [`ts/src/patch.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline/ts/src/patch.ts)와 `commitRoot()`에서 일어난다. 특히 `applyPatches()`는 remove를 나중에, 그것도 index 역순으로 처리한다.

```ts
const removals = patches
  .filter((patch) => patch.type === "REMOVE")
  .sort((left, right) => (right.index ?? 0) - (left.index ?? 0));

const others = patches.filter((patch) => patch.type !== "REMOVE");
```

이 ordering이 중요한 이유는 child index가 앞에서부터 무너지면 뒤 patch가 가리키는 대상이 달라질 수 있기 때문이다. create/update/replace를 먼저 하고 remove를 뒤에서부터 처리하면 DOM index 안정성이 조금 더 유지된다. 작은 구현이지만 commit ordering을 따로 의식하기 시작한 지점이라는 점에서 의미가 있다.

## `flushSync`는 render phase를 강제로 끝내고 commit까지 밀어 넣는다

[`ts/src/scheduler.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline/ts/src/scheduler.ts)의 `workLoop()`는 `timeRemaining()`이 1 미만이면 멈춘다.

```ts
while (nextUnitOfWork && !shouldYield) {
  nextUnitOfWork = performUnitOfWork(nextUnitOfWork, (fiber) => {
    deletions.push(fiber);
  });
  shouldYield = deadline.timeRemaining() < 1;
}

if (!nextUnitOfWork && wipRoot) {
  commitRoot();
}
```

여기서 `flushSync()`는 사실상 무한한 남은 시간을 주는 방식으로 work loop를 강제로 끝까지 돌린다.

```ts
export function flushSync(): void {
  workLoop({
    timeRemaining() {
      return Number.POSITIVE_INFINITY;
    },
  });
}
```

이 구조 덕분에 interrupted work도 설명 가능해진다. 첫 pass에서 시간이 부족하면 DOM은 여전히 비어 있고, 나중에 `flushSync()`를 호출하면 그때야 commit이 일어난다. 테스트 `supports interrupted work before commit`이 바로 이 경계를 고정한다.

## 이번 검증은 "계산"과 "반영"이 실제로 분리됐는지 확인하는 쪽에 가까웠다

이번 Todo에서 다시 돌린 검증은 아래 한 줄이면 충분했다.

```bash
npm run verify --workspace @front-react/render-pipeline
```

재실행 결과는 다음을 확인해 줬다.

- `diff.test.ts`, `patch.test.ts`, `scheduler.test.ts` 포함 8개 테스트 통과
- typecheck 통과

중요한 건 pass 개수보다 어떤 경계가 잠겼는가다.

- prop delta와 child diff 계산
- remove patch ordering
- render phase 동안 DOM mutation 금지
- interrupted work 뒤 commit 가능

반대로 아직 잠기지 않은 것도 분명하다.

- keyed reorder를 별도 MOVE patch로 표현하지 않는다.
- unkeyed child reorder는 identity-preserving move가 아니라 index-based rewrite로 읽힌다.

즉 이 프로젝트는 "빠른 renderer"를 만든 단계라기보다, render가 더 이상 commit과 같은 말이 아니게 된 첫 단계로 읽는 편이 정확하다.

## 그래서 이 단계가 다음 runtime으로 넘어가는 진짜 다리 역할을 한다

여기에는 아직 hooks도 없고 state도 없고 effect도 없다. 하지만 그걸 붙일 자리는 생겼다. tree를 계산하는 단계와 DOM에 반영하는 단계가 분리됐기 때문이다.

다음 단계인 `03-hooks-and-events`가 의미를 가지려면, 상태 변경이 곧바로 DOM mutation으로 직행하지 않는다는 전제가 먼저 필요하다. 이 프로젝트는 바로 그 전제를 가장 작은 fiber-like work loop와 patch system으로 고정해 둔다.
