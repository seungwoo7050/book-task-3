# 문제 인식 — 왜 hooks와 events가 필요한가

## render pipeline 이후의 빈 자리

`02-render-pipeline`에서 diff/patch와 fiber 기반 reconciliation을 만들었다. render phase에서 변경을 계산하고, commit phase에서 DOM에 반영하는 흐름까지 완성했다. 하지만 한 가지가 없다 — 컴포넌트 자체가 상태를 가지는 방법이 없다.

현재까지의 파이프라인은 "외부에서 새 VNode 트리를 넣으면 비교해서 반영한다"가 전부다. 컴포넌트가 스스로 "나는 count가 3이다"라고 말하고, 버튼이 눌리면 4로 바꾸고, 그에 따라 다시 그리는 — 이 루프가 없다.

이벤트도 마찬가지다. DOM에 직접 addEventListener를 다는 건 가능하지만, 리렌더링할 때마다 listener를 다시 달아야 하고, 이전 것을 지워야 한다. 컴포넌트가 사라졌다가 다시 나타나면? handler가 어떤 노드에 붙어 있는지 추적해야 한다.

## 이 프로젝트의 세 가지 축

이 문제를 세 축으로 분해했다.

**1. Hook Slot — 함수 컴포넌트의 상태**

함수 컴포넌트는 클래스와 달리 인스턴스가 없다. 호출할 때마다 새로 실행된다. 그런데 상태를 유지해야 한다. React의 해법은 "호출 순서로 인덱싱되는 slot array"다. 첫 번째 useState가 slot[0], 두 번째가 slot[1]. 이 순서가 바뀌면 깨진다 — 이것이 hooks 규칙의 실체다.

**2. Effect Lifecycle — 부수 효과 관리**

렌더링과 부수 효과는 분리되어야 한다. render에서 effect를 바로 실행하면 DOM이 아직 commit 전이다. 그래서 effect는 "등록만 하고, commit 후에 실행"한다. 이전 effect의 cleanup을 먼저 실행하고, 새 effect를 실행한다. 컴포넌트가 사라지면 unmount cleanup이 돌아간다.

**3. Delegated Events — 이벤트 위임**

각 DOM 노드에 listener를 다는 대신, root container에 이벤트 타입별로 하나만 등록한다. 이벤트가 발생하면 target에서 root까지 올라가면서 handler를 찾고 실행한다. 이 방식의 장점은 리렌더링 후에도 listener를 다시 달 필요가 없다는 것이다 — handler 정보는 runtime이 관리하는 메타데이터에 있으니까.

## 의존 구조

이 프로젝트는 `@front-react/render-pipeline`을 의존으로 참조한다. createElement, diff, applyPatches, resetScheduler를 가져와서 쓴다. diff/patch를 다시 만들지 않고 이전 프로젝트의 구현을 그대로 활용한다.

## 범위와 한계

다루는 것:
- useState의 slot array 모델과 재렌더
- hook count 변화 감지 (invariant 위반 시 에러)
- useEffect의 setup/cleanup/deps 비교
- unmount 시 cleanup
- delegated event bubbling과 stopPropagation
- event → state update → rerender → effect의 통합 흐름

다루지 않는 것:
- useReducer, useMemo, useCallback, useRef
- layout effect, insertion effect
- concurrent rendering과 priority
- 다중 root

이 프로젝트에서 만드는 것은 "최소 runtime"이다. useState와 useEffect 두 개의 hook, delegated event 하나의 dispatch 모델 — 이것만으로 React의 runtime loop가 어떻게 돌아가는지 설명할 수 있다.
