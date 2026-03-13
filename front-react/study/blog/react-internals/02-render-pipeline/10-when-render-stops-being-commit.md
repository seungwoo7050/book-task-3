# When Render Stops Being Commit

foundation 단계의 순진한 렌더러는 분명 이해하기 쉽다. 하지만 그 단순함은 동시에 한계를 숨기지 않는다. old tree와 new tree가 있는데 무엇이 달라졌는지 계산하지 못하고, DOM을 언제 건드리는지도 통제하지 못한다면, "다시 그린다"는 말은 사실상 "처음부터 다시 만든다"와 다르지 않다.

이 프로젝트는 그 상태에서 한 발 더 내려간다. render를 계산 단계로, commit을 반영 단계로 갈라서 보고, 그 사이에 diff와 patch와 work loop를 넣는다. 이름만 보면 복잡하지만, 실제로는 한 가지 질문을 계속 붙잡는 과정이다. 지금 이 변경은 어디서 계산되고, 어디서 실제 DOM이 바뀌는가.

그 질문이 선명해지는 순간, keyed child와 patch ordering, interrupted work 같은 주제도 더 이상 별개의 테크닉이 아니라 같은 파이프라인의 일부로 읽히기 시작한다.

## 구현 순서를 먼저 짚으면

- `diff.ts`에서 prop delta와 child patch를 계산하는 change detection부터 만들었다.
- `patch.ts`에서 create/update/remove 순서를 정리해 DOM-safe한 반영 규칙을 만들었다.
- `scheduler.ts`에서 render phase와 commit phase를 분리하고 `flushSync()` semantics를 고정했다.

## 먼저 "무엇이 달라졌는가"를 계산하는 단계가 필요했다

이 프로젝트의 첫 전환점은 patch가 아니라 diff다. 특히 child는 key 유무에 따라 비교 전략이 달라지므로, 단순히 같은 index끼리 비교하는 것만으로는 충분하지 않았다.

```ts
function diffChildrenByKey(oldChildren: VNode[], newChildren: VNode[]): Patch[] {
  const oldMap = new Map<string, { node: VNode; index: number }>();
  ...
  if (!oldMatch) {
    patches.push({ type: "CREATE", newNode: child, index });
    return;
  }
  ...
  if (typeof key === "string" && !visitedKeys.has(key)) {
    patches.push({ type: "REMOVE", oldNode: child, index });
  }
}
```

이 코드가 바꿔 놓은 건 성능보다 identity 모델이다. key가 있는 child는 더 이상 "같은 위치의 노드"가 아니라 "같은 정체성을 가진 노드"로 비교된다. 이 차이가 있어야 다음 단계의 patch도 단순한 배열 치환이 아니라 의미 있는 노드 이동/삭제/생성으로 읽힌다.

`diff.test.ts`가 keyed create/remove와 type change replace를 먼저 잡아 두는 것도 그래서다. render pipeline의 첫걸음은 DOM mutation이 아니라 change detection의 의미를 고정하는 일이다.

## patch는 계산보다 순서가 더 중요했다

patch를 적용할 때 흥미로운 지점은 알고리즘보다 순서였다. 특히 remove patch를 앞에서부터 적용하면 index가 밀려서 나머지 patch가 엉뚱한 노드를 건드릴 수 있다. 그래서 이 구현은 remove를 따로 모아 뒤에서 적용한다.

```ts
export function applyPatches(parent: HTMLElement | Text, patches: Patch[]): void {
  const removals = patches
    .filter((patch) => patch.type === "REMOVE")
    .sort((left, right) => (right.index ?? 0) - (left.index ?? 0));

  const others = patches.filter((patch) => patch.type !== "REMOVE");
  others.forEach((patch) => applyPatchAt(parent, patch, patch.index ?? 0));
  removals.forEach((patch) => applyPatchAt(parent, patch, patch.index ?? 0));
}
```

이 짧은 함수는 render pipeline이 왜 필요한지 아주 선명하게 보여 준다. DOM 반영은 "패치를 받았다, 실행한다"로 끝나지 않는다. 어떤 patch를 먼저 적용하느냐가 곧 correctness 문제다.

foundation 단계에서 `updateDom()` 정책을 먼저 분리해 둔 덕분에, 여기서는 DOM-safe ordering만 집중해서 다룰 수 있었다. 아래 계층이 미리 정리돼 있으면 위 계층도 이유 있는 단순함을 얻는다는 점이 잘 드러나는 장면이다.

## render가 commit과 갈라지는 순간 scheduler가 의미를 얻었다

마지막 전환점은 `workLoop()`다. 이 함수는 다음 unit of work를 조금씩 처리하고, 시간이 다 되면 yield한다. 그리고 더 이상 남은 일이 없을 때만 `commitRoot()`를 호출한다.

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

이 시점부터 render는 더 이상 DOM을 즉시 바꾸는 말이 아니다. 계산만 하고 멈출 수 있는 단계가 된다. `docs/concepts/render-vs-commit.md`가 render phase에서 DOM을 바꾸지 않는다고 굳이 강조하는 이유도 여기에 있다. commit timing을 분리해야 interrupted work와 `flushSync()`를 같은 언어로 설명할 수 있다.

검증도 그 점을 정확히 겨냥한다. `scheduler.test.ts`는 render 직후 container가 아직 비어 있는지, `flushSync()`가 끝난 뒤에만 commit이 일어나는지를 확인한다. 즉 이 프로젝트의 correctness는 눈에 보이는 결과보다 "언제" 반영되느냐에 더 가깝다.

```bash
cd study
npm run verify --workspace @front-react/render-pipeline
```

2026-03-13 replay 기준으로 `vitest` 8개 테스트와 `tsc --noEmit`이 모두 통과했다. 이 수치가 말해 주는 건, diff와 patch와 scheduler가 같은 파이프라인으로 묶였고 그 경계가 깨지지 않았다는 사실이다.

## 무엇이 아직 남았는가

여기까지 와도 state와 effect와 event는 아직 없다. 즉 "언제 다시 계산할 것인가"와 "계산 결과를 언제 반영할 것인가"는 생겼지만, 무엇이 그 계산을 촉발하는지는 아직 비어 있다.

그래서 다음 프로젝트는 자연스럽게 hook runtime으로 넘어간다. `03-hooks-and-events`는 바로 이 파이프라인 위에 state slot, effect cleanup, delegated event를 올려서 실제 상호작용이 어디서부터 시작되는지 설명한다.
