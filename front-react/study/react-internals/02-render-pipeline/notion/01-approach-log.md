# 접근 기록 — render pipeline 구현 과정

## 타입 설계부터 시작

코드를 짜기 전에 types.ts를 먼저 정의했다. 이 프로젝트에는 두 가지 축이 있으므로 타입도 두 그룹으로 나뉜다.

**diff/patch 축:**
- `PatchType`을 `"CREATE" | "REMOVE" | "REPLACE" | "UPDATE"` 리터럴 유니온으로 정의
- `PropsPatch`로 prop 변경 결과를 `{ set, remove }` 형태로 표현
- `Patch` 인터페이스에 type, index, oldNode, newNode, props, children을 선택 필드로 모아둠

**fiber 축:**
- `EffectTag`를 `"PLACEMENT" | "UPDATE" | "DELETION"`으로 정의
- `Fiber` 인터페이스에 parent/child/sibling linked list 포인터, alternate(이전 fiber 참조), effectTag 포함
- `IdleDeadlineLike`로 `requestIdleCallback` 시그니처를 추상화

VNode과 VNodeProps는 vdom-foundations에서 re-export한다. 새로 만들지 않고 가져오는 것 자체가 01과의 의존을 표현하는 방법이다.

## diff.ts — 변경 집합 계산

diff 모듈은 세 계층으로 구성했다.

**diffProps**: 두 props 객체를 비교한다. children 속성은 제외하고, 값이 달라진 prop은 set에, 새 props에 없는 키는 remove에 넣는다. 단순하지만 이게 prop 업데이트의 전부다.

**diffChildren**: 자식 비교 전략을 선택한다. 모든 자식에 key가 있으면 keyed 전략, 아니면 index 기반 unkeyed 전략을 택한다. 이진 분기다. keyed 전략에서는 old children을 Map에 넣어 O(1) lookup을 쓰고, new children을 순회하며 CREATE/UPDATE를 판단한다. Map에 남으면 REMOVE다. unkeyed에서는 같은 인덱스끼리 비교한다.

**diff**: 최상위 함수. oldNode/newNode 유무에 따라 CREATE, REMOVE를 판단하고, 타입이 다르면 REPLACE, 같으면 diffProps와 diffChildren을 합쳐 UPDATE를 만든다. 재귀 구조이므로 children의 diff 안에서 다시 diff가 호출된다.

keyed diff에서 reorder 최적화(move 연산)를 넣지 않은 것은 의도적이다. remove + create로 처리하면 DOM 조작은 많아지지만 "position이 바뀌면 무슨 patch가 필요한지"가 명확해진다.

## patch.ts — 변경 적용

applyPatches 함수는 Patch 배열을 받아 DOM에 반영한다.

핵심 설계 결정이 하나 있다: **REMOVE를 먼저, 역순으로 처리**한다. 인덱스로 접근하는데 앞에서부터 지우면 뒤쪽 인덱스가 밀린다. 그래서 removals를 분리하고 `sort((a, b) => b.index - a.index)`로 내림차순 정렬한 뒤 처리한다.

각 patch 타입별 처리:
- CREATE: vdom-foundations의 createDom으로 노드를 만들고, `insertBefore`로 해당 인덱스에 삽입. 해당 위치에 기존 노드가 없으면 appendChild 효과.
- REMOVE: `removeChild`로 제거
- REPLACE: `replaceChild`로 교체
- UPDATE: `updateDom`으로 prop을 갱신하고, children patch가 있으면 재귀 적용

createDomTree 헬퍼는 createDom + 자식 재귀 빌드를 합쳐 준다. render(vdom-foundations 것)를 내부적으로 쓸 수도 있지만, 패치 맥락에서는 직접 조립하는 게 의도가 분명하다.

## fiber.ts — 작업 단위 분할

fiber 모듈은 reconciliation을 다른 구조로 풀어낸다.

**reconcileChildren**: old fiber의 linked list와 new elements 배열을 동시에 순회한다. 같은 타입이면 UPDATE fiber를 만들고(dom은 기존 것 재사용, alternate에 old fiber 연결), 다르면 PLACEMENT(새 노드)와 DELETION(삭제 대상)을 만든다. 결과 fiber들을 child/sibling 체인으로 연결한다. 삭제 대상은 별도의 onDelete 콜백으로 수집한다.

**performUnitOfWork**: fiber 하나를 처리하는 함수다. dom이 없으면 vdom-foundations의 createDom으로 생성하고, reconcileChildren을 호출한 뒤, 다음 작업을 반환한다. 순회 순서는 **child → sibling → uncle** — 깊이 우선이되 sibling 체인을 따라가고, sibling이 없으면 parent로 올라가 parent의 sibling을 찾는다.

이 순회 구조가 linked list fiber의 핵심이다. 재귀 호출 없이 반복문으로 트리를 순회할 수 있고, 중간에 멈췄다가 이어갈 수 있다.

## scheduler.ts — render와 commit의 분리

스케줄러는 모듈 레벨 변수 네 개로 상태를 관리한다:
- `nextUnitOfWork`: 다음에 처리할 fiber
- `wipRoot`: work-in-progress root fiber
- `currentRoot`: 마지막으로 커밋된 root
- `deletions`: 삭제 대상 fiber 목록

**render**: wipRoot를 설정하고 nextUnitOfWork를 시작점으로 놓는다. DOM은 건드리지 않는다. 이게 "render phase에서는 DOM을 바꾸지 않는다"의 실체다.

**workLoop**: deadline.timeRemaining()을 확인하며 performUnitOfWork를 반복한다. 시간이 부족하면 멈춘다. 모든 작업이 끝나면(nextUnitOfWork가 null) commitRoot를 호출한다.

**commitRoot**: deletions를 먼저 처리하고, wipRoot.child부터 재귀적으로 commitWork를 호출한다. commitWork는 effect tag에 따라 appendChild, updateDom, removeChild를 실행한다. commit이 끝나면 currentRoot에 wipRoot를 저장하고 wipRoot를 null로 만든다.

**commitDeletion**: fiber에 dom이 있으면 바로 제거하고, 없으면 자식을 재귀 탐색한다. function component처럼 dom 없는 fiber를 대비한 처리다(이 프로젝트에서는 아직 없지만).

**flushSync**: timeRemaining이 항상 Infinity를 반환하는 가짜 deadline으로 workLoop를 호출한다. 테스트에서 동기적으로 전체 작업을 끝내기 위한 도구.

**resetScheduler**: 네 변수를 초기화한다. 테스트 격리용.

## index.ts — 공개 API 설계

모든 구현을 하나의 barrel 파일에서 re-export한다. vdom-foundations에서 가져온 것도 함께 내보내서, 이 패키지만으로 createElement부터 render까지 완결된 API를 제공한다. 다음 프로젝트(03-hooks-and-events)가 이 패키지를 의존으로 참조할 때 필요한 모든 것이 여기에 있다.
