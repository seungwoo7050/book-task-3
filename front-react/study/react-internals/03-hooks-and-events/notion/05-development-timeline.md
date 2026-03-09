# 개발 타임라인 — hooks와 events 프로젝트 구축 과정

## Phase 0: 프로젝트 초기화 및 의존 연결

```bash
cd study
npm install
```

workspace 루트에서 install을 실행하면, `@front-react/hooks-and-events`의 package.json에 선언된 `@front-react/render-pipeline` 의존이 symlink로 연결된다. render-pipeline이 다시 vdom-foundations를 참조하므로, 3단계 의존 체인이 형성된다.

```
node_modules/@front-react/render-pipeline → ../../02-render-pipeline
node_modules/@front-react/vdom-foundations → ../../01-vdom-foundations
```

## Phase 1: 타입 설계

```
ts/src/types.ts
```

VNode을 render-pipeline에서 import하고, 이 프로젝트 고유 타입을 정의:
- SetStateAction, StateSetter — useState의 타입
- EffectCallback, DependencyList — useEffect의 타입
- DelegatedEvent, EventHandler — 이벤트 위임의 타입
- HookSlot (StateHookSlot | EffectHookSlot) — slot array의 원소
- RuntimeNode, RuntimeNodeMeta — VNode의 런타임 확장
- PendingEffect — commit 후 실행할 effect 정보
- RuntimeRoot — 전체 런타임 상태
- HookContext — 렌더링 중 hook 호출 위치

## Phase 2: runtime.ts 핵심 구조 구현

```
ts/src/runtime.ts
```

하나의 파일에 전체 runtime을 구현. 순서대로:

1. **헬퍼 함수**: normalizeChild, splitProps, createRuntimeNode, toVNode, depsChanged, getDisplayName
2. **render 흐름**: resolveNode, resolveFunctionComponent, resolveHostNode
3. **commit 흐름**: commitRoot (diff/applyPatches 사용)
4. **effect 관리**: collectUnmounts, runEffects
5. **event delegation**: createDelegatedEvent, dispatchDelegatedEvent, syncEventListeners, syncDomMeta
6. **스케줄링**: scheduleRender, performRender
7. **공개 API**: createElement, render, flushSync, resetRuntime, useState, useEffect

## Phase 3: useState 테스트

```
ts/tests/state.test.ts
```

두 가지 시나리오를 작성:

```bash
npm run test --workspace @front-react/hooks-and-events -- --run state
```

1. event handler에서 setState → 재렌더 후 업데이트된 텍스트 확인
2. 조건부 hook 호출 → Hook order changed 에러 검증

## Phase 4: useEffect 테스트

```
ts/tests/effect.test.ts
```

```bash
npm run test --workspace @front-react/hooks-and-events -- --run effect
```

1. setup/cleanup 순서 검증: `["setup:0", "cleanup:0", "setup:1"]`
2. unmount 시 cleanup 호출 검증 (vi.fn 사용)

## Phase 5: delegated events 테스트

```
ts/tests/events.test.ts
```

```bash
npm run test --workspace @front-react/hooks-and-events -- --run events
```

1. bubbling 순서 검증: button → section (target → parent)
2. stopPropagation 검증: button만 호출되고 section은 스킵

## Phase 6: integration 테스트

```
ts/tests/integration.test.ts
```

```bash
npm run test --workspace @front-react/hooks-and-events -- --run integration
```

event → state update → rerender → effect의 전체 흐름을 하나의 테스트에서 검증:
- 초기 render: status "idle", lifecycle에 "effect:idle"
- 버튼 클릭: status "ready", lifecycle에 "effect:ready" 추가

## Phase 7: barrel export 구성

```
ts/src/index.ts
```

공개 API: createElement, render, flushSync, resetRuntime, useState, useEffect
타입 export: DelegatedEvent, EventHandler, RuntimeNode 등

## Phase 8: 타입 체크

```bash
npm run typecheck --workspace @front-react/hooks-and-events
```

strict mode에서 타입 일관성 확인. render-pipeline의 VNode 타입과 이 프로젝트의 RuntimeNode 타입이 올바르게 연결되는지 검증.

## Phase 9: 문서 작성

```
docs/concepts/hook-slot-model.md
docs/concepts/effect-timing-and-cleanup.md
docs/concepts/delegated-event-flow.md
docs/references/verification-notes.md
```

각 축(hook, effect, event)의 설계 결정과 범위 제한을 기록.

## Phase 10: 전체 검증

```bash
cd study
npm run verify --workspace @front-react/hooks-and-events
```

verify = test + typecheck 순차 실행. 모든 검증 통과 후 `verified` 상태로 전환.

## 사용된 도구 정리

| 도구 | 용도 |
|------|------|
| TypeScript 5.3 | strict mode 타입 체크 |
| Vitest 1.6.0 | 단위/통합 테스트 |
| jsdom 24.0.0 | DOM API 에뮬레이션 (document, Event, MouseEvent) |
| npm workspaces | 로컬 패키지 의존 (render-pipeline → vdom-foundations) |
| vi.fn() | effect cleanup 호출 추적 |

## 디렉토리 구조

```
03-hooks-and-events/
├── package.json          # @front-react/hooks-and-events
├── tsconfig.json
├── vitest.config.ts
├── README.md
├── docs/
│   ├── concepts/
│   │   ├── hook-slot-model.md
│   │   ├── effect-timing-and-cleanup.md
│   │   └── delegated-event-flow.md
│   └── references/
│       └── verification-notes.md
├── problem/              # 레거시 원문
├── ts/
│   ├── src/
│   │   ├── types.ts      # 전체 타입 정의
│   │   ├── runtime.ts    # useState, useEffect, event delegation, render loop
│   │   └── index.ts      # barrel export
│   └── tests/
│       ├── state.test.ts       # useState 동작 + hook invariant
│       ├── effect.test.ts      # effect lifecycle
│       ├── events.test.ts      # delegated bubbling
│       └── integration.test.ts # 전체 흐름 통합
└── notion/               # (로컬 전용)
```
