# 회고 — hooks와 events를 만들면서 배운 것

## "왜 hook을 조건부로 호출하면 안 되는가"를 코드로 답할 수 있게 됐다

React를 배울 때 "hook은 조건문 안에서 호출하지 마세요"라는 규칙을 만난다. 규칙을 외울 수는 있지만, 왜 그런지는 slot array를 직접 만들어 봐야 체감된다.

`instances: Map<string, HookSlot[]>`에서 path로 slot array를 찾고, hookIndex로 순서를 센다. 첫 번째 렌더에서 useState, useState, useEffect 순으로 호출하면 slot[0], slot[1], slot[2]에 각각 저장된다. 두 번째 렌더에서 조건문 때문에 useState 하나를 건너뛰면, 원래 slot[2]에 있던 useEffect 정보를 slot[1]에서 useState로 읽으려 한다.

이 프로젝트에서는 hook count가 달라지면 에러를 던지도록 했다. 실제 React도 같은 이유로 이 규칙을 강제한다. "외우는 규칙"이 "구현에서 비롯된 제약"으로 바뀌는 순간이다.

## RuntimeRoot라는 단일 상태 구조의 효과

이전 프로젝트들(vdom-foundations, render-pipeline)은 모듈마다 독립적인 상태를 가졌다. scheduler에 wipRoot와 currentRoot, fiber에서는 별도의 트리 — 각자의 상태가 각자의 파일에 있었다.

이 프로젝트에서는 RuntimeRoot 하나에 모든 것을 모았다. hook slots, pending effects, event listeners, DOM metadata, 렌더링 플래그까지. 처음에는 너무 큰 객체라고 생각했는데, 디버깅할 때 root 하나만 보면 전체 상태를 알 수 있다는 게 큰 장점이었다.

"상태가 흩어지면 상태 간의 관계를 추적하기 어렵다"는 걸 체감했다. React 내부에서 FiberRoot가 왜 그렇게 많은 것을 담고 있는지 이해가 된다.

## 이전 프로젝트의 코드를 실제로 재사용한 순간

이 프로젝트의 commitRoot에서 `diff(root.hostVNode, nextVNode)`를 호출하고, 결과를 `applyPatches(root.container, [patch])`에 넣는다. 이 두 함수는 render-pipeline에서 만든 것이다. 그리고 render-pipeline의 createElement는 vdom-foundations에서 가져온 것이다.

3개의 프로젝트가 실제로 의존 체인을 이루고 있고, 각각 자기 역할만 한다. vdom-foundations는 VNode과 DOM 생성, render-pipeline은 diff/patch, hooks-and-events는 상태 관리와 이벤트 — 이 계층 구조가 코드에서 보인다.

workspace 의존이 단순한 코드 공유가 아니라 "관심사의 계층 분리"라는 걸 깨달았다.

## delegated event가 "마법"이 아님을 확인

React에서 onClick을 쓸 때, 실제로 DOM 노드에 listener가 붙는 게 아니라는 건 알고 있었다. 하지만 "그러면 어떻게 동작하는 거지?"에 대한 답은 없었다.

직접 구현해 보니 놀랍도록 단순하다:
1. container에 event type별로 하나의 listener를 등록
2. WeakMap으로 DOM 노드 → handler 매핑을 유지
3. 이벤트 발생 시 target에서 container까지 parentNode를 따라가며 handler 실행

"framework event system"이라고 하면 거창해 보이지만, 실체는 WeakMap과 while 루프다. stopPropagation도 플래그 하나로 해결된다.

syncDomMeta가 매 commit 후에 WeakMap을 재구축하는 방식이 비효율적으로 보일 수 있다. 하지만 DOM이 바뀌면 노드 참조도 바뀌니까 새로 연결해야 한다. 실제 React는 fiber 자체에 handler를 저장하므로 이 문제가 다른 방식으로 풀린다.

## effect timing이 보여 준 것

"effect는 commit 후에 실행된다"는 문장을 코드로 표현하면:

```
resolveNode (render) → collectUnmounts → commitRoot (DOM mutation) → runEffects
```

이 순서에서 runEffects 위치가 중요하다. DOM이 이미 업데이트된 후이므로, effect 안에서 DOM을 읽으면 최신 상태를 볼 수 있다. 이것이 useEffect의 본질이다 — "render 결과가 화면에 반영된 후에 실행되는 코드."

cleanup이 새 effect 전에 실행된다는 것도 구현하면서 확인했다. lifecycle 배열에 `["setup:0", "cleanup:0", "setup:1"]` 순서가 찍히는 테스트를 보며, React 문서에서 읽었던 "cleanup → setup" 순서를 코드로 확인했다.

## 다음 단계를 위한 관찰

이 프로젝트의 runtime은 학습용 단일 root 모델이다. 하지만 실제 앱에서 useState와 useEffect를 조합하면 얼마나 복잡한 상호작용이 가능한지는 아직 테스트하지 않았다.

다음 프로젝트(04-runtime-demo-app)에서 이 runtime 위에 검색, 페이지네이션, 렌더 메트릭 같은 기능을 만들어야 한다. "최소 runtime이 실제로 쓸 만한가"를 검증하는 단계다.
