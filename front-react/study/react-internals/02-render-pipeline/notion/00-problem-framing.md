# 문제 인식 — 왜 render pipeline이 필요한가

## 이전 단계에서 남은 질문

`01-vdom-foundations`에서 VNode를 만들고 DOM으로 한 번에 그리는 흐름까지는 구현했다. createElement로 트리를 구성하고, createDom으로 실제 노드를 만들고, render로 컨테이너에 붙인다. 작동하지만, "다시 그린다"라는 문제 앞에서 한계가 보인다.

트리 전체를 지우고 처음부터 다시 그리는 건 동작하지만 비용이 크다. 어떤 부분이 바뀌었는지 알 수 있으면 바뀐 것만 반영하면 된다. 이 질문이 render pipeline의 출발점이다.

## 두 가지 축: diff/patch와 fiber

문제를 분해하면 두 가지 접근이 보인다.

첫 번째는 **전통적인 diff/patch**다. 두 VNode 트리를 비교해서 차이를 Patch 객체로 표현하고, 그 Patch를 한꺼번에 DOM에 적용한다. 이 방식은 직관적이다. oldTree와 newTree를 받아서 "무엇이 바뀌었는가"를 계산하고, 그 결과를 "어떻게 반영하는가"와 분리한다.

두 번째는 **fiber 기반 reconciliation**이다. 트리를 linked list 형태의 fiber 구조로 바꾸고, 각 fiber를 하나의 work unit으로 취급한다. reconcile 과정에서 old fiber와 new element를 비교하며 PLACEMENT, UPDATE, DELETION 같은 effect tag를 부여하고, commit phase에서 DOM에 반영한다.

이 프로젝트에서 두 접근을 모두 구현하는 이유는, 각각이 설명하는 관점이 다르기 때문이다. diff/patch는 "변경 집합"이라는 데이터를 명시적으로 보여 주고, fiber는 "작업 단위의 분할과 스케줄링"이라는 실행 모델을 보여 준다.

## 이 프로젝트에서 다루는 것과 다루지 않는 것

다루는 범위는 명확하다:
- prop 변경/제거 계산 (diffProps)
- keyed/unkeyed child 비교 (diffChildren)
- CREATE, REMOVE, REPLACE, UPDATE 네 가지 patch 타입
- fiber tree 구성과 effect tag 부여 (reconcileChildren)
- 단위 작업 순회 (performUnitOfWork)
- render/commit phase 분리 (workLoop, commitRoot)
- interrupted work 이후에도 일관된 commit 보장 (flushSync)

의도적으로 뺀 것도 있다:
- keyed reorder 최적화 알고리즘
- priority lanes, concurrent rendering semantics
- class component lifecycle

범위를 줄인 이유는 docs/concepts/diff-and-patch-scope.md에 정리해 두었다. 핵심은, render와 commit을 분리한다는 mental model을 만드는 것이지 patch 종류를 많이 늘리는 것이 아니라는 점이다.

## 선행 조건과 의존 관계

이 프로젝트는 `@front-react/vdom-foundations`를 npm workspace 의존으로 참조한다. VNode 타입, createElement, createDom, updateDom을 모두 01에서 가져온다. 01의 코드가 깨지면 이 프로젝트도 깨진다. 이 의존 관계는 package.json의 dependencies에 명시되어 있다.

## 기대하는 결과

이 프로젝트가 끝나면 "React가 다시 그릴 때 무슨 일이 일어나는가"라는 질문에 두 가지 관점으로 대답할 수 있어야 한다. diff/patch 관점에서는 "변경 집합을 계산하고 한 번에 반영한다"이고, fiber 관점에서는 "작업 단위를 쪼개서 render phase에서 모아 두고 commit phase에서 반영한다"이다. 그리고 두 관점이 결국 같은 문제를 다른 구조로 풀고 있다는 것까지 보여야 한다.
