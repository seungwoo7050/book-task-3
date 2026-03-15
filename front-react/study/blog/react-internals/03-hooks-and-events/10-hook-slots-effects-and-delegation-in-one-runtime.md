# Hook Slots, Effects, And Delegation In One Runtime

이 프로젝트를 다시 읽으면서 가장 중요하게 보였던 건 API 이름이 아니라 저장 위치였다. state는 어디에 남고, effect cleanup은 언제 실행되며, click handler는 어떻게 runtime tree를 따라 올라가는가. 이걸 따로따로 보면 조각 지식이 되지만, [`runtime.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/03-hooks-and-events/ts/src/runtime.ts)는 세 가지를 하나의 루프로 묶는다.

## hook은 "함수 안의 변수"가 아니라 path+index slot이다

`useState`와 `useEffect`의 핵심은 값 저장 자체보다 slot address다. runtime은 component path별로 `slots` 배열을 들고 있고, 현재 render 중인 component가 몇 번째 hook에 접근했는지 `hookIndex`로 추적한다.

```ts
currentHookContext = {
  root,
  path,
  slots,
  hookIndex: 0,
  displayName: getDisplayName(vnode.type),
};
```

`useState`는 이 index 위치에 state slot이 없으면 만들고, 있으면 재사용한다.

```ts
const hookIndex = currentHookContext.hookIndex;
const existingSlot = slots[hookIndex] as StateHookSlot<T> | undefined;
...
slots[hookIndex] = slot;
currentHookContext.hookIndex += 1;
```

그래서 이 runtime에서 hook identity는 이름이 아니라 call order에 달려 있다. `state.test.ts`가 조건부 hook 사용 시 `Hook order changed`를 던지는 이유도 여기 있다. 이 단계의 중요한 이해는 "hook은 magical syntax가 아니라 slot numbering discipline"이라는 점이다.

## effect는 commit 뒤에 실행되고, 다음 effect 전에 cleanup된다

`useEffect`도 비슷하게 slot index를 쓴다. 다만 state와 달리 바로 실행하지 않고 `pendingEffects`에 넣어 둔다.

```ts
if (!previousSlot || depsChanged(previousSlot.deps, deps)) {
  root.pendingEffects.push({
    path,
    index: hookIndex,
    create: callback,
    previousCleanup: previousSlot?.cleanup,
  });
}
```

그리고 실제 실행은 `commitRoot()`가 끝난 뒤 `runEffects(root)`에서 일어난다.

```ts
root.pendingEffects.forEach((effect) => {
  if (typeof effect.previousCleanup === "function") {
    effect.previousCleanup();
  }
  ...
  slot.cleanup = effect.create();
});
```

이 순서가 중요하다.

- 먼저 DOM commit
- 그다음 이전 cleanup
- 그다음 새 setup

`effect.test.ts`도 바로 이 순서를 잠근다. `setup:0 -> cleanup:0 -> setup:1`이 나와야 하고, component가 unmount되면 cleanup이 한 번 더 호출돼야 한다. 그래서 이 runtime은 effect를 "render 중 바로 실행하는 side effect"가 아니라, commit 뒤 lifecycle 단계로 분리해 둔다.

## delegated event는 DOM node가 아니라 runtime metadata를 타고 올라간다

이 프로젝트가 의외로 재미있는 부분은 event 처리다. 각 DOM 노드에 직접 listener를 붙이지 않고, root container에 이벤트 타입별 listener를 한 번만 붙인 뒤 `domToMeta` WeakMap에 저장해 둔 handler metadata를 따라 올라간다.

```ts
function syncDomMeta(root: RuntimeRoot, domNode: Node, runtimeNode: RuntimeNode): void {
  root.domToMeta.set(domNode, {
    path: runtimeNode.path,
    handlers: runtimeNode.handlers,
  });
  ...
}
```

dispatch는 이렇게 올라간다.

```ts
while (currentNode) {
  const meta = root.domToMeta.get(currentNode);
  const handler = meta?.handlers[eventType];

  if (handler) {
    const event = createDelegatedEvent(nativeEvent, currentNode);
    handler(event);
    if (event.propagationStopped) {
      return;
    }
  }
  ...
  currentNode = currentNode.parentNode;
}
```

즉 bubbling은 브라우저 native bubble만 믿는 게 아니라, runtime이 유지하는 metadata tree를 다시 타게 된다. `events.test.ts`가 button click 뒤 `["button", "section"]` 순서를 확인하고, `stopPropagation()` 호출 시 `["button"]`에서 멈추는 이유가 바로 여기 있다.

다만 여기서 "delegated event"를 React synthetic event 전체와 같은 말로 읽으면 과해진다. runtime이 직접 만드는 event 객체는 다음 정도만 담는다.

```ts
return {
  nativeEvent,
  target: nativeEvent.target,
  currentTarget,
  get defaultPrevented() {
    return nativeEvent.defaultPrevented;
  },
  get propagationStopped() {
    return propagationStopped;
  },
  preventDefault() {
    nativeEvent.preventDefault();
  },
  stopPropagation() {
    propagationStopped = true;
    nativeEvent.stopPropagation();
  },
};
```

즉 currentTarget rebinding과 stopPropagation 같은 최소 기능은 있지만, capture phase, event pooling, priority, plugin system 같은 더 넓은 synthetic event semantics는 없다. `splitProps()`도 `on...` 함수 prop만 소문자 event type으로 모을 뿐이어서, 현재 delegated layer는 "bubble-phase root listener + runtime metadata lookup" 정도로 이해하는 편이 정확하다.

## 이 runtime은 한 번에 하나의 root만 관리한다

코드에서 드러나는 중요한 경계 하나는 single-root 성격이다.

```ts
if (currentRoot && currentRoot.container !== container) {
  cleanupRoot(currentRoot);
  currentRoot = null;
  resetScheduler();
}
```

즉 다른 container에 render하면 이전 root를 정리하고 새 root로 넘어간다. multi-root runtime을 일반화한 구조는 아니다. 그리고 이 경계는 테스트가 직접 잠근 규약이라기보다 `currentRoot` 전역과 `cleanupRoot()` 호출 순서를 따라가며 읽히는 source-level conclusion이다. 이 점은 사소해 보이지만, 현재 구현이 "학습용 단일 runtime 흐름"에 맞춰져 있음을 잘 보여 준다.

## 이번 검증은 state/effect/event가 정말 같은 루프 안에서 이어지는지 확인했다

이번 Todo에서 다시 돌린 검증은 아래 한 줄이었다.

```bash
npm run verify --workspace @front-react/hooks-and-events
```

재실행 결과는 다음을 확인해 줬다.

- `state.test.ts`, `effect.test.ts`, `events.test.ts`, `integration.test.ts` 포함 7개 테스트 통과
- typecheck 통과

특히 integration test가 중요했다. button click으로 `status`가 `idle -> ready`로 바뀌고, 같은 흐름 안에서 DOM text가 업데이트되고 effect 로그가 `effect:idle -> effect:ready`로 이어지는지 본다. 이건 세 기능이 같은 runtime에 묶였다는 걸 가장 직접적으로 보여 주는 신호다.

## 그래서 이 프로젝트의 성과는 hook API 구현보다 runtime 축을 세운 데 있다

여기에는 아직 `useMemo`, `useReducer`, `context`도 없고, React의 concurrent semantics도 없다. 하지만 state slot, effect timing, delegated bubbling이 한 루프로 묶이면서 이후 demo app이 기대는 최소 런타임 축은 생겼다.

다음 단계인 `04-runtime-demo-app`은 바로 이 축 위에서 돌아간다. 중요한 건 API 수가 아니라, 상태 변경이 rerender와 effect, event propagation을 끊김 없이 통과하는 최소 모델이 이미 서 있다는 점이다.
