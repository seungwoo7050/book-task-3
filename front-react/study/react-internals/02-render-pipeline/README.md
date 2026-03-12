# 02 Render Pipeline

상태: `verified`

## 무슨 문제인가

동기 재귀 render만으로는 무엇이 바뀌었는지 계산할 수 없고, DOM을 언제 건드릴지도 통제하기 어렵다. 이 단계는 최소 DOM 변경 계산과 render/commit 분리를 하나의 파이프라인으로 설계하는 문제를 푼다.

## 왜 필요한가

React는 "다시 그린다"로 끝나지 않는다. 무엇이 바뀌었는지 계산하고, 그 계산을 언제 commit할지를 분리하는 사고가 있어야 성능과 한계를 설명할 수 있다.

## 내가 만든 답

`@front-react/vdom-foundations` 위에 diff, patch, cooperative work loop, `flushSync`를 얹어 최소 render pipeline 패키지를 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [ts/README.md](ts/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `ts/src/diff.ts`에서 prop delta와 keyed/unkeyed child diff를 계산한다.
- `ts/src/patch.ts`에서 create/remove/replace/update patch를 DOM-safe 순서로 적용한다.
- `ts/src/scheduler.ts`에서 render phase 동안 DOM mutation을 미루고, `flushSync`와 interrupted work를 지원한다.

## 검증

```bash
cd study
npm run test --workspace @front-react/render-pipeline
npm run typecheck --workspace @front-react/render-pipeline
npm run verify --workspace @front-react/render-pipeline
```

- 검증 기준일: 2026-03-08
- `vitest`: `diff.test.ts`, `patch.test.ts`, `scheduler.test.ts`로 diff/patch/scheduler 확인
- `typecheck`: `@front-react/render-pipeline` 패키지 타입 검사 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [ts/README.md](ts/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 함수 컴포넌트 상태와 effect는 아직 없다.
- event delegation과 React의 priority/lanes 모델은 다루지 않는다.
- 다음 단계인 `03-hooks-and-events`에서 state, effect, event를 같은 runtime 흐름으로 묶는다.
