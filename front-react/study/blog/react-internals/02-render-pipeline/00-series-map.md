# 02 Render Pipeline

VDOM foundation 위에 diff, patch, cooperative work loop를 얹어 render와 commit을 분리한 프로젝트다. 이 단계부터는 "다시 그린다"는 말이 실제로 무엇을 뜻하는지, 그리고 DOM을 언제 건드려야 하는지가 코드로 드러난다.

## 왜 이 순서로 읽는가

이 프로젝트는 change detection, patch ordering, commit timing이라는 세 가지 주제가 하나의 파이프라인으로 이어진다. 한 편 안에서 순차적으로 읽는 편이 가장 자연스럽다.

## 근거로 사용한 자료

- `react-internals/02-render-pipeline/README.md`
- `react-internals/02-render-pipeline/docs/concepts/render-vs-commit.md`
- `react-internals/02-render-pipeline/ts/src/diff.ts`
- `react-internals/02-render-pipeline/ts/src/patch.ts`
- `react-internals/02-render-pipeline/ts/src/scheduler.ts`
- `react-internals/02-render-pipeline/ts/tests/diff.test.ts`
- `react-internals/02-render-pipeline/ts/tests/scheduler.test.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/render-pipeline`
- 2026-03-13 replay 기준 `vitest` 8개, `tsc --noEmit` 통과

## 본문

- [10-when-render-stops-being-commit.md](10-when-render-stops-being-commit.md)
  - "렌더한다"는 말이 왜 diff 계산과 DOM 반영이라는 두 단계로 갈라져야 했는지 따라간다.
