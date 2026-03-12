# 03 Hooks And Events

상태: `verified`

## 무슨 문제인가

함수 컴포넌트 state, effect cleanup, delegated event는 따로 배우면 조각 지식으로 남기 쉽다. 이 단계는 세 가지를 하나의 runtime 안에서 함께 돌게 만들면서 "상태 변경이 어떻게 이벤트와 effect로 이어지는가"를 설명하는 문제를 푼다.

## 왜 필요한가

React를 실무에서 쓰려면 state/effect와 event가 한 런타임 안에서 어떻게 이어지는지 설명할 수 있어야 한다. 이 단계는 hooks와 events를 분리된 trivia가 아니라 같은 runtime 축으로 묶는다.

## 내가 만든 답

`@front-react/render-pipeline` 위에 `useState`, `useEffect`, delegated event, runtime integration을 얹은 학습용 runtime 패키지를 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [ts/README.md](ts/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `ts/src/runtime.ts`에서 child normalization, hook slot 저장, effect cleanup, DOM metadata 동기화를 한 파일로 통합한다.
- hook order invariant를 지켜 조건부 hook 사용을 에러로 드러낸다.
- root container 단위 delegated event를 붙여 bubbling과 `stopPropagation`을 runtime 메타데이터로 처리한다.

## 검증

```bash
cd study
npm run test --workspace @front-react/hooks-and-events
npm run typecheck --workspace @front-react/hooks-and-events
npm run verify --workspace @front-react/hooks-and-events
```

- 검증 기준일: 2026-03-08
- `vitest`: `state.test.ts`, `effect.test.ts`, `events.test.ts`, `integration.test.ts`로 hook/event/runtime 흐름 확인
- `typecheck`: `@front-react/hooks-and-events` 패키지 타입 검사 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [ts/README.md](ts/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- `useMemo`, `useReducer`, `context`는 없다.
- React의 synthetic event 전체 호환성과 concurrent semantics 전체를 복제하지 않는다.
- 다음 단계인 `04-runtime-demo-app`에서 이 runtime을 실제 상호작용 앱에 얹어 본다.
