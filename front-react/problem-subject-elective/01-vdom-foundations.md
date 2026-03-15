# 01-vdom-foundations 문제지

## 왜 중요한가

Virtual DOM의 가장 작은 핵심을 직접 구현하면서 JSX-like 호출이 어떤 VNode 구조로 바뀌고, 그 구조가 실제 DOM으로 렌더되는지 설명 가능한 형태로 만든다.

## 목표

시작 위치의 구현을 완성해 props.children은 항상 배열이어야 한다, primitive child는 TEXT_ELEMENT로 감싸야 한다, DOM property와 event listener 반영은 updateDom 규칙으로 통일한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts`
- `../study/react-internals/01-vdom-foundations/problem/code/element.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/dom-utils.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/element.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/index.ts`
- `../study/react-internals/01-vdom-foundations/ts/src/types.ts`
- `../study/react-internals/01-vdom-foundations/ts/tests/dom-utils.test.ts`
- `../study/react-internals/01-vdom-foundations/ts/tests/element.test.ts`

## starter code / 입력 계약

- ../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts에서 starter 코드와 입력 경계를 잡는다.
- ../study/react-internals/01-vdom-foundations/problem/code/element.ts에서 starter 코드와 입력 경계를 잡는다.
- ../study/react-internals/01-vdom-foundations/problem/code/types.ts에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- props.children은 항상 배열이어야 한다.
- primitive child는 TEXT_ELEMENT로 감싸야 한다.
- DOM property와 event listener 반영은 updateDom 규칙으로 통일한다.
- createElement
- createTextElement
- createDom
- updateDom
- render
- ts/에 실행 가능한 VDOM 패키지 구현
- 다음 단계가 소비할 수 있는 export 경계
- VNode 구조와 DOM 반영을 검증하는 테스트

## 제외 범위

- diff/patch
- scheduler와 render/commit 분리
- hooks, effect, delegated events

## 성공 체크리스트

- `../study/react-internals/01-vdom-foundations/problem/code/dom-utils.ts`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `isEvent`와 `isProperty`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `createDom`와 `should create a Text node for TEXT_ELEMENT`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/react-internals/01-vdom-foundations/problem/script/Makefile` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
cd study && npm run test:vdom && npm run typecheck:vdom && npm run verify:vdom
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/01-vdom-foundations && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/01-vdom-foundations && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-vdom-foundations_answer.md`](01-vdom-foundations_answer.md)에서 확인한다.
