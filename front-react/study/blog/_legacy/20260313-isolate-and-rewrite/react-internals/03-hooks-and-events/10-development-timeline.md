# 03 Hooks And Events development timeline

`03-hooks-and-events`는 internals 트랙에서 가장 많은 판단이 한 파일에 압축된 단계다. `study/react-internals/03-hooks-and-events/ts/src/runtime.ts`를 중심으로 README, tests, 재검증 CLI를 같이 읽으면 이 프로젝트의 진짜 질문이 hooks API 자체보다 "state 변화와 effect cleanup, event bubbling을 같은 runtime에 어떻게 실어 보낼까"라는 데 있다는 점이 드러난다.

## 구현 순서 요약

1. README와 problem 문서로 이 단계가 hook trivia가 아니라 runtime integration 문제라는 점을 먼저 고정했다.
2. `dispatchDelegatedEvent`와 `syncEventListeners`를 따라 DOM metadata와 runtime tree를 연결했다.
3. `useState`/`useEffect`의 slot invariant를 읽고, 마지막에 verify와 typecheck로 integration contract를 닫았다.

## 2026-03-08 / Phase 1 - runtime integration 문제라는 점을 먼저 고정한다

- 당시 목표:
  hooks와 events를 따로 떨어진 주제로 읽지 않도록 범위를 먼저 고정한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `docs/README.md`, `ts/README.md`
- 처음 가설:
  `useState`, `useEffect`, delegated event를 각각 구현한 예제로 볼 수 있지만, README는 세 가지를 하나의 runtime loop로 묶는다고 분명히 말하고 있었다.
- 실제 진행:
  README와 problem 문서를 읽으며 runtime integration tests까지가 public contract라는 점을 먼저 고정했다.

CLI:

```bash
$ git log --reverse --stat -- study/react-internals/03-hooks-and-events | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... ts/src/runtime.ts
... ts/tests/state.test.ts
... ts/tests/effect.test.ts
... ts/tests/events.test.ts
```

검증 신호:

- source tree가 runtime source와 네 종류의 tests를 같이 가지고 있어서, 이 단계는 feature 추가보다 integration correctness가 핵심이라는 점이 보였다.

핵심 코드:

```ts
function dispatchDelegatedEvent(root: RuntimeRoot, eventType: string, nativeEvent: Event): void {
  let currentNode = nativeEvent.target as Node | null;
  while (currentNode) {
    const meta = root.domToMeta.get(currentNode);
    const handler = meta?.handlers[eventType];
```

왜 이 코드가 중요했는가:

delegated event를 단순 DOM bubbling 재사용으로만 보면 이 프로젝트 절반을 놓치게 된다. 여기서는 DOM node마다 runtime metadata를 붙이고, bubbling 과정에서도 그 metadata를 따라 handler를 찾는다. 즉 event delegation 자체가 runtime tree의 일부다.

새로 배운 것:

- event 시스템을 설명하려면 DOM과 runtime metadata의 대응 관계를 먼저 봐야 한다. 그렇지 않으면 `stopPropagation` 같은 동작도 어디서 끊기는지 흐려진다.

다음:

- hook slot과 effect timing이 이 runtime loop에 어떻게 붙는지 본다.

## 2026-03-08 / Phase 2 - hook slot과 effect timing을 같은 루프에 올린다

- 당시 목표:
  `useState`와 `useEffect`가 왜 hook order invariant를 필요로 하는지 설명한다.
- 변경 단위:
  `ts/src/runtime.ts`, `ts/tests/state.test.ts`, `ts/tests/effect.test.ts`
- 처음 가설:
  state와 effect helper를 각자 따로 읽으면 될 것 같지만, 둘 다 `currentHookContext`와 slot index를 공유하기 때문에 같은 문맥에서 봐야 한다고 판단했다.
- 실제 진행:
  `rg -n`으로 `useState`, `useEffect`, `scheduleRender` 위치를 잡고, slot 생성과 rerender scheduling, deps change에 따른 cleanup scheduling을 함께 읽었다.

CLI:

```bash
$ rg -n 'dispatchDelegatedEvent|syncEventListeners|useState|useEffect|scheduleRender' \
  study/react-internals/03-hooks-and-events/ts/src/runtime.ts
runtime.ts:111:function scheduleRender(root: RuntimeRoot)
runtime.ts:197:function dispatchDelegatedEvent(...)
runtime.ts:220:function syncEventListeners(...)
runtime.ts:427:export function useState<T>(initialValue: T)
runtime.ts:467:export function useEffect(callback: EffectCallback, deps?: DependencyList)
```

검증 신호:

- runtime metadata, scheduling, hook slot, effect queue가 모두 한 파일 안에 이어져 있어서 "같은 runtime"이라는 README 설명이 실제 코드 구조와 일치했다.

핵심 코드:

```ts
export function useState<T>(initialValue: T): [T, StateSetter<T>] {
  const { root, path, slots } = currentHookContext;
  const hookIndex = currentHookContext.hookIndex;
  const existingSlot = slots[hookIndex] as StateHookSlot<T> | undefined;
  ...
  slot.value = nextValue;
  scheduleRender(root);
}
```

왜 이 코드가 중요했는가:

`useState`는 API보다 invariant가 본질이다. 같은 render 경로에서 같은 `hookIndex`를 다시 찾아야 하고, 값이 바뀌면 즉시 DOM을 고치지 않고 runtime 전체 rerender를 예약한다. 이 구조가 있어야 effect timing과 event metadata도 같은 루프에 남는다.

새로 배운 것:

- hooks의 핵심은 저장 방식보다 순서다. slot index가 무너지면 state도 effect도 모두 잘못된 위치로 흘러간다.

다음:

- verify가 state/effect/event integration을 어떻게 묶어 확인하는지 본다.

## 2026-03-13 / Phase 3 - verify로 integration contract를 닫는다

- 당시 목표:
  runtime integration이 현재 시점에도 깨지지 않는다는 근거를 확보한다.
- 변경 단위:
  `ts/tests/state.test.ts`, `ts/tests/effect.test.ts`, `ts/tests/events.test.ts`, `ts/tests/integration.test.ts`, `tsconfig.json`
- 처음 가설:
  API 수가 많지 않으니 간단한 smoke 정도면 될 것 같지만, 이 단계는 ordering과 cleanup correctness가 중요해 integration test가 필수라고 봤다.
- 실제 진행:
  canonical verify를 다시 실행해 `4 files / 7 tests passed`와 `tsc --noEmit` 통과를 확인했다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/hooks-and-events
✓ ts/tests/state.test.ts (2 tests)
✓ ts/tests/events.test.ts (2 tests)
✓ ts/tests/effect.test.ts (2 tests)
✓ ts/tests/integration.test.ts (1 test)
Test Files  4 passed (4)
Tests  7 passed (7)
> tsc --noEmit
```

검증 신호:

- state/effect/event/integration tests가 각각 분리돼 있어서 runtime contract가 어느 층에서 깨지는지 추적하기 쉬웠다.
- typecheck 통과가 runtime public API surface를 다시 고정해 줬다.

핵심 코드:

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

왜 이 코드가 중요했는가:

effect를 즉시 실행하지 않고 pending queue에 넣는 순간, 이 runtime은 단순 helper 모음이 아니라 render 이후의 별도 phase를 가진 시스템이 된다. cleanup ordering과 setup timing을 설명하려면 바로 이 enqueue 지점이 필요하다.

새로 배운 것:

- effect는 "렌더 중에 실행되는 코드"가 아니라 render 후 별도 timing에 처리되는 계약이라는 점이 코드로 훨씬 분명해졌다.

다음:

- 이 runtime이 실제 상호작용 앱을 얼마나 버티는지는 다음 단계 `04-runtime-demo-app`에서 본다.

## 남은 경계

- `useMemo`, `useReducer`, `context`는 없다.
- synthetic event 전체 호환성과 concurrent semantics 전체를 복제하지 않는다.
- runtime은 학습용이며 production React 대체품이 아니다.
