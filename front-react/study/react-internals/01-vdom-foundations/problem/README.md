# 문제 정의

프로비넌스: `adapted`

## 문제

Virtual DOM의 가장 작은 핵심을 직접 구현하면서 JSX-like 호출이 어떤 VNode 구조로 바뀌고, 그 구조가 실제 DOM으로 렌더되는지 설명 가능한 형태로 만든다.

## 제공 자산

- [original/README.md](original/README.md): 원문 문제 명세
- `code/element.ts`: `createElement`, `createTextElement` 스켈레톤
- `code/dom-utils.ts`: `createDom`, `updateDom`, `render` 스켈레톤
- `code/types.ts`: VNode 타입 정의
- `script/Makefile`: 새 워크스페이스 경로에 맞춘 적응 스크립트
- `data/`: 별도 입력 데이터가 없어 placeholder만 유지

## 제약

- `props.children`은 항상 배열이어야 한다.
- primitive child는 `TEXT_ELEMENT`로 감싸야 한다.
- DOM property와 event listener 반영은 `updateDom` 규칙으로 통일한다.

## 포함 범위

- `createElement`
- `createTextElement`
- `createDom`
- `updateDom`
- `render`

## 제외 범위

- diff/patch
- scheduler와 render/commit 분리
- hooks, effect, delegated events

## 요구 산출물

- `ts/`에 실행 가능한 VDOM 패키지 구현
- 다음 단계가 소비할 수 있는 export 경계
- VNode 구조와 DOM 반영을 검증하는 테스트

## Canonical Verification

```bash
cd study
npm run test:vdom
npm run typecheck:vdom
npm run verify:vdom
```

- `element.test.ts`: VNode 구조와 text child 정규화 확인
- `dom-utils.test.ts`: DOM 생성, prop 반영, 동기 재귀 render 확인
