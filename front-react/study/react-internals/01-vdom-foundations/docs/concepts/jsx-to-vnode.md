# JSX 에서 VNode 까지

`01-vdom-foundations`에서 구현하는 `createElement`는 JSX 변환의 가장 단순한 목표 지점이다.

## 핵심 흐름

```jsx
<div id="root">
  <span>Hello</span>
</div>
```

위 표현은 개념적으로 아래 호출로 바뀐다.

```ts
createElement(
  "div",
  { id: "root" },
  createElement("span", null, "Hello"),
);
```

이 호출이 다시 아래 같은 plain object 트리로 정규화된다.

```ts
{
  type: "div",
  props: {
    id: "root",
    children: [
      {
        type: "span",
        props: {
          children: [
            {
              type: "TEXT_ELEMENT",
              props: { nodeValue: "Hello", children: [] },
            },
          ],
        },
      },
    ],
  },
}
```

## 왜 text wrapper가 필요한가

문자열과 숫자는 `type`과 `props`를 갖지 않는다. 렌더러가 모든 child를 같은 인터페이스로 순회하려면 primitive도 VNode로 감싸야 한다. 이 단계에서는 `"TEXT_ELEMENT"`가 그 역할을 맡는다.

## 이 단계에서 기억할 것

- `props.children`은 항상 배열이다.
- `null` props는 빈 객체로 취급한다.
- primitive child는 `createTextElement`를 거친다.
- 이 구조가 있어야 다음 단계에서 old/new 트리를 비교할 수 있다.

