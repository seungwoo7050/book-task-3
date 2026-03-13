# 01 VDOM Foundations

JSX 같은 입력이 실제로 어떤 plain object 트리로 정규화되고, 그 트리가 어떤 규칙으로 DOM이 되는지를 가장 작은 범위에서 보여 주는 프로젝트다. 뒤 단계의 diff와 scheduler는 모두 여기서 만든 shape를 전제로 움직인다.

## 왜 이 순서로 읽는가

이 프로젝트는 child shape 정규화, DOM 생성/업데이트 분리, 패키지 경계 고정이라는 단일 축으로 읽힌다. foundation 단계라 문서를 여러 편으로 나누기보다 한 편에서 끝까지 따라가는 편이 더 자연스럽다.

## 근거로 사용한 자료

- `react-internals/01-vdom-foundations/README.md`
- `react-internals/01-vdom-foundations/docs/concepts/jsx-to-vnode.md`
- `react-internals/01-vdom-foundations/ts/src/element.ts`
- `react-internals/01-vdom-foundations/ts/src/dom-utils.ts`
- `react-internals/01-vdom-foundations/ts/tests/element.test.ts`
- `react-internals/01-vdom-foundations/ts/tests/dom-utils.test.ts`

## 현재 검증 상태

- `npm run verify:vdom`
- 2026-03-13 replay 기준 `vitest` 27개, `tsc --noEmit` 통과

## 본문

- [10-from-jsx-shape-to-dom-nodes.md](10-from-jsx-shape-to-dom-nodes.md)
  - `TEXT_ELEMENT` 정규화가 왜 foundation 단계의 가장 중요한 결정이었는지 따라간다.
