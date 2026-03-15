# 03-hooks-and-events 문제지

## 왜 중요한가

함수 컴포넌트 state, effect cleanup, delegated event를 각각 따로 구현하는 대신, 세 가지가 하나의 runtime loop 안에서 어떻게 이어지는지 보여 주는 학습용 runtime을 만든다.

## 목표

시작 위치의 구현을 완성해 @front-react/render-pipeline의 diff/patch helper를 그대로 소비한다, hook order invariant를 지켜야 한다, delegated event는 runtime tree 메타데이터를 통해 처리해야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/react-internals/03-hooks-and-events/ts/src/index.ts`
- `../study/react-internals/03-hooks-and-events/ts/src/runtime.ts`
- `../study/react-internals/03-hooks-and-events/ts/src/types.ts`
- `../study/react-internals/03-hooks-and-events/ts/tests/effect.test.ts`
- `../study/react-internals/03-hooks-and-events/ts/tests/events.test.ts`
- `../study/react-internals/03-hooks-and-events/tsconfig.json`
- `../study/react-internals/03-hooks-and-events/package.json`
- `../study/react-internals/03-hooks-and-events/vitest.config.ts`

## starter code / 입력 계약

- `../study/react-internals/03-hooks-and-events/ts/src/index.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- @front-react/render-pipeline의 diff/patch helper를 그대로 소비한다.
- hook order invariant를 지켜야 한다.
- delegated event는 runtime tree 메타데이터를 통해 처리해야 한다.
- function component execution
- useState
- useEffect와 cleanup lifecycle
- delegated event bubbling
- stopPropagation
- runtime integration
- ts/에 실행 가능한 hooks/events runtime 구현
- hook slot, effect timing, delegated event를 설명하는 공개 문서
- state, effect, event integration을 검증하는 테스트

## 제외 범위

- useMemo, useReducer, context
- React의 synthetic event 전체 호환성
- concurrent semantics 전체

## 성공 체크리스트

- 핵심 흐름은 `currentRoot`와 `currentHookContext`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `useEffect`와 `runs effects after commit and cleans them up before the next effect`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/react-internals/03-hooks-and-events/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `cd study && npm run verify --workspace @front-react/hooks-and-events`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/hooks-and-events
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/03-hooks-and-events && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/03-hooks-and-events && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-hooks-and-events_answer.md`](03-hooks-and-events_answer.md)에서 확인한다.
