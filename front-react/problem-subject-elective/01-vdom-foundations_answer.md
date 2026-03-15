# 01-vdom-foundations 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 props.children은 항상 배열이어야 한다, primitive child는 TEXT_ELEMENT로 감싸야 한다, DOM property와 event listener 반영은 updateDom 규칙으로 통일한다를 한 흐름으로 설명하고 검증한다. 핵심은 `isEvent`와 `isProperty`, `isNew` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- props.children은 항상 배열이어야 한다.
- primitive child는 TEXT_ELEMENT로 감싸야 한다.
- DOM property와 event listener 반영은 updateDom 규칙으로 통일한다.
- 첫 진입점은 `../study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts`이고, 여기서 `isEvent`와 `isProperty` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts`: `isEvent`, `isProperty`, `isNew`, `isGone`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/01-vdom-foundations/ts/src/element.ts`: `createTextElement`, `createElement`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/01-vdom-foundations/ts/src/index.ts`: 핵심 구현을 담는 파일이다.
- `../study/react-internals/01-vdom-foundations/ts/src/types.ts`: 핵심 구현을 담는 파일이다.
- `../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts`: `createDom`, `updateDom`, `render`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/01-vdom-foundations/problem/code/element.ts`: `createTextElement`, `createElement`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/react-internals/01-vdom-foundations/ts/tests/dom-utils.test.ts`: `createDom`, `should create a Text node for TEXT_ELEMENT`, `should create an HTMLElement for a tag type`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/react-internals/01-vdom-foundations/ts/tests/element.test.ts`: `createTextElement`, `should create a text VNode with type TEXT_ELEMENT`, `should handle empty strings`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts`와 `../study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `createDom` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run test:vdom && npm run typecheck:vdom && npm run verify:vdom`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run test:vdom && npm run typecheck:vdom && npm run verify:vdom
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/01-vdom-foundations && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/01-vdom-foundations && npm run verify
```

- `../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `createDom`와 `should create a Text node for TEXT_ELEMENT`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run test:vdom && npm run typecheck:vdom && npm run verify:vdom`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/element.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/index.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/types.ts`
- `../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts`
- `../study/react-internals/01-vdom-foundations/problem/code/element.ts`
- `../study/react-internals/01-vdom-foundations/ts/tests/dom-utils.test.ts`
- `../study/react-internals/01-vdom-foundations/ts/tests/element.test.ts`
- `../study/react-internals/01-vdom-foundations/problem/script/Makefile`
- `../study/react-internals/01-vdom-foundations/tsconfig.json`
