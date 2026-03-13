# Hook Slots, Effects, And Delegation In One Runtime

hooks를 배울 때는 종종 `useState`, `useEffect`, event bubbling을 서로 다른 챕터처럼 익힌다. 그런데 실제 런타임 코드로 내려오면 셋은 완전히 따로 놀 수가 없다. state update는 다시 render를 예약하고, commit 뒤 effect가 실행되고, 이벤트는 지금 살아 있는 runtime tree를 따라 전파되어야 한다. 하나라도 흐트러지면 나머지 둘도 같이 흔들린다.

이 프로젝트가 흥미로운 이유는 그 연결을 교과서가 아니라 구현으로 보여 준다는 점이다. `runtime.ts` 한 파일 안에 slot 저장, effect queue, DOM metadata, delegated event dispatch가 함께 들어 있다. 보기에는 빽빽하지만, 오히려 그래서 state/effect/event가 한 세계 안에 있다는 사실이 더 잘 드러난다.

처음에는 이 셋을 별개 기능처럼 보게 되지만, 코드를 끝까지 읽고 나면 결국 같은 질문으로 귀결된다. 지금 이 runtime root는 현재 tree를 얼마나 정확하게 기억하고 있는가.

## 구현 순서를 먼저 짚으면

- path와 hook index를 기준으로 slot을 저장해 `useState`와 `useEffect`를 만들었다.
- commit 뒤 effect를 실행하고 cleanup을 정리하는 queue를 붙였다.
- DOM node와 handler metadata를 root가 들고 있게 만들어 delegated event를 runtime tree 기준으로 해석했다.

## hook의 핵심은 API 이름보다 슬롯 주소였다

`useState()` 구현을 보면 setter보다 먼저 눈에 들어오는 것이 하나 있다. 현재 component path의 몇 번째 hook인지, 그리고 그 slot이 state slot인지 effect slot인지부터 검사한다는 점이다.

```ts
export function useState<T>(initialValue: T): [T, StateSetter<T>] {
  const existingSlot = slots[hookIndex] as StateHookSlot<T> | undefined;
  if (existingSlot && existingSlot.kind !== "state") {
    throw new Error(`Hook kind mismatch at ${path}:${hookIndex}.`);
  }
  if (!existingSlot) {
    const slot: StateHookSlot<T> = {
      kind: "state",
      value: initialValue,
      setState: ...
    };
    slots[hookIndex] = slot;
  }
```

이 코드는 hook이 "렌더마다 실행되는 마법 함수"가 아니라 path와 index에 걸린 slot이라는 사실을 아주 직접적으로 보여 준다. `docs/concepts/hook-slot-model.md`가 conditional hook이 왜 깨지는지 slot array 관점으로 설명하는 것도 같은 맥락이다.

여기서 새로 보인 건 `useState`의 본질이 setter가 아니라 주소 지정이라는 점이었다. 어떤 component path의 몇 번째 slot을 다시 읽어 와야 하는지를 잃는 순간, state 복원 규칙 자체가 사라진다.

## effect는 렌더 중에 실행되지 않고 commit 뒤에 줄을 선다

`useEffect()`도 마찬가지다. 중요한 건 callback을 저장한다는 사실보다, 이전 cleanup과 새 effect를 언제 실행할지를 root의 pending queue에 미룬다는 점이다.

```ts
function runEffects(root: RuntimeRoot): void {
  root.pendingUnmounts.forEach((cleanup) => cleanup());
  root.pendingEffects.forEach((effect) => {
    if (typeof effect.previousCleanup === "function") {
      effect.previousCleanup();
    }
    const slots = root.instances.get(effect.path);
    const slot = slots?.[effect.index];
    if (!slot || slot.kind !== "effect") {
      return;
    }
    slot.cleanup = effect.create();
  });
}
```

이 흐름 덕분에 effect는 렌더와 분리된 의미를 가진다. 렌더는 tree를 계산하고, commit 이후에야 effect가 실제로 실행된다. cleanup이 다음 effect보다 먼저 도는 순서까지 명시돼 있기 때문에, 이 런타임은 단순히 "effect가 있다"가 아니라 effect timing semantics를 갖게 된다.

`effect.test.ts`가 굳이 "다음 effect 전에 cleanup 되는가"를 따로 확인하는 것도 이 때문이다. effect는 side note가 아니라 commit 이후의 엄격한 후처리 단계다.

## delegated event도 결국 root가 기억하는 metadata 위에서 움직였다

이 프로젝트를 읽으며 가장 재미있었던 지점은 event delegation이 뜻밖에도 hook slot과 닮아 있다는 사실이었다. 둘 다 root가 기억하는 metadata를 조회해 현재 tree를 다시 해석한다.

```ts
function dispatchDelegatedEvent(root: RuntimeRoot, eventType: string, nativeEvent: Event): void {
  let currentNode = nativeEvent.target as Node | null;

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

    if (currentNode === root.container) {
      return;
    }
    currentNode = currentNode.parentNode;
  }
}
```

여기서는 DOM bubbling을 그대로 믿는 대신, root가 `domToMeta`를 통해 현재 노드가 어떤 runtime path에 속하는지 다시 읽는다. 그래서 host node와 function component 사이를 오가더라도 같은 규칙으로 handler를 찾을 수 있다.

즉 hook slot과 delegated event는 겉보기와 달리 같은 종류의 문제였다. 둘 다 "현재 runtime tree를 root가 얼마나 정확하게 기억하고 있는가"에 달려 있다. slot은 path/index로 찾고, event handler는 DOM metadata로 찾는다. 저장하는 형태만 다를 뿐, 본질은 같은 기억 장치다.

```bash
cd study
npm run verify --workspace @front-react/hooks-and-events
```

2026-03-13 replay 기준으로 `vitest` 7개 테스트와 `tsc --noEmit`이 통과했다. `state.test.ts`, `effect.test.ts`, `events.test.ts`, `integration.test.ts`가 각각 따로 존재하지만, 실제로는 모두 같은 흐름을 다른 각도에서 확인하는 셈이다.

## 무엇이 아직 남았는가

이 runtime은 아직 `useMemo`, `useReducer`, `context`, fully compatible synthetic event 같은 더 넓은 세계를 다루지 않는다. 하지만 여기까지 오면 적어도 하나는 분명해진다. state, effect, event는 독립 지식이 아니라 같은 runtime root가 관리하는 metadata와 timing의 문제다.

다음 단계는 이 런타임이 실제 앱을 얼마나 버티는지 보는 것이다. `04-runtime-demo-app`은 검색과 pagination과 metrics를 얹어 이 runtime이 consumer app 위에서 어디까지 설명 가능한지 확인한다.
