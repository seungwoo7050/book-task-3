# TypeScript 구현

프로비넌스: `authored`

## 이 구현이 답하는 범위

- `createElement`
- `createTextElement`
- `createDom`
- `updateDom`
- `render`

## 핵심 파일

- `src/element.ts`: VNode 생성과 text child 정규화
- `src/dom-utils.ts`: DOM 생성, prop/event 반영, 동기 재귀 render
- `src/index.ts`: 다음 단계가 소비할 export 경계

## 실행과 검증

```bash
cd study
npm run test:vdom
npm run typecheck:vdom
npm run verify:vdom
```

## 현재 한계

- 동기 재귀 렌더만 지원한다.
- 함수 컴포넌트 실행, diff/patch, scheduler, hooks, delegation은 아직 없다.
- `null` 같은 특수 child 값은 최소 구현 범위 밖이다.
