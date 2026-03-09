# 회고 — render pipeline을 만들면서 배운 것

## 가장 중요한 깨달음: 계산과 반영의 분리

이 프로젝트 전체를 관통하는 하나의 원칙이 있다면, "무엇이 바뀌었는지 계산하는 것"과 "바뀐 것을 DOM에 반영하는 것"을 분리하라는 것이다.

diff/patch 구조에서는 이 분리가 모듈 단위로 표현된다. diff.ts는 Patch 객체를 반환할 뿐 DOM을 건드리지 않는다. patch.ts가 그 Patch를 받아 DOM을 바꾼다. 두 모듈 사이에 데이터(Patch 배열)가 흐르고, 그게 전체 rendering의 경계다.

fiber 구조에서는 이 분리가 phase로 표현된다. render phase에서 fiber tree를 만들며 effect tag를 붙이고, commit phase에서 effect tag에 따라 DOM을 조작한다. 중간에 멈출 수 있는 이유도 이 분리 때문이다 — render phase에서는 DOM을 안 건드리니까 중단해도 사용자는 불완전한 화면을 보지 않는다.

## diff/patch와 fiber를 함께 만들어 본 효과

처음에는 왜 두 접근을 한 프로젝트에서 다루는지 의문이었다. 하나만 골라도 되지 않을까.

결론적으로 둘 다 만든 게 맞았다. diff/patch는 "변경 계산"이라는 순수 함수적 사고를 연습하게 해 줬다. 입력(oldTree, newTree)을 받아 출력(Patch[])을 반환한다. 중간 상태가 없다. 테스트하기 쉽다.

fiber는 "실행 모델"로의 전환을 보여 줬다. linked list, 상태 변수, work loop — 함수보다 프로세스에 가까운 사고다. 같은 문제(트리 비교와 DOM 업데이트)를 다른 구조로 풀면서, 어떤 구조가 어떤 종류의 확장에 유리한지 체감할 수 있었다.

React가 fiber를 선택한 이유도 여기서 드러난다. diff/patch는 깔끔하지만, "중간에 멈추고 우선순위 높은 작업을 먼저 하겠다"라는 요구에는 대응하기 어렵다. fiber는 작업을 쪼갤 수 있으므로 그게 가능하다.

## linked list의 위력과 어색함

fiber에서 child/sibling/parent 포인터로 트리를 표현하는 건 배열 기반 사고와 완전히 다르다. 처음에는 `children: Fiber[]`로 하면 안 되나 생각했다.

답은 "순회를 중단했다가 이어가려면 배열 인덱스보다 포인터가 낫다"다. 현재 fiber에서 sibling으로, sibling이 없으면 parent로, parent의 sibling으로 — 이 순회는 반복문 하나로 되고, "다음에 처리할 fiber"라는 커서 하나만 있으면 된다.

```typescript
if (fiber.child) return fiber.child;
let nextFiber = fiber;
while (nextFiber) {
  if (nextFiber.sibling) return nextFiber.sibling;
  nextFiber = nextFiber.parent;
}
return null;
```

재귀 없이 트리를 순회한다. 이게 requestIdleCallback 같은 cooperative scheduling과 어울리는 이유다.

## alternate 패턴의 의미

fiber에서 `alternate`는 "이전 commit에서의 나"를 가리킨다. reconcileChildren에서 old fiber와 new element를 비교할 때, UPDATE fiber의 alternate에 old fiber를 연결하고, dom은 old fiber에서 가져온다.

이 구조의 효과는 commitWork에서 드러난다. UPDATE일 때 `fiber.alternate?.props`와 `fiber.props`를 비교해서 updateDom을 호출한다. alternate가 없으면 이전 상태를 알 방법이 없다. 트리를 통째로 비교하는 대신, 개별 fiber가 "나의 이전 버전"을 기억하고 있다.

## 테스트에서 배운 것

scheduler 테스트가 가장 인상적이었다. 세 가지를 순서대로 검증한다:

1. render 직후 container가 비어 있음 → render phase에서 DOM 안 바꿈
2. flushSync 후 DOM에 노드가 있음 → commit phase가 DOM을 바꿈
3. interrupted work 후 flushSync → 중단 후 재개해도 결과가 같음

특히 세 번째 테스트에서 `timeRemaining()`을 조작해서 "첫 번째 fiber만 처리하고 멈추는" 상황을 만드는 것이 좋았다. 실제 브라우저의 requestIdleCallback 동작을 테스트 환경에서 재현하는 방법을 배웠다.

## 범위 제한의 교훈

keyed diff에서 reorder(move) 패치를 일부러 빼고 remove + create로 대체한 것, priority lanes를 넣지 않은 것 — 이런 제한이 오히려 학습에 도움이 됐다. move 패치를 넣으면 "인접 순열 대비 최소 이동"을 계산하는 알고리즘이 필요한데, 그건 diff의 본질이 아니라 최적화다.

"render와 commit을 분리한다"라는 한 문장을 코드로 보여 주려면, 코드가 적을수록 좋다. 이 프로젝트에서 가장 많이 한 설계 결정은 "이건 빼자"였다.

## 다음 단계를 위한 열린 질문

fiber 구조가 만들어졌으니, 여기에 상태(hook)를 얹으면 어떻게 되는가? performUnitOfWork가 fiber를 처리할 때 hook slot을 읽고, setState가 re-render를 trigger하면 wipRoot를 다시 설정하는 방식이 될 것이다.

이것이 `03-hooks-and-events`로 이어지는 질문이다. fiber가 reconciliation의 단위이면서 동시에 상태의 단위가 되는 순간, React의 함수 컴포넌트 모델이 보이기 시작한다.
