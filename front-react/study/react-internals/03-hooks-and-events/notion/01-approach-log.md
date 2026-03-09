# 접근 기록 — hooks와 events 구현 과정

## 타입 설계: RuntimeRoot라는 중심 구조

이 프로젝트의 핵심 설계는 types.ts의 `RuntimeRoot` 인터페이스에 집약되어 있다. 이전 프로젝트들이 모듈 분리로 관심사를 나눴다면, 이 프로젝트는 하나의 root 객체가 전체 런타임 상태를 담는다.

```typescript
interface RuntimeRoot {
  container: HTMLElement;
  element: VNode;
  hostTree: RuntimeNode | null;
  hostVNode: VNode | null;
  instances: Map<string, HookSlot[]>;
  pendingEffects: PendingEffect[];
  pendingUnmounts: Array<() => void>;
  visitedInstances: Set<string>;
  requestedEvents: Set<string>;
  domToMeta: WeakMap<Node, RuntimeNodeMeta>;
  listeners: Map<string, EventListener>;
  isRendering: boolean;
  needsRender: boolean;
}
```

이 구조가 useState의 slot storage, useEffect의 pending queue, event delegation의 listener registry, 재렌더링 스케줄링까지 모두 관장한다.

**RuntimeNode**는 VNode의 런타임 확장이다. path(트리 위치 식별자)와 handlers(이벤트 핸들러 맵)를 추가로 가진다. 이 path가 hook slot의 key로 쓰인다 — 같은 path는 같은 컴포넌트 인스턴스다.

**HookSlot**은 StateHookSlot과 EffectHookSlot의 유니온이다. kind 필드로 구분한다. 하나의 slot array 안에 state와 effect가 섞여 있고, 호출 순서(인덱스)로 구분된다.

## useState 구현: closure와 slot array

useState의 구현은 세 가지를 해결해야 한다:
1. 최초 호출 시 slot 생성
2. 재렌더 시 기존 slot에서 값 읽기
3. setState가 호출되면 값 갱신 + 재렌더 예약

핵심은 closure다. setState 함수는 생성 시점에 자신의 slot을 캡처한다. 나중에 어디서 호출되든 `slot.value`를 직접 갱신한다.

```typescript
const slot: StateHookSlot<T> = {
  kind: "state",
  value: initialValue,
  setState: (action) => {
    const nextValue = typeof action === "function"
      ? (action as Function)(slot.value)
      : action;
    if (Object.is(nextValue, slot.value)) return;
    slot.value = nextValue;
    scheduleRender(root);
  }
};
```

`Object.is` 비교로 같은 값이면 재렌더를 건너뛴다. functional update(`setCount(c => c + 1)`)도 지원한다.

**HookContext**는 렌더링 진행 중의 "현재 위치" 정보다. 어떤 root의, 어떤 path에서, 몇 번째 hook을 호출하고 있는지 추적한다. 전역 변수 `currentHookContext`에 저장되고, 컴포넌트 함수 호출 전에 설정되고 후에 복원된다.

## useEffect 구현: 등록과 지연 실행

useEffect는 render phase에서 "이 effect를 나중에 실행해 달라"고 등록만 한다. 실제 실행은 commit이 끝난 후.

핵심 로직:

1. 이전 slot의 deps와 새 deps를 비교한다 (`depsChanged`)
2. deps가 바뀌었으면 `PendingEffect`를 root.pendingEffects에 추가
3. commit 후 `runEffects()`에서 순서대로 실행

`depsChanged`의 구현은 단순하다: `Object.is`로 각 원소를 비교하고, 길이가 다르거나 하나라도 다르면 true.

cleanup은 이전 effect의 반환값이다. 새 effect를 실행하기 전에 `previousCleanup()`을 호출한다. unmount 시에는 `collectUnmounts()`가 방문하지 않은 인스턴스의 effect cleanup을 수집하고, `runEffects()` 첫 단계에서 실행한다.

## createElement: 함수 컴포넌트 지원

createElement를 render-pipeline의 것을 감싸서 다시 정의한다. 이유는 render-pipeline의 createElement가 string type만 받는데, 이 프로젝트에서는 function type도 전달해야 하기 때문이다.

```typescript
export function createElement(type: string | Function, props, ...children): VNode {
  return baseCreateElement(type as any, props, ...children);
}
```

`type as any`는 타입 시스템을 우회하는 것이다. runtime에서는 function component의 type 필드에 함수 자체가 들어간다. resolveNode에서 `typeof vnode.type === "function"`으로 분기한다.

## resolveNode: VNode 트리를 RuntimeNode 트리로 변환

이 함수가 render phase의 핵심이다. VNode을 받아 RuntimeNode를 반환한다.

- string type: **resolveHostNode**로 간다. props에서 event handler(on* 접두사)를 분리하고, children을 재귀적으로 resolve한다. handler의 event type을 `requestedEvents`에 등록한다.
- function type: **resolveFunctionComponent**로 간다. 이전 slot을 복원하고 HookContext를 설정한 뒤 함수를 호출한다. 반환값을 다시 resolveNode에 넣는다.

함수 컴포넌트 호출 전후로 HookContext를 save/restore하는 패턴이 중요하다. 컴포넌트가 중첩될 때(App 안에 Counter가 있을 때) 각자의 context가 보존된다.

## delegated event: root에서 dispatch

이벤트 위임은 세 단계로 구현된다.

**1. syncEventListeners**: commit 후에 호출. `requestedEvents`에 있는 event type은 container에 listener를 등록하고, 더 이상 사용하지 않는 event type의 listener는 제거한다.

**2. syncDomMeta**: DOM 노드와 RuntimeNode를 매핑하는 WeakMap을 구성한다. DOM 노드에서 해당 RuntimeNode의 path와 handlers를 찾을 수 있게 한다.

**3. dispatchDelegatedEvent**: 실제 이벤트 발생 시 호출. target에서 시작해 parentNode를 따라 root까지 올라가며, 각 노드의 handler를 실행한다. handler는 DelegatedEvent 래퍼를 받는다 — stopPropagation이 호출되면 루프를 멈춘다.

DelegatedEvent는 nativeEvent를 감싸는 proxy다. currentTarget을 handler가 실행되는 노드로 고정하고, propagationStopped 플래그를 관리한다. DOM의 native bubbling과는 별개의 자체 bubbling이다.

## commitRoot: 전체 흐름을 묶는 곳

commitRoot는 이전 프로젝트의 diff/applyPatches를 사용해 DOM을 갱신한다.

```
hostVNode 없고 nextVNode 있음 → CREATE patch
hostVNode 있고 nextVNode 없음 → REMOVE patch
둘 다 있음 → diff해서 결과 patch 적용
```

DOM 갱신 후:
1. hostTree와 hostVNode 교체
2. domToMeta WeakMap 재구축 (syncDomMeta)
3. event listener 동기화 (syncEventListeners)
4. effect 실행 (runEffects)

## performRender: 재렌더 루프

scheduleRender가 `needsRender = true`를 설정하고 performRender를 호출한다. performRender는 `while(root.needsRender)` 루프를 돌린다.

이 루프가 필요한 이유: effect 안에서 setState가 호출되면 또 다시 needsRender가 true가 된다. 한 번의 performRender 안에서 연쇄적인 재렌더를 처리한다.

`isRendering` 플래그로 재진입을 방지한다. render 중에 setState가 호출되면 needsRender만 true로 만들고, 현재 루프의 다음 iteration에서 처리된다.

## index.ts: 최소 공개 API

내보내는 것: createElement, render, flushSync, resetRuntime, useState, useEffect  
타입만 내보내는 것: DelegatedEvent, EventHandler, RuntimeNode 등

다음 프로젝트(04-runtime-demo-app)가 이 패키지를 import해서 실제 앱을 만든다.
