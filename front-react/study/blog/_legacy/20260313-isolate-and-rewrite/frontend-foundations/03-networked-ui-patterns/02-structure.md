# 03 Networked UI Patterns structure

## opening frame

- 한 줄 훅: 이 프로젝트의 핵심은 "데이터를 가져온다"가 아니라 어떤 응답만 state를 바꿀 자격이 있는지를 끝까지 통제하는 데 있다.
- chronology 주의: commit은 하나로 압축돼 있지만, 코드 구조는 `service -> state -> app -> tests`로 명확히 갈라져 있어 이 순서로 글을 세우는 편이 자연스럽다.
- 첫 질문: loading, empty, error, retry, abort, stale response를 explorer UI 한 화면에서 어떻게 제품처럼 보이게 했는가.

## chapter flow

1. README와 `problem/README.md`로 async UI contract를 먼저 선언한다.
2. `createRequestTracker`, `loadList`, `loadDetail`를 따라 stale response 방지 invariant를 설명한다.
3. verify 결과로 retry와 query-driven navigation이 실제로 닫히는지 보여 준다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log --reverse --stat`
- 본문 1: `vanilla/src/state.ts`의 URL state + request tracker
- 본문 2: `vanilla/src/app.ts`의 `loadList`/`loadDetail`
- 본문 3: `npm run verify --workspace @front-react/networked-ui-patterns`와 `vanilla/tests/explorer.spec.ts`

## tone guardrails

- mock API라는 표현에 기대지 않고, 왜 abort와 latest-token check가 둘 다 필요한지 구체적으로 쓴다.
- loading/empty/error/retry를 나열하지 말고 state 전이로 이어서 설명한다.
- notion과 새 blog 파일은 근거에서 제외한다.
