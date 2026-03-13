# 04 Runtime Demo App

직접 만든 `@front-react/hooks-and-events` 런타임을 실제 consumer app이 가져다 쓰게 만들어, debounce, pagination, metrics 같은 상호작용이 어디까지 버티는지 확인한 프로젝트다.

## 왜 이 순서로 읽는가

이 프로젝트의 본론은 새로운 런타임 기능을 더하는 일이 아니라, 이미 만든 런타임이 실제 앱 맥락에서 어떤 한계를 드러내는지 보는 일이다. 본문 1편으로 따라가는 편이 가장 자연스럽다.

## 근거로 사용한 자료

- `react-internals/04-runtime-demo-app/README.md`
- `react-internals/04-runtime-demo-app/docs/concepts/shared-runtime-consumption.md`
- `react-internals/04-runtime-demo-app/ts/src/app.ts`
- `react-internals/04-runtime-demo-app/ts/src/data.ts`
- `react-internals/04-runtime-demo-app/ts/tests/demo.test.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/runtime-demo-app`
- 2026-03-13 replay 기준 `vitest` 3개, `tsc --noEmit` 통과

## 본문

- [10-making-the-runtime-survive-a-real-app.md](10-making-the-runtime-survive-a-real-app.md)
  - debounce와 metrics 같은 평범한 앱 상호작용이 오히려 런타임의 한계를 가장 잘 드러낸다는 사실을 따라간다.
