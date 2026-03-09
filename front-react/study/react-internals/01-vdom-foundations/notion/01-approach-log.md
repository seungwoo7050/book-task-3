# 접근 과정: UI를 데이터로 만들다

## 타입 설계로 시작하기

가장 먼저 한 것은 `VNode`의 타입을 정의하는 일이었다. React에서 JSX가 결국 만들어 내는 것은 무엇인가? `type`과 `props`를 가진 plain object다.

```typescript
interface VNode {
  type: string | Function;
  props: {
    [key: string]: any;
    children: VNode[];
  };
}
```

이 타입을 정의하면서 두 가지를 의식적으로 결정했다.

첫째, `type`에 `Function`을 포함시켰다. 지금 당장은 문자열(HTML 태그)만 다루지만, 나중에 함수 컴포넌트를 지원하려면 이 자리에 함수가 올 수 있어야 한다. 미리 자리를 만들어 두는 것이다.

둘째, `children`을 `props` 안에 넣었다. React도 이렇게 한다. children은 특별한 존재가 아니라 "그냥 또 다른 prop"이다. 이 설계 덕분에 `createElement`가 단순해진다.

## createElement: JSX의 목표 지점

JSX `<div id="root"><span>Hello</span></div>`는 다음과 같은 함수 호출로 변환된다:

```typescript
createElement("div", { id: "root" }, createElement("span", null, "Hello"))
```

이 함수를 구현하면서 핵심적인 판단을 두 가지 내렸다.

**첫째, null props를 빈 객체로 처리한다.** `createElement("div", null)`이 호출되면, props를 `{}`로 만들고 `children: []`을 추가한다. 이렇게 하면 이후 코드에서 props의 존재 여부를 매번 확인하지 않아도 된다.

**둘째, primitive child를 TEXT_ELEMENT VNode로 감싼다.** 문자열 "Hello"나 숫자 42는 `type`과 `props`가 없다. 렌더러가 모든 child를 `VNode` 인터페이스로 균일하게 순회하려면, primitive도 같은 구조로 변환해야 한다. `createTextElement()`가 이 일을 맡는다.

이 정규화(normalization)가 있어야, 렌더링 코드에서 "child의 type이 무엇인가"만 확인하면 모든 자식을 처리할 수 있다.

## createDom과 updateDom: 실제 DOM으로 내보내기

VNode를 만들었으면 실제 DOM으로 바꿔야 한다. 이 과정을 `createDom()`과 `updateDom()`으로 나눴다.

**`createDom()`은 VNode type에 따라 DOM 노드를 생성한다.** TEXT_ELEMENT면 `createTextNode()`, 그 외면 `createElement()`. 생성 직후 `updateDom()`을 호출해서 props와 이벤트를 반영한다.

**`updateDom()`은 prop 변경을 네 단계로 처리한다:**

1. 이전 이벤트 리스너 제거 (바뀌었거나 사라진 것)
2. 사라진 일반 prop 제거 (빈 문자열로 초기화)
3. 새로 추가되거나 변경된 일반 prop 설정
4. 새 이벤트 리스너 추가

이 순서가 중요한 이유가 있다. 이벤트를 먼저 정리하고 새로 달아야 핸들러가 중복 등록되지 않고, prop을 먼저 지우고 새로 설정해야 오래된 값이 남지 않는다. 처음에는 순서를 신경 쓰지 않았다가 이벤트가 두 번 발생하는 버그를 겪은 뒤에, 이 순서를 의식적으로 고정했다.

## render: 재귀로 트리를 펼치다

`render()` 함수는 놀라울 정도로 단순하다.

1. `createDom()`으로 현재 VNode의 DOM 노드를 만든다
2. children이 있으면 각 child에 대해 `render()`를 재귀 호출한다
3. 만든 DOM 노드를 parent container에 `appendChild()`한다

이 세 줄이 전체 VDOM → DOM 변환의 핵심이다. 하지만 이 단순함이 곧 한계이기도 하다. 재귀가 깊어지면 메인 스레드가 오래 점유되고, 이전 렌더 결과와 비교하지 않으니 매번 처음부터 다시 만든다.

이 한계를 체감하면서 "왜 React가 reconciliation과 fiber를 발명했는가"를 이해할 기반이 생겼다.

## isEvent / isProperty: 작은 유틸의 큰 효과

`updateDom`에서 prop을 이벤트와 일반 속성으로 분류하는 헬퍼가 있다.

- `isEvent`: key가 "on"으로 시작하면 이벤트 (onClick, onInput 등)
- `isProperty`: children이 아니고 이벤트도 아니면 일반 속성

이 분류가 있어야 `addEventListener`와 property 설정을 깔끔하게 나눌 수 있다. 처음에는 한 루프에서 모든 걸 처리하려 했는데, 코드가 복잡해지고 분기가 늘어나서 분리했다.
