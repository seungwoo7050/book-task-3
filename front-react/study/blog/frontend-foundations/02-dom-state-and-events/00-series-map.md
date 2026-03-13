# 02 DOM State And Events

search, filter, sort, selection, inline edit, URL query, localStorage를 한 화면에 올리고 브라우저 상태를 어디에 둘지 정리한 프로젝트다. 이 단계부터는 semantic shell보다 상태 경계와 rerender 이후의 사용자 감각이 더 중요해진다.

## 왜 이 순서로 읽는가

이 프로젝트도 구현 축이 하나로 묶여 있다. URL과 local state의 우선순위를 먼저 정하고, 그 위에 event delegation과 focus 복원을 얹고, 마지막에 reload와 keyboard flow를 브라우저에서 확인한다.

## 근거로 사용한 자료

- `frontend-foundations/02-dom-state-and-events/README.md`
- `frontend-foundations/02-dom-state-and-events/docs/concepts/state-and-url-boundaries.md`
- `frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/tests/state.test.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/tests/board.spec.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/dom-state-and-events`
- 2026-03-13 replay 기준 `vitest` 6개, `playwright` 2개 시나리오 통과

## 본문

- [10-where-browser-state-actually-lives.md](10-where-browser-state-actually-lives.md)
  - URL state와 local UI state가 왜 같은 "state"라는 이름으로는 설명되지 않는지 따라간다.
