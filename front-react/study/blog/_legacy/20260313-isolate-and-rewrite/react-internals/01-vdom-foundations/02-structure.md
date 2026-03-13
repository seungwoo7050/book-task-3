# 01 VDOM Foundations structure

## opening frame

- 한 줄 훅: 이 단계의 핵심은 DOM을 "다시 그린다"가 아니라 JSX-like 호출을 어떤 데이터 shape로 고정해야 이후 단계가 설명 가능해지는지에 있다.
- chronology 주의: code와 docs가 2026-03-08 한 commit에 압축돼 있으므로, 글은 `VNode shape -> DOM reflection -> verify` 순서로 재구성한다.
- 첫 질문: primitive child와 props/event를 어떤 최소 규칙으로 정규화해야 `render`가 가능해지는가.

## chapter flow

1. adapted 문제 범위와 package contract를 먼저 고정한다.
2. `createTextElement`/`createElement`로 VNode shape를 설명한다.
3. `updateDom`/`render`와 verify 결과로 DOM reflection contract를 닫는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `problem/original/README.md`, `git log`
- 본문 1: `ts/src/element.ts`
- 본문 2: `ts/src/dom-utils.ts`
- 본문 3: `npm run verify --workspace @front-react/vdom-foundations`와 `ts/tests/*`

## tone guardrails

- React 역사 설명으로 흐르지 말고, 현재 패키지가 어떤 최소 invariant를 세웠는지에 집중한다.
- code snippet은 짧게 두고 `TEXT_ELEMENT`, prop/event reflection이 왜 다음 단계의 전제가 되는지 길게 설명한다.
- notion과 새 blog는 입력에서 제외한다.
