# 디버그 기록 — render pipeline에서 마주친 문제들

## patch 순서와 인덱스 밀림

### 증상

REMOVE patch를 앞쪽 인덱스부터 적용하면 뒤쪽 노드의 인덱스가 변한다. 예를 들어 인덱스 0을 지우면, 원래 인덱스 1이었던 노드가 0이 된다. 그 상태에서 인덱스 1을 지우면 원래 인덱스 2였던 노드가 사라진다.

### 원인

`childNodes`는 live collection이다. removeChild를 호출하면 즉시 인덱스가 재정렬된다. patch 배열의 인덱스는 원래 트리 기준이므로, 앞에서부터 지우면 인덱스-값 매핑이 어긋난다.

### 해결

applyPatches에서 REMOVE 패치를 분리하고, 인덱스 내림차순으로 정렬한 뒤 처리한다. 뒤에서부터 지우면 앞쪽 인덱스에 영향이 없다. 나머지 패치(CREATE, REPLACE, UPDATE)는 이후에 원래 순서대로 적용한다.

```typescript
const removals = patches.filter(p => p.type === "REMOVE");
const others = patches.filter(p => p.type !== "REMOVE");
removals.sort((a, b) => (b.index ?? 0) - (a.index ?? 0));
```

## render phase에서 DOM이 바뀌는 현상

### 증상

초기 구현에서 `render()` 호출 직후 container에 노드가 나타났다. scheduler.test.ts의 "does not mutate the DOM during the render phase" 테스트가 실패했다.

### 원인

fiber를 생성하면서 동시에 DOM에 붙이고 있었다. render phase와 commit phase의 경계가 없었다. performUnitOfWork 안에서 createDom을 호출하는 것까지는 맞지만, 생성한 dom을 parent.dom에 appendChild하는 코드가 섞여 있었다.

### 해결

performUnitOfWork에서는 fiber.dom을 만들기만 하고, parent.dom에 붙이는 행위는 commitWork에서만 한다. render 함수는 wipRoot와 nextUnitOfWork만 설정하고 workLoop에 위임한다. DOM mutation은 commitRoot가 호출될 때만 발생한다.

## interrupted work 후 partial commit

### 증상

workLoop에서 timeRemaining이 0을 반환해 중간에 멈추면, 일부 fiber만 처리된 상태가 된다. 이 상태에서 commitRoot가 호출되면 불완전한 트리가 DOM에 반영된다.

### 원인

commitRoot 시점의 조건이 잘못되어 있었다. nextUnitOfWork가 아직 남아 있는데 commitRoot를 호출하는 경로가 있었다.

### 해결

workLoop의 commit 조건을 `!nextUnitOfWork && wipRoot`로 변경했다. 모든 작업이 끝나야(nextUnitOfWork === null) commit한다. 중간에 멈춘 경우는 다음 workLoop 호출에서 이어서 진행한다.

```typescript
if (!nextUnitOfWork && wipRoot) {
  commitRoot();
}
```

테스트에서 이 시나리오를 정확히 검증한다: 첫 번째 workLoop에서 시간이 부족해 중단되고, container는 비어 있다. flushSync를 호출하면 나머지 작업을 마치고 commit한다.

## fiber 순회 순서 혼동

### 증상

performUnitOfWork에서 다음 fiber를 반환하는 로직이 잘못되어, 일부 sibling이 건너뛰어졌다.

### 원인

child → sibling → uncle 순회에서 sibling이 없을 때 parent로 올라가는 부분에서, parent 자체를 다음 작업으로 반환하고 있었다. parent는 이미 처리했으므로 parent.sibling을 반환해야 한다.

### 해결

```typescript
let nextFiber: Fiber | null = fiber;
while (nextFiber) {
  if (nextFiber.sibling) return nextFiber.sibling;
  nextFiber = nextFiber.parent;
}
return null;
```

parent로 올라가면서 sibling을 찾는 루프다. sibling이 있으면 반환하고, 없으면 계속 올라간다. root까지 올라가면 null을 반환하고 작업이 종료된다.

## vdom-foundations 의존 타이밍

### 증상

npm workspace에서 02-render-pipeline의 테스트를 실행하면 `@front-react/vdom-foundations` 모듈을 찾지 못하는 에러가 발생했다.

### 원인

workspace 루트에서 `npm install`을 실행하지 않으면 symlink가 생성되지 않는다. 또한 vdom-foundations의 index.ts에서 export하지 않는 함수를 import하려고 시도한 경우도 있었다.

### 해결

`cd study && npm install`로 workspace 링크를 갱신하고, import 대상이 vdom-foundations의 index.ts에서 실제로 export되는지 확인했다. 01 프로젝트의 공개 API와 02의 import가 정확히 일치해야 한다.

## commitDeletion의 재귀 구조

### 증상

dom이 없는 fiber를 삭제하려 할 때 `parentDom.removeChild(fiber.dom)` 에서 null 에러가 발생했다.

### 원인

fiber.dom이 null인 경우가 있다. function component같이 DOM을 직접 가지지 않는 fiber 타입이 있을 수 있고, 이 때는 자식 fiber를 재귀적으로 찾아가서 실제 dom을 가진 fiber를 제거해야 한다.

### 해결

commitDeletion 함수를 분리하고, fiber.dom이 있으면 바로 removeChild, 없으면 fiber.child로 재귀한다. 현재 이 프로젝트에서 dom 없는 fiber는 발생하지 않지만, 03-hooks-and-events에서 function component가 추가되면 이 로직이 필요해진다.
