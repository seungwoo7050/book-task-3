# 01 VDOM Foundations development timeline

`01-vdom-foundations`를 읽을 때 중요한 건 "React처럼 보이는가"가 아니라 "다음 단계를 떠받칠 최소 shape를 세웠는가"다. `study/react-internals/01-vdom-foundations`의 adapted problem, `ts/src/element.ts`, `ts/src/dom-utils.ts`, tests, 그리고 2026-03-13 재검증 결과를 따라가면 이 프로젝트가 왜 일부러 작고 엄격한 패키지로 남아 있는지 보인다.

## 구현 순서 요약

1. adapted/original README로 이 단계가 어디까지를 VDOM foundation으로 볼지 먼저 고정했다.
2. `createTextElement`와 `createElement`로 모든 child를 같은 VNode shape로 정규화했다.
3. `createDom`, `updateDom`, `render`로 DOM reflection을 붙인 뒤 verify와 typecheck로 package contract를 닫았다.

## 2026-03-08 / Phase 1 - adapted 범위와 package contract를 먼저 고정한다

- 당시 목표:
  이 단계가 diff 이전의 foundation이라는 점을 분명히 한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `problem/original/README.md`, `ts/README.md`
- 처음 가설:
  internals 트랙이라서 reconciliation이 바로 나올 것 같지만, README를 읽으면 이 단계는 의도적으로 `createElement`, `createDom`, `render`까지만 다룬다.
- 실제 진행:
  adapted README와 original README를 나란히 읽고, 다음 단계가 이 패키지를 import해 쓰도록 export 경계를 먼저 고정했다.

CLI:

```bash
$ git log --reverse --stat -- study/react-internals/01-vdom-foundations | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... problem/original/README.md
... ts/src/element.ts
... ts/src/dom-utils.ts
... ts/tests/element.test.ts
```

검증 신호:

- source tree만 봐도 이 단계가 adapted problem, implementation, tests를 한 패키지로 닫고 있다는 점이 드러났다.

핵심 코드:

```ts
export function createTextElement(text: string): VNode {
  return {
    type: "TEXT_ELEMENT",
    props: {
      nodeValue: text,
      children: [],
    },
  };
}
```

왜 이 코드가 중요했는가:

이 프로젝트의 첫 전환점은 "모든 child를 같은 shape로 만든다"는 결정을 명시한 지점이다. primitive child가 제각각 남아 있으면 이후의 diff나 patch는 출발도 못 한다. `TEXT_ELEMENT`는 그 불균일성을 가장 작은 비용으로 없애는 규칙이다.

새로 배운 것:

- Virtual DOM의 가치 일부는 추상화 그 자체보다, 뒤 단계가 기대할 수 있는 uniform shape를 강제하는 데 있다.

다음:

- `createElement`가 이 규칙을 전체 tree에 어떻게 적용하는지 본다.

## 2026-03-08 / Phase 2 - VNode shape를 tree 전체로 퍼뜨린다

- 당시 목표:
  JSX-like 호출이 어떤 데이터 구조로 번역되는지 닫는다.
- 변경 단위:
  `ts/src/element.ts`, `ts/tests/element.test.ts`
- 처음 가설:
  `type`와 `props`만 있으면 충분해 보이지만, children을 배열로 강제하지 않으면 tree traversal이 흔들릴 거라고 봤다.
- 실제 진행:
  `createElement`가 `children.map`으로 모든 child를 object 또는 `TEXT_ELEMENT`로 바꾸는 지점을 중심으로 읽었다.

CLI:

```bash
$ rg -n 'createTextElement|createElement' \
  study/react-internals/01-vdom-foundations/ts/src/element.ts
study/.../element.ts:3:export function createTextElement(text: string): VNode
study/.../element.ts:13:export function createElement(
```

검증 신호:

- `element.ts` 자체가 짧아서 이 단계의 데이터 모델이 얼마나 의도적으로 작게 설계됐는지 드러났다.

핵심 코드:

```ts
export function createElement(type: string, props: Record<string, any> | null, ...children: any[]): VNode {
  return {
    type,
    props: {
      ...(props ?? {}),
      children: children.map((child) =>
        typeof child === "object" ? child : createTextElement(String(child)),
      ),
    },
  };
}
```

왜 이 코드가 중요했는가:

`children.map` 한 줄이 이 프로젝트 전체를 떠받친다. object child는 그대로 두고 primitive child만 text vnode로 감싸는 방식 덕분에, 아래 단계들은 child shape를 매번 분기하지 않아도 된다.

새로 배운 것:

- minimal runtime에서도 invariants를 먼저 세우면 후속 알고리즘 복잡도가 크게 줄어든다.

다음:

- 이 VNode가 실제 DOM mutation으로 어떻게 연결되는지 본다.

## 2026-03-08 to 2026-03-13 / Phase 3 - DOM reflection과 verify로 foundation을 닫는다

- 당시 목표:
  VNode shape가 실제 DOM 생성과 prop/event 반영으로 이어지는 경로를 닫는다.
- 변경 단위:
  `ts/src/dom-utils.ts`, `ts/tests/dom-utils.test.ts`, `tsconfig.json`
- 처음 가설:
  VNode 생성만 맞으면 끝날 것 같지만, prop/event 반영 규칙까지 정리되지 않으면 foundation package라고 부르기 어렵다고 봤다.
- 실제 진행:
  `createDom`, `updateDom`, `render`를 읽고, 2026-03-13에 `npm run verify --workspace @front-react/vdom-foundations`를 다시 실행해 vitest `27 passed`와 typecheck 통과를 고정했다.

CLI:

```bash
$ rg -n 'createDom|updateDom|render' \
  study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts
study/.../dom-utils.ts:18:export function createDom(vnode: VNode)
study/.../dom-utils.ts:29:export function updateDom(
study/.../dom-utils.ts:65:export function render(element: VNode, container: HTMLElement | Text)

$ cd study
$ npm run verify --workspace @front-react/vdom-foundations
Test Files  2 passed (2)
Tests  27 passed (27)
> tsc --noEmit
```

검증 신호:

- `27 passed`는 foundation package가 data shape와 DOM reflection을 충분히 검증하고 있다는 신호였다.
- typecheck 통과가 다음 단계 패키지 import contract를 현재 시점에도 보장해 줬다.

핵심 코드:

```ts
export function updateDom(dom: HTMLElement | Text, prevProps: Record<string, any>, nextProps: Record<string, any>): void {
  Object.keys(prevProps).filter(isEvent).forEach((name) => {
    const eventType = name.toLowerCase().substring(2);
    dom.removeEventListener(eventType, prevProps[name]);
  });
  Object.keys(nextProps).filter(isEvent).forEach((name) => {
    const eventType = name.toLowerCase().substring(2);
    dom.addEventListener(eventType, nextProps[name]);
  });
}
```

왜 이 코드가 중요했는가:

이 블록이 foundation package를 단순 tree printer가 아니라 "DOM과 상호작용하는 최소 runtime"으로 바꾼다. prop와 event reflection 규칙이 있어야 다음 단계의 diff/patch가 무엇을 비교하고 무엇을 commit해야 하는지도 설명된다.

새로 배운 것:

- foundation 단계에서 중요한 건 완성도가 아니라 후속 단계가 전제로 삼을 수 있는 규칙의 명시성이다.

다음:

- 최소 DOM 변경 계산과 render/commit 분리는 다음 단계 `02-render-pipeline`에서 다룬다.

## 남은 경계

- diff/patch는 아직 없다.
- scheduler와 render/commit 분리도 아직 없다.
- state, effect, delegated event는 다음 단계 이후에 등장한다.
