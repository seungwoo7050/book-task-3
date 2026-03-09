# 지식 색인 — hooks와 events 핵심 개념 정리

## Hook Slot Array

함수 컴포넌트의 상태 저장 메커니즘. 컴포넌트 path별로 `HookSlot[]` 배열을 유지하고, hook 호출 순서(인덱스)로 각 slot에 접근한다.

- `instances: Map<string, HookSlot[]>` — path → slot array 매핑
- `hookIndex` — 현재 렌더에서 몇 번째 hook을 호출하고 있는지
- 호출 순서가 바뀌면(조건부 hook) 인덱스-slot 매핑이 어긋남 → 에러

관련 코드: `ts/src/runtime.ts`의 `resolveFunctionComponent`, `useState`, `useEffect`
관련 문서: `docs/concepts/hook-slot-model.md`

## useState

함수 컴포넌트에서 상태를 선언하는 hook.

```typescript
const [value, setValue] = useState<T>(initialValue);
```

- 최초 호출: `StateHookSlot` 생성, slot array에 추가
- 재렌더: 기존 slot에서 value 읽기
- `setValue(newValue)` 또는 `setValue(prev => next)` — 값 갱신 + `scheduleRender`
- `Object.is` 비교로 동일한 값이면 재렌더 건너뜀

관련 코드: `ts/src/runtime.ts`의 `useState` 함수

## useEffect

렌더링 후 부수 효과를 실행하는 hook.

```typescript
useEffect(() => {
  // setup
  return () => { /* cleanup */ };
}, [deps]);
```

실행 순서:
1. render phase — `PendingEffect`로 등록만 함
2. commit phase — DOM 갱신
3. post-commit — `runEffects`: 이전 cleanup → 새 setup

- `depsChanged(prev, next)` — `Object.is`로 각 원소 비교
- deps가 undefined면 매번 실행
- unmount 시 `collectUnmounts`가 cleanup 수집

관련 코드: `ts/src/runtime.ts`의 `useEffect`, `runEffects`, `collectUnmounts`
관련 문서: `docs/concepts/effect-timing-and-cleanup.md`

## HookContext

렌더링 진행 중의 "현재 위치" 정보.

```typescript
interface HookContext {
  root: RuntimeRoot;
  path: string;
  slots: HookSlot[];
  hookIndex: number;
  displayName: string;
}
```

- 전역 변수 `currentHookContext`에 저장
- 컴포넌트 함수 호출 전에 설정, 호출 후에 이전 context로 복원
- useState/useEffect가 이 context를 통해 어디에 slot을 저장할지 결정
- 컴포넌트 밖에서 hook 호출 시 에러 ("must be called during component render")

## RuntimeNode

VNode의 런타임 확장. 트리 위치(path)와 이벤트 핸들러를 추가로 담는다.

```typescript
interface RuntimeNode {
  type: string;
  props: Record<string, any> & { children: RuntimeNode[] };
  path: string;
  handlers: Record<string, EventHandler>;
}
```

- `path`: 트리 위치 식별자 (예: "0.1.2"). hook slot의 key로 사용
- `handlers`: on* props에서 분리된 이벤트 핸들러 맵

관련 코드: `ts/src/types.ts`, `ts/src/runtime.ts`의 `resolveHostNode`

## Delegated Event System

root container에 이벤트 타입별로 하나의 listener를 등록하고, 실제 이벤트 발생 시 target에서 root까지 올라가며 handler를 실행하는 방식.

구성 요소:
- `domToMeta: WeakMap<Node, RuntimeNodeMeta>` — DOM 노드 → handler 매핑
- `listeners: Map<string, EventListener>` — container에 등록된 listener 목록
- `requestedEvents: Set<string>` — 현재 렌더에서 필요한 event type 집합
- `dispatchDelegatedEvent` — target → root 방향으로 handler 탐색/실행

DelegatedEvent 래퍼:
```typescript
interface DelegatedEvent {
  nativeEvent: Event;
  target: EventTarget | null;
  currentTarget: EventTarget | null;  // handler가 실행되는 노드
  propagationStopped: boolean;
  preventDefault(): void;
  stopPropagation(): void;
}
```

관련 문서: `docs/concepts/delegated-event-flow.md`

## RuntimeRoot

전체 런타임 상태를 담는 중심 구조.

| 필드 | 용도 |
|------|------|
| `container` | DOM root element |
| `element` | 최상위 VNode |
| `hostTree` | 현재 RuntimeNode 트리 |
| `hostVNode` | 현재 VNode 트리 (diff 용) |
| `instances` | hook slot storage |
| `pendingEffects` | commit 후 실행할 effect 목록 |
| `pendingUnmounts` | unmount cleanup 목록 |
| `visitedInstances` | 현재 렌더에서 방문한 인스턴스 |
| `requestedEvents` | 필요한 event type |
| `domToMeta` | DOM-handler 매핑 |
| `listeners` | container listener 목록 |
| `isRendering` | 재진입 방지 플래그 |
| `needsRender` | 재렌더 필요 플래그 |

## splitProps

on* 접두사로 시작하는 props를 handler로 분리하는 함수.

```typescript
{ onClick: fn, className: "a", children: [...] }
→ domProps: { className: "a" }, handlers: { click: fn }
```

- `on` + `Click` → `click`으로 변환 (toLowerCase + slice(2))
- `children`은 domProps에서 제외

## resolveNode 흐름

```
resolveNode(vnode)
├── typeof type === "function" → resolveFunctionComponent
│   ├── HookContext 설정
│   ├── 컴포넌트 함수 호출 (useState/useEffect 가능)
│   ├── hook count 검증
│   └── 반환값을 다시 resolveNode
└── typeof type === "string" → resolveHostNode
    ├── splitProps로 handler 분리
    ├── children 재귀 resolve
    └── RuntimeNode 생성
```

## npm Workspace 의존 체인

```
vdom-foundations (01)
  ↑
render-pipeline (02) — diff, applyPatches, createElement
  ↑
hooks-and-events (03) — runtime, useState, useEffect
```

```json
"dependencies": {
  "@front-react/render-pipeline": "*"
}
```
