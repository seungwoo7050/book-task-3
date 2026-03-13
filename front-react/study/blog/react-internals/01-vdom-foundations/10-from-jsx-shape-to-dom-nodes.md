# From JSX Shape To DOM Nodes

React internals를 공부할 때 가장 쉽게 흐려지는 순간은 JSX를 너무 빨리 당연한 것으로 받아들이는 때다. `<div>Hello</div>` 같은 표현은 보기에는 간단하지만, 런타임이 다루려면 결국 type과 props와 children을 가진 데이터 구조로 바뀌어야 한다. 이 프로젝트는 바로 그 가장 낮은 층을 직접 만드는 단계다.

흥미로운 건 여기서부터 벌써 다음 단계의 복잡도가 결정된다는 점이다. child shape를 애매하게 남겨 두면 나중의 diff와 patch도 계속 예외 처리를 떠안아야 한다. 반대로 입력을 초기에 정규화해 두면, 아래 단계는 훨씬 단순한 규칙 위에서 움직일 수 있다.

그래서 이 프로젝트의 중심은 "렌더러를 빨리 만든다"가 아니라 "무엇을 같은 shape로 취급할 것인가"에 있다. 텍스트도 element도 같은 VNode 인터페이스를 가지게 만들겠다는 선택이 바로 그 출발점이었다.

## 구현 순서를 먼저 짚으면

- `createElement()`에서 primitive child를 모두 `TEXT_ELEMENT`로 감싸 입력 shape를 통일했다.
- `createDom()`, `updateDom()`, `render()`를 나눠 DOM 생성과 업데이트 정책을 분리했다.
- 마지막에는 `npm run verify:vdom`으로 27개 테스트와 typecheck를 통과시켜 foundation boundary를 고정했다.

## foundation 단계의 핵심은 render가 아니라 shape normalization이었다

`createElement()`가 하는 일은 생각보다 단순하지만, 뒤 단계 전체를 결정한다. 문자열이나 숫자를 만날 때마다 나중에 특별 취급하지 않도록, 처음부터 `TEXT_ELEMENT`라는 VNode shape로 감싸 버린다.

```ts
export function createElement(
  type: string,
  props: Record<string, any> | null,
  ...children: any[]
): VNode {
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

이 한 번의 정규화가 중요한 이유는 명확하다. 이후 단계는 child가 문자열인지 숫자인지, 아니면 이미 element인지 다시 묻지 않는다. 모두 같은 `type + props.children` 인터페이스를 가진 노드로 취급할 수 있다.

`docs/concepts/jsx-to-vnode.md`가 primitive child를 굳이 별도 섹션으로 설명하는 것도 같은 이유다. foundation 단계의 가장 값진 선택은 런타임이 나중에 덜 고민하게 만드는 선택이다.

## DOM 생성과 업데이트를 나누자 렌더러의 성격이 분명해졌다

다음 전환점은 `createDom()`과 `updateDom()`을 분리한 것이다. 노드를 만들고, 기존 props와 새 props를 비교해 바꾸고, 이벤트는 별도로 제거/재등록한다. 이 흐름이 나중의 diff/patch 단계가 기대할 최소 정책이 된다.

```ts
Object.keys(prevProps)
  .filter(isEvent)
  .filter((key) => !(key in nextProps) || isNew(prevProps, nextProps)(key))
  .forEach((name) => {
    const eventType = name.toLowerCase().substring(2);
    dom.removeEventListener(eventType, prevProps[name]);
  });

Object.keys(nextProps)
  .filter(isProperty)
  .filter(isNew(prevProps, nextProps))
  .forEach((name) => {
    (dom as any)[name] = nextProps[name];
  });
```

이 코드가 보여 주는 건 렌더러의 본질이 `appendChild`가 아니라 update policy라는 사실이다. 어떤 값은 속성 대입으로 충분하고, 어떤 값은 예전 listener를 떼고 새 listener를 다시 달아야 한다. foundation 단계에서 이 차이를 분리해 둬야 다음 단계에서 patch가 DOM-safe한 순서를 가질 수 있다.

실제 `render()`가 재귀적으로 child를 append하는 구조도 같은 맥락에서 읽힌다. 아직은 순진한 렌더러지만, 바로 그 단순함 덕분에 다음 단계에서 무엇이 부족한지 선명하게 드러난다.

```ts
export function render(element: VNode, container: HTMLElement | Text): void {
  const dom = createDom(element);

  if (element.props.children) {
    element.props.children.forEach((child) => {
      render(child, dom);
    });
  }

  container.appendChild(dom);
}
```

## 마지막에는 "여기까지가 foundation"이라는 경계를 잠갔다

이 프로젝트의 검증은 꽤 넓다. `element.test.ts`는 child shape 정규화를, `dom-utils.test.ts`는 property set/remove와 event listener 교체를, 마지막에는 nested render를 확인한다.

```bash
cd study
npm run verify:vdom
```

2026-03-13 replay 기준으로 `vitest` 27개 테스트가 전부 통과했고, `tsc --noEmit`도 성공했다. 이 숫자가 의미하는 건 완성도가 아니라 경계다. 지금의 foundation은 어디까지 책임지고, 아직 diff도 hook도 scheduler도 없다는 사실을 테스트로 분명히 남겨 둔 것이다.

이게 중요한 이유는 다음 단계가 바로 이 foundation 패키지를 소비하기 때문이다. `@front-react/vdom-foundations`라는 이름 자체가 "더 위 단계가 가져다 쓸 최소 surface"라는 선언이 된다.

## 무엇이 아직 남았는가

아직 이 렌더러는 전체 트리를 동기적으로 다시 만든다. 무엇이 바뀌었는지 계산하지도 않고, DOM을 언제 건드릴지도 통제하지 않는다. 하지만 foundation 단계에서는 바로 그 결핍이 오히려 중요하다. 지금 없는 것이 분명해야 다음 단계의 목표도 분명해지기 때문이다.

다음 프로젝트의 질문은 자연스럽다. old tree와 new tree가 있을 때, 무엇이 달라졌는지 어떻게 계산할 것인가. `02-render-pipeline`은 바로 그 지점에서 render와 commit을 분리하기 시작한다.
