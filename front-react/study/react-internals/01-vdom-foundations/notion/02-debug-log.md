# 디버그 기록: VDOM 구현에서 만난 함정들

## 이벤트 핸들러 중복 등록

`updateDom()`에서 prop을 순회할 때, 이벤트 prop(onClick 등)과 일반 prop을 구분하지 않고 처리했더니, 같은 핸들러가 두 번 등록되는 문제가 생겼다. `button.click()`을 한 번 호출했는데 핸들러가 두 번 실행되는 것이다.

원인은 이전 이벤트를 제거하기 전에 새 이벤트를 추가해서였다. 이전 핸들러가 남아 있는 상태에서 새 핸들러가 추가되니 두 개가 공존했다.

해결은 updateDom의 처리 순서를 고정하는 것이었다: **이전 이벤트 제거 → 이전 prop 제거 → 새 prop 설정 → 새 이벤트 추가**. 이 순서를 지키면 항상 깨끗한 상태에서 새 핸들러가 등록된다.

## TEXT_ELEMENT를 빼먹은 초기 구현

처음에는 `createElement`에서 문자열 child를 그대로 배열에 넣었다. `children: ["Hello", vnode]` 같은 형태. 이러면 `render()`에서 child를 순회할 때, 문자열에 대해 `child.type`을 참조하면 `undefined`가 되어 에러가 발생한다.

모든 child를 VNode로 정규화해야 렌더러가 uniform하게 처리할 수 있다. `createTextElement()`를 만들고, primitive child는 반드시 이 함수를 거치게 수정했다.

이 경험에서 **React가 왜 internal하게 text를 별도로 처리하는지**를 이해하게 됐다.

## className vs class 혼동

HTML에서는 `class` 속성을 쓰지만, DOM property로는 `className`을 써야 한다. `updateDom()`이 property assignment(`(dom as any)[name] = value`)를 사용하므로, `className`이 맞다.

테스트에서 `createElement("div", { class: "box" })`로 작성했다가 class가 적용되지 않는 문제를 겪었다. `className`으로 바꾸니 해결됐다. React도 `className`을 강제하는 이유가 이것이다 — JSX는 DOM property를 사용한다.

## children 키를 일반 prop으로 처리한 실수

`updateDom()`에서 모든 prop을 순회하면서 DOM에 반영하는데, `children`도 그냥 반영해 버리는 실수가 있었다. `div.children = [vnode1, vnode2]` 같은 할당이 되어 예상치 못한 동작이 발생했다.

`isProperty` 헬퍼에서 `key !== "children"`을 체크하도록 수정. children은 `render()`의 재귀에서 별도로 처리되므로, `updateDom()`에서는 건드리면 안 된다.

## 깊은 중첩에서 appendChild 순서

`render()`가 재귀적으로 children을 처리한 뒤 현재 노드를 parent에 append하는 구조인데, 처음에는 append를 먼저 하고 children을 재귀 처리했다. 결과적으로는 같은 DOM 트리가 만들어지지만, append를 먼저 하면 **불완전한 DOM이 화면에 잠깐 보이는** 문제가 생길 수 있다.

children을 먼저 처리하고 마지막에 append하면, 완성된 서브트리가 한 번에 붙으므로 깜빡임이 없다. 이 순서는 React의 commit phase 개념과 같은 원리다 — 준비가 다 되면 한 번에 반영한다.
