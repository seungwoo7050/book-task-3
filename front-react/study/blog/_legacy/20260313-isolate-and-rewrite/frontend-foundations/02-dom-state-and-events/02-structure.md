# 02 DOM State And Events structure

## opening frame

- 한 줄 훅: 이 프로젝트의 진짜 난점은 이벤트 handler 개수가 아니라 URL, localStorage, selection, edit state가 다시 그리기 이후에도 서로 모순 없이 남아야 한다는 점이다.
- chronology 주의: `46051f3`에 state helper와 board UI가 압축돼 있어서, 글은 `state boundary -> render loop -> verify` 순서로 재구성한다.
- 첫 질문: 브라우저 state를 어디에 두고, 어떤 이벤트로 다시 그리고, rerender 뒤 focus는 어떻게 유지하는가.

## chapter flow

1. README와 `state.ts`로 query state vs local state 경계를 먼저 설명한다.
2. `mountBoard`의 render loop와 root delegation으로 selection/edit 흐름을 따라간다.
3. verify 출력으로 query -> select -> edit -> save 시나리오를 닫고 남은 비범위를 적는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log --reverse --stat`
- 본문 1: `vanilla/src/state.ts`의 `serializeQuery`, `reconcileSelection`
- 본문 2: `vanilla/src/app.ts`의 `render`, `setEditing`, root event delegation
- 본문 3: `npm run verify --workspace @front-react/dom-state-and-events`와 `vanilla/tests/board.spec.ts`

## tone guardrails

- "이벤트를 처리했다"가 아니라 어떤 state가 URL에 남고 어떤 state는 local로만 남는지 구체적으로 적는다.
- rerender와 focus 복원을 같은 문단에서 다뤄 keyboard continuity를 흐리지 않는다.
- notion과 기존 blog는 입력 근거로 쓰지 않는다.
