# 03 Hooks And Events

hook slot, effect cleanup, delegated event를 하나의 runtime root 안에 묶어 "상태가 바뀌면 무엇이 다시 돌고 언제 부수효과가 실행되는가"를 직접 보여 주는 프로젝트다.

## 왜 이 순서로 읽는가

state, effect, event를 따로 떼어 쓰면 trivia처럼 남기 쉽다. 이 프로젝트는 셋을 하나의 render/commit 흐름으로 묶는 데 의미가 있으므로, 본문도 한 편으로 압축했다.

## 근거로 사용한 자료

- `react-internals/03-hooks-and-events/README.md`
- `react-internals/03-hooks-and-events/docs/concepts/hook-slot-model.md`
- `react-internals/03-hooks-and-events/ts/src/runtime.ts`
- `react-internals/03-hooks-and-events/ts/tests/state.test.ts`
- `react-internals/03-hooks-and-events/ts/tests/effect.test.ts`
- `react-internals/03-hooks-and-events/ts/tests/events.test.ts`
- `react-internals/03-hooks-and-events/ts/tests/integration.test.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/hooks-and-events`
- 2026-03-13 replay 기준 `vitest` 7개, `tsc --noEmit` 통과

## 본문

- [10-hook-slots-effects-and-delegation-in-one-runtime.md](10-hook-slots-effects-and-delegation-in-one-runtime.md)
  - hook slot과 delegated event가 왜 사실상 같은 metadata 문제였는지 따라간다.
