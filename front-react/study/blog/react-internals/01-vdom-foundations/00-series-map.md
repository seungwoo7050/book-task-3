# 01 VDOM Foundations

이 프로젝트의 핵심은 "작은 React를 만들었다"가 아니라, JSX-like 입력이 어떤 VNode shape로 정규화되고 그 shape가 실제 DOM 노드로 물질화되는지를 가장 작은 규칙 집합으로 고정하는 데 있다. 이번 Todo에서는 `TEXT_ELEMENT` 정규화, `updateDom`의 prop/event 규칙, 그리고 diff 없는 append-only render 경계를 중심으로 다시 정리했다. 여기에 더해 React와 다른 child semantics도 분명히 남긴다. 현재 구현은 `false`를 text로 바꾸고, `null`은 안전하게 걸러 내지 않는다.

## 왜 이 순서로 읽는가

구현 축이 단순하고 또렷하다. `element.ts`에서 VNode shape를 먼저 고정하고, `dom-utils.ts`에서 DOM 생성과 prop/event 반영 규칙을 붙인 다음, 테스트로 그 shape와 동작을 잠근다. 그래서 이 프로젝트도 `series map + 본문 1편` 구조가 가장 적합했다.

## 이번 재작성의 근거

- `react-internals/01-vdom-foundations/problem/README.md`
- `react-internals/01-vdom-foundations/docs/README.md`
- `react-internals/01-vdom-foundations/ts/README.md`
- `react-internals/01-vdom-foundations/ts/src/element.ts`
- `react-internals/01-vdom-foundations/ts/src/dom-utils.ts`
- `react-internals/01-vdom-foundations/ts/src/index.ts`
- `react-internals/01-vdom-foundations/ts/tests/element.test.ts`
- `react-internals/01-vdom-foundations/ts/tests/dom-utils.test.ts`

## 현재 검증 상태

```bash
npm run test:vdom
npm run typecheck:vdom
npm run verify:vdom
```

- 2026-03-14 재실행 기준 `vitest` 27개 테스트 통과
- `tsc --noEmit` typecheck 통과
- `verify:vdom` 통과

## 본문

- [10-from-jsx-shape-to-dom-nodes.md](10-from-jsx-shape-to-dom-nodes.md)
  - child 정규화, DOM prop/event 반영, append-only render 경계를 순서대로 따라간다.

## 이번에 명시적으로 남긴 경계

- `render()`는 container를 비우지 않고 새 트리를 append한다.
- diff/patch, scheduler, hooks, delegated events는 아직 없다.
- `false` 같은 boolean child는 React처럼 무시되지 않고 text로 정규화된다.
- `null` 같은 특수 child는 최소 구현 범위 밖이라 안전하게 걸러지지 않는다.
