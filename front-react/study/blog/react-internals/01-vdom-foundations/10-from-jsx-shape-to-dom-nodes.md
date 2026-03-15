# From JSX Shape To DOM Nodes

이 프로젝트를 다시 읽으면서 가장 중요하게 보였던 건 "가상 DOM"이라는 큰 이름보다, 그 가상이라는 말이 실제로 어디서 시작되고 끝나는가였다. 여기서는 fiber도 없고 diff도 없고 scheduler도 없다. 대신 더 기초적인 질문만 남긴다. JSX-like 호출은 어떤 객체가 되고, 그 객체는 어떤 규칙으로 실제 DOM node가 되는가.

## 첫 번째 고정점은 child를 항상 같은 shape로 만드는 일이다

핵심 시작점은 [`ts/src/element.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/01-vdom-foundations/ts/src/element.ts)다. 여기서 중요한 건 fancy abstraction이 아니라 "children은 항상 배열"이고 "primitive child는 항상 `TEXT_ELEMENT`"라는 규칙이다.

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

이 한 조각이 중요한 이유는 뒤 단계가 child 종류를 다시 분기하지 않아도 되게 만들기 때문이다. 문자열 `"Hello"`든 숫자 `42`든 결국 `TEXT_ELEMENT`가 되므로, renderer는 "VNode를 받는다"라는 가정만 유지하면 된다.

하지만 여기서 React와 갈라지는 경계도 동시에 생긴다. `typeof false !== "object"`이므로 boolean child는 `String(false)`를 거쳐 `"false"` 텍스트 노드가 된다. 반대로 `typeof null === "object"`라서 `null` child는 그대로 children 배열에 남는다. 즉 이 프로젝트의 정규화 규칙은 "primitive는 전부 text로 감싼다"에 가깝지, React의 falsy child filtering과 동일하지는 않다.

테스트도 바로 이 규칙을 잠근다.

- string child는 `TEXT_ELEMENT`
- number child도 `TEXT_ELEMENT`
- nested vnode는 그대로 유지
- `props.children`은 항상 배열

반대로 boolean/null child를 React처럼 special-case하는 테스트는 없다. 이 부재도 현재 범위를 보여 주는 중요한 신호다.

이 정도의 정규화만 있어도 JSX가 "렌더 가능한 데이터 구조"로 바뀌는 첫 문턱은 설명 가능해진다.

## 두 번째 고정점은 DOM 반영 규칙을 `updateDom` 하나에 모으는 일이다

이 프로젝트가 의외로 좋은 이유는 DOM 조작을 여기저기 흩뿌리지 않는다는 점이다. [`ts/src/dom-utils.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts)의 `updateDom()`이 property와 event 규칙을 한곳에 모아 둔다.

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

여기서 핵심은 두 가지다.

- `children`은 property set에서 제외한다.
- event listener는 "없어졌거나 바뀐 것 제거 -> 새 것 추가" 순서로 처리한다.

이 규칙 덕분에 `createDom()`은 단순히 node를 만들고 `updateDom(dom, {}, vnode.props)`만 호출하면 된다. DOM 생성과 DOM 갱신의 경계가 여기서 처음 만들어지는 셈이다. 아직 diff는 없지만, prop/event 반영 자체는 이미 하나의 규칙으로 추상화됐다.

테스트도 이 부분을 꽤 촘촘하게 고정한다.

- 새 property 설정
- 옛 property 제거
- 변경된 property 교체
- listener 추가/삭제/교체
- `children` key 무시

즉 이 단계의 진짜 성과는 "DOM을 만들었다"가 아니라, DOM을 바꾸는 규칙을 따로 분리해 뒀다는 데 있다.

## 마지막 단계는 render이지만, 아직은 재조정이 아니라 append다

`render()`는 오히려 아주 단순하다.

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

이 구현은 지금 단계의 가능성과 한계를 동시에 보여 준다.

- 가능성: VNode 트리를 실제 DOM 트리로 동기 재귀 변환할 수 있다.
- 한계: 기존 tree와 비교하지 않으므로 매번 새 DOM을 append한다.

테스트에 있는 "same container에 두 번 render하면 paragraph가 두 개 된다"는 시나리오가 바로 이 경계를 드러낸다. 이건 버그라기보다, 아직 diff/commit 분리를 도입하기 전 단계라는 사실을 아주 정직하게 보여 주는 신호다.

그래서 이 프로젝트를 "React clone 1단계"로 읽기보다, render pipeline의 가장 앞단 shape를 고정하는 작업으로 읽는 편이 맞다. JSX-like 입력이 객체가 되고, 그 객체가 DOM으로 바뀌는 건 성공했다. 하지만 무엇을 유지하고 무엇만 바꿀지는 아직 모른다.

## 이번 검증은 shape와 경계를 둘 다 확인했다

이번 Todo에서 다시 돌린 검증은 아래 셋이다.

```bash
npm run test:vdom
npm run typecheck:vdom
npm run verify:vdom
```

재실행 결과는 다음과 같았다.

- `element.test.ts`와 `dom-utils.test.ts` 포함 총 27개 테스트 통과
- `tsc --noEmit` 통과
- verify 전체 통과

이 결과가 의미하는 건 단순한 green check가 아니다. child 정규화, DOM prop/event 반영, 동기 재귀 render라는 최소 약속이 지금은 안정적으로 잠겨 있다는 뜻이다.

## 그래서 이 프로젝트의 진짜 역할은 다음 단계를 위한 shape 고정이다

여기에는 state도 없고 hook도 없고 diff도 없다. 그 대신 더 앞단의 질문을 해결한다. "렌더 가능한 트리란 무엇인가"와 "그 트리는 어떤 규칙으로 DOM이 되는가"다.

다음 단계인 `02-render-pipeline`이 의미를 가지려면, 바로 이 최소 shape가 먼저 고정돼 있어야 한다. 비교 대상이 되는 tree, prop update 규칙, append-only 현재 동작이 이미 선명해야 그다음에야 diff와 commit 분리를 설명할 수 있기 때문이다.
