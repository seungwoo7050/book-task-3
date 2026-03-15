# 02 Render Pipeline

이 프로젝트의 핵심은 "VDOM이 있으니 빨라진다"가 아니라, 어떤 변경을 계산하는 단계와 실제 DOM을 건드리는 단계를 분리해 두면 무엇을 설명할 수 있게 되는가에 있다. 이번 Todo에서는 prop delta, keyed/unkeyed child diff, `effectTag` 기반 fiber work loop, `flushSync` commit 경계를 중심으로 다시 정리했다.

## 왜 이 순서로 읽는가

구현 흐름이 명확하다. `diff.ts`가 변경 계산 범위를 먼저 고정하고, `fiber.ts`가 render phase에서 effect를 모으며, `patch.ts`와 `scheduler.ts`가 commit 시점과 DOM-safe ordering을 책임진다. 그래서 이 프로젝트도 `series map + 본문 1편` 구조가 가장 자연스럽다.

## 이번 재작성의 근거

- `react-internals/02-render-pipeline/problem/README.md`
- `react-internals/02-render-pipeline/docs/README.md`
- `react-internals/02-render-pipeline/ts/README.md`
- `react-internals/02-render-pipeline/ts/src/diff.ts`
- `react-internals/02-render-pipeline/ts/src/fiber.ts`
- `react-internals/02-render-pipeline/ts/src/patch.ts`
- `react-internals/02-render-pipeline/ts/src/scheduler.ts`
- `react-internals/02-render-pipeline/ts/tests/diff.test.ts`
- `react-internals/02-render-pipeline/ts/tests/patch.test.ts`
- `react-internals/02-render-pipeline/ts/tests/scheduler.test.ts`

## 현재 검증 상태

```bash
npm run verify --workspace @front-react/render-pipeline
```

- 2026-03-14 재실행 기준 `vitest` 8개 테스트 통과
- `tsc --noEmit` typecheck 통과
- verify 전체 통과

## 본문

- [10-when-render-stops-being-commit.md](10-when-render-stops-being-commit.md)
  - diff 계산, fiber effect 수집, commit 시점, interrupted work 경계를 순서대로 따라간다.

## 이번에 명시적으로 남긴 경계

- render phase에서는 DOM mutation이 일어나지 않는다.
- keyed diff는 reorder patch를 만들지 않고 create/remove/update 수준까지만 다룬다.
- unkeyed diff는 child identity를 추적하지 않고 index 위치를 기준으로 같은 자리의 node를 update한다.
- hooks, effects, priority lanes, delegated events는 아직 없다.
