# 02 DOM State And Events

이 프로젝트의 진짜 질문은 "board UI를 만들 수 있는가"가 아니라, search/filter/sort처럼 공유돼야 하는 상태와 selection/edit처럼 로컬에 머물러야 하는 상태를 브라우저 안에서 어떻게 분리할 것인가에 있다. 이번 Todo에서는 URL query, localStorage persistence, delegated event handling, rerender 뒤 focus 복원이 실제 코드와 테스트에서 어떻게 이어지는지 다시 묶었다.

## 왜 이 순서로 읽는가

구현 축이 명확하다. `state.ts`가 URL과 persistence 경계를 먼저 잡고, `app.ts`가 root-level delegation으로 그 상태를 투영하며, 마지막에 브라우저 검증이 query -> select -> edit -> save 흐름을 재생한다. 그래서 이 프로젝트도 `series map + 본문 1편` 구조가 적당했다.

## 이번 재작성의 근거

- `frontend-foundations/02-dom-state-and-events/problem/README.md`
- `frontend-foundations/02-dom-state-and-events/docs/README.md`
- `frontend-foundations/02-dom-state-and-events/docs/references/verification-notes.md`
- `frontend-foundations/02-dom-state-and-events/vanilla/README.md`
- `frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/tests/state.test.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/tests/shell.test.ts`
- `frontend-foundations/02-dom-state-and-events/vanilla/tests/board.spec.ts`

## 현재 검증 상태

```bash
npm run build --workspace @front-react/dom-state-and-events
npm run test --workspace @front-react/dom-state-and-events
npm run e2e --workspace @front-react/dom-state-and-events
```

- 2026-03-14 재실행 기준 `vite build` 통과
- `vitest` 6개 테스트 통과
- `playwright` 2개 시나리오 통과

## 본문

- [10-where-browser-state-actually-lives.md](10-where-browser-state-actually-lives.md)
  - query state와 local state의 경계, delegated action, rerender 후 focus 복원이 어떻게 이어지는지 따라간다.

## 이번에 명시적으로 남긴 경계

- query state는 URL에 남기지만 edit draft 자체는 URL에 실리지 않는다.
- selection은 현재 visible items를 기준으로 `reconcileSelection()`에서 다시 계산된다.
- 실제 network request, server cache, multi-user sync는 아직 없다.
