# 지식 색인 — render pipeline 핵심 개념 정리

## Diff (변경 계산)

두 VNode 트리를 비교해서 차이를 데이터로 표현하는 과정. 이 프로젝트에서 diff는 순수 함수다 — DOM에 접근하지 않고, Patch 배열을 반환한다.

- `diffProps(oldProps, newProps)` → `{ set: {...}, remove: [...] }`
- `diffChildren(oldChildren, newChildren)` → `Patch[]`
- `diff(oldNode, newNode)` → `Patch`

관련 코드: `ts/src/diff.ts`

## Patch 타입

diff의 결과를 표현하는 네 가지 유형:

| 타입 | 의미 | 조건 |
|------|------|------|
| CREATE | 새 노드 추가 | oldNode 없고 newNode 있음 |
| REMOVE | 기존 노드 제거 | oldNode 있고 newNode 없음 |
| REPLACE | 노드 전체 교체 | 타입(tag)이 다름 |
| UPDATE | 속성/자식만 갱신 | 같은 타입, props나 children이 다름 |

관련 코드: `ts/src/types.ts`, `ts/src/patch.ts`

## Keyed vs Unkeyed Child Diff

자식 비교 전략이 두 가지로 나뉜다:

- **Unkeyed**: 인덱스 위치로 비교. 인덱스 0끼리, 1끼리 비교. 순서가 바뀌면 전부 UPDATE/REPLACE.
- **Keyed**: key 속성으로 식별. old children을 Map<key, VNode>으로 만들어 O(1) lookup. 위치가 바뀌어도 같은 key면 같은 노드.

이 프로젝트에서는 모든 자식에 key가 있으면 keyed, 아니면 unkeyed로 분기한다. 혼합은 고려하지 않는다.

관련 코드: `ts/src/diff.ts`의 `diffChildren`, `diffChildrenByKey`, `diffChildrenByIndex`

## Fiber

React의 작업 단위. VNode 트리를 linked list로 변환한 구조:

```
parent ← fiber → child
            ↓
         sibling → sibling.child
```

- `type`: 노드 타입 (태그 이름 또는 "ROOT")
- `props`: VNodeProps
- `dom`: 실제 DOM 노드 (아직 안 붙임)
- `parent/child/sibling`: 트리 포인터
- `alternate`: 이전 commit의 같은 위치 fiber
- `effectTag`: PLACEMENT | UPDATE | DELETION

관련 코드: `ts/src/types.ts`, `ts/src/fiber.ts`

## Effect Tag

fiber에 부여되는 DOM 조작 유형:

| Effect | 조건 | commitWork 동작 |
|--------|------|-----------------|
| PLACEMENT | 새로 추가된 fiber | `appendChild` |
| UPDATE | 타입이 같고 props가 다름 | `updateDom` |
| DELETION | old fiber에 대응하는 new element 없음 | `removeChild` |

관련 코드: `ts/src/fiber.ts`의 `reconcileChildren`, `ts/src/scheduler.ts`의 `commitWork`

## Render Phase vs Commit Phase

이 프로젝트의 핵심 mental model:

**Render Phase:**
- fiber tree를 구성하고 effect tag를 부여
- DOM을 건드리지 않음
- 중단 가능 (cooperative scheduling)
- `render()` → `workLoop()` → `performUnitOfWork()`

**Commit Phase:**
- effect tag에 따라 실제 DOM mutation
- 중단 불가 (한 번 시작하면 끝까지)
- `commitRoot()` → `commitWork()` → DOM API 호출

테스트로 검증: render 직후 container는 비어 있고, flushSync 후에야 노드가 나타남.

관련 문서: `docs/concepts/render-vs-commit.md`

## Work Loop

cooperative scheduling 패턴:

```typescript
while (nextUnitOfWork && !shouldYield) {
  nextUnitOfWork = performUnitOfWork(nextUnitOfWork, onDelete);
  shouldYield = deadline.timeRemaining() < 1;
}
```

- `deadline.timeRemaining()`: 남은 유휴 시간 (ms). 브라우저의 `requestIdleCallback`이 제공.
- 시간이 부족하면 루프를 빠져나오고, 다음 idle period에 이어서 진행.
- 테스트에서는 `IdleDeadlineLike` 인터페이스로 추상화하고, `flushSync()`로 무한 시간을 제공.

관련 코드: `ts/src/scheduler.ts`, `ts/src/types.ts`

## Fiber 순회 순서

`performUnitOfWork`가 반환하는 다음 fiber의 우선순위:

1. **child** — 자식이 있으면 깊이 들어감
2. **sibling** — 형제가 있으면 옆으로 이동
3. **uncle (parent.sibling)** — parent로 올라가며 sibling 탐색

이 순서로 전체 트리를 재귀 없이 반복문으로 순회한다. "다음에 처리할 fiber"라는 커서 하나로 상태를 유지할 수 있다.

## Alternate (Double Buffering)

wipRoot(작업 중인 트리)와 currentRoot(마지막으로 커밋된 트리)를 구분한다. render를 시작할 때 wipRoot의 alternate에 currentRoot를 연결하고, commit이 끝나면 `currentRoot = wipRoot`로 교체한다.

개별 fiber도 alternate로 이전 버전을 참조한다. UPDATE 시 이전 props를 알아야 `updateDom(dom, oldProps, newProps)`를 호출할 수 있다.

## npm Workspace 의존

`@front-react/render-pipeline`은 `@front-react/vdom-foundations`를 dependencies로 참조한다. workspace symlink를 통해 로컬 패키지를 직접 import한다. createElement, createDom, updateDom, VNode 타입을 모두 01에서 가져온다.

```json
"dependencies": {
  "@front-react/vdom-foundations": "*"
}
```

관련 파일: `package.json`
