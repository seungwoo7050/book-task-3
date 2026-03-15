# 02-render-pipeline 문제지

## 왜 중요한가

동기 전체 render의 다음 단계는 무엇이 바뀌었는지 계산하고, 그 계산 결과를 언제 DOM에 반영할지 분리하는 것이다. 이 단계는 reconciliation과 fiber-like work loop를 "render pipeline"이라는 하나의 질문으로 묶어 구현한다.

## 목표

시작 위치의 구현을 완성해 @front-react/vdom-foundations의 VNode 구조를 그대로 사용한다, render phase 동안 DOM mutation을 하면 안 된다, keyed/unkeyed child diff를 모두 설명할 수 있어야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/react-internals/02-render-pipeline/ts/src/diff.ts`
- `../study/react-internals/02-render-pipeline/ts/src/fiber.ts`
- `../study/react-internals/02-render-pipeline/ts/src/index.ts`
- `../study/react-internals/02-render-pipeline/ts/src/patch.ts`
- `../study/react-internals/02-render-pipeline/ts/tests/diff.test.ts`
- `../study/react-internals/02-render-pipeline/ts/tests/patch.test.ts`
- `../study/react-internals/02-render-pipeline/tsconfig.json`
- `../study/react-internals/02-render-pipeline/package.json`

## starter code / 입력 계약

- `../study/react-internals/02-render-pipeline/ts/src/diff.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- @front-react/vdom-foundations의 VNode 구조를 그대로 사용한다.
- render phase 동안 DOM mutation을 하면 안 된다.
- keyed/unkeyed child diff를 모두 설명할 수 있어야 한다.
- diffProps
- diffChildren
- diff
- applyPatches
- render
- workLoop
- flushSync
- ts/에 실행 가능한 render pipeline 패키지 구현
- diff, patch, scheduler를 설명하는 공개 문서
- DOM patch ordering과 interrupted work를 검증하는 테스트

## 제외 범위

- 함수 컴포넌트 state와 effect
- delegated events
- React의 priority/lanes 모델 전체

## 성공 체크리스트

- 핵심 흐름은 `diffProps`와 `isEmptyPropsPatch`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `diffProps`와 `returns changed and removed props`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/react-internals/02-render-pipeline/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `cd study && npm run verify --workspace @front-react/render-pipeline`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/render-pipeline
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/02-render-pipeline && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-render-pipeline_answer.md`](02-render-pipeline_answer.md)에서 확인한다.
