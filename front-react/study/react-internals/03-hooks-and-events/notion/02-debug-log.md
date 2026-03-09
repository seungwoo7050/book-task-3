# 디버그 기록 — hooks와 events에서 마주친 문제들

## hook count 변화를 감지하지 못함

### 증상

조건부로 hook을 호출하는 컴포넌트(if문 안에서 useState)를 만들었을 때, 두 번째 렌더에서 slot array의 인덱스가 어긋나면서 잘못된 값을 읽었다. 에러 없이 잘못된 상태가 표시됐다.

### 원인

resolveFunctionComponent에서 hook 호출 횟수를 체크하지 않았다. 이전 렌더에서 2개의 hook을 호출하고, 다음 렌더에서 1개만 호출하면, slot[1]의 state가 slot[0]에서 읽히는 상황이 발생한다.

### 해결

```typescript
const usedHookCount = currentHookContext.hookIndex;
if (previousSlots.length > 0 && previousSlots.length !== usedHookCount) {
  throw new Error(
    `Hook order changed for ${getDisplayName(vnode.type)}. ` +
    `Expected ${previousSlots.length} hooks but rendered ${usedHookCount}.`
  );
}
```

이전 렌더의 slot 수와 현재 렌더의 hook 호출 수를 비교하고, 다르면 즉시 에러를 던진다. 최초 렌더(previousSlots.length === 0)에서는 체크를 건너뛴다.

state.test.ts의 "throws when the hook count changes between renders" 테스트가 이 invariant를 정확히 검증한다.

## effect cleanup 순서 혼동

### 증상

effect가 의존성 변화로 재실행될 때, 새 effect가 먼저 실행되고 이전 cleanup이 나중에 실행됐다. `calls` 배열이 `["setup:0", "setup:1", "cleanup:0"]` 순으로 기록됐다.

### 원인

runEffects에서 cleanup과 setup을 분리하지 않았다. PendingEffect를 순회하면서 create()만 호출하고, previousCleanup은 무시하고 있었다.

### 해결

runEffects의 순서를 명확히 했다:

1. unmount cleanup 먼저 실행 (`pendingUnmounts`)
2. 각 pending effect마다 `previousCleanup()` 호출 후 `create()` 호출
3. create의 반환값을 slot.cleanup에 저장

```typescript
root.pendingUnmounts.forEach((cleanup) => cleanup());
root.pendingUnmounts = [];

root.pendingEffects.forEach((effect) => {
  if (typeof effect.previousCleanup === "function") {
    effect.previousCleanup();
  }
  const slot = slots?.[effect.index];
  slot.cleanup = effect.create();
});
```

effect.test.ts의 "runs effects after commit and cleans them up before the next effect" 테스트로 검증: `["setup:0", "cleanup:0", "setup:1"]` 순서가 보장된다.

## unmount cleanup이 실행되지 않음

### 증상

컴포넌트를 다른 VNode으로 교체하면, 이전 컴포넌트의 effect cleanup이 호출되지 않았다.

### 원인

collectUnmounts가 누락되어 있었다. render phase에서 방문한 인스턴스(visitedInstances)와 전체 인스턴스(instances) Map을 비교해서, 방문하지 않은 인스턴스의 cleanup을 수집해야 하는데, 이 로직이 없었다.

### 해결

performRender 안에서 resolveNode 후 collectUnmounts를 호출한다:

```typescript
const nextTree = resolveNode(root, root.element, "0");
collectUnmounts(root);
commitRoot(root, nextTree);
```

collectUnmounts는 instances Map을 순회하면서 visitedInstances에 없는 path의 effect cleanup을 pendingUnmounts에 추가하고, instances에서 삭제한다. 그러면 runEffects의 첫 단계에서 이 cleanup들이 실행된다.

## event handler가 리렌더 후 작동하지 않음

### 증상

setState로 재렌더가 발생한 후, 버튼의 onClick handler가 호출되지 않았다. 첫 클릭은 됐지만 두 번째 클릭부터 반응이 없었다.

### 원인

domToMeta WeakMap이 리렌더 후 갱신되지 않았다. commit에서 DOM을 교체하면 새 DOM 노드가 생기는데, 이전 DOM 노드에 매핑된 메타 정보만 남아 있었다.

### 해결

commitRoot에서 DOM 갱신 후 domToMeta를 새로 만들고 syncDomMeta를 다시 호출한다:

```typescript
root.domToMeta = new WeakMap();
if (nextTree && root.container.firstChild) {
  syncDomMeta(root, root.container.firstChild, nextTree);
}
```

WeakMap을 교체하는 게 핵심이다. 이전 DOM 노드에 대한 참조는 GC가 수거하고, 새 DOM 노드와 새 RuntimeNode의 매핑만 남는다.

## delegated event의 bubbling 경로 혼동

### 증상

중첩된 handler에서 버튼 클릭 시 section의 handler가 먼저 호출되고, 그 다음에 button의 handler가 호출됐다.

### 원인

dispatchDelegatedEvent에서 root.container부터 시작해서 target으로 내려가는 방향(capture)으로 순회했다. DOM 이벤트의 bubbling은 target에서 root로 올라가는 방향이다.

### 해결

```typescript
let currentNode = nativeEvent.target as Node | null;
while (currentNode) {
  const meta = root.domToMeta.get(currentNode);
  const handler = meta?.handlers[eventType];
  if (handler) {
    const event = createDelegatedEvent(nativeEvent, currentNode);
    handler(event);
    if (event.propagationStopped) return;
  }
  if (currentNode === root.container) return;
  currentNode = currentNode.parentNode;
}
```

target에서 시작해 parentNode를 따라 올라간다. container에 도달하면 멈춘다. 이 순서가 DOM의 bubbling phase와 일치한다.

## HookContext 복원 누락

### 증상

중첩된 함수 컴포넌트(App 안에 Counter)에서 Counter의 useState가 App의 slot을 덮어썼다.

### 원인

resolveFunctionComponent에서 컴포넌트 함수 호출 전에 currentHookContext를 설정했지만, 호출 후에 이전 context를 복원하지 않았다. 재귀적으로 resolveNode가 호출될 때, 내부 컴포넌트의 context가 외부 컴포넌트의 context를 덮어쓴다.

### 해결

```typescript
const previousContext = currentHookContext;
currentHookContext = { root, path, slots, hookIndex: 0, displayName };
const output = (vnode.type as Function)(vnode.props);
currentHookContext = previousContext;
```

호출 전에 저장하고, 호출 후에 복원한다. 스택 프레임과 같은 패턴이다.

## splitProps에서 children 속성 누수

### 증상

domProps에 children 배열이 포함되어 diff 결과에 영향을 미쳤다.

### 원인

splitProps가 모든 props를 domProps에 넣고, on* 접두사만 handlers로 분리했다. children은 VNode의 props에 항상 있지만 DOM 속성이 아니다.

### 해결

```typescript
if (key === "children") return;
```

splitProps 루프 초반에 children을 skip한다. vdom-foundations의 updateDom이 children을 무시하도록 되어 있지만, 여기서도 명시적으로 거르는 게 안전하다.
