# 04-runtime-demo-app 문제지

## 왜 중요한가

직접 만든 runtime이 실제 상호작용 앱 위에서 어디까지 버틸 수 있는지 보여 주기 위해, shared runtime을 그대로 import해 검색, 페이지네이션, metrics를 갖춘 consumer app을 만든다.

## 목표

시작 위치의 구현을 완성해 runtime 코드를 복사하지 않고 @front-react/hooks-and-events를 직접 소비해야 한다, debounced search와 pagination이 같은 UI에서 함께 동작해야 한다, metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/react-internals/04-runtime-demo-app/ts/src/app.ts`
- `../study/react-internals/04-runtime-demo-app/ts/src/data.ts`
- `../study/react-internals/04-runtime-demo-app/ts/src/main.ts`
- `../study/react-internals/04-runtime-demo-app/ts/tests/demo.test.ts`
- `../study/react-internals/04-runtime-demo-app/tsconfig.json`
- `../study/react-internals/04-runtime-demo-app/package.json`
- `../study/react-internals/04-runtime-demo-app/vite.config.ts`

## starter code / 입력 계약

- `../study/react-internals/04-runtime-demo-app/ts/src/app.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- runtime 코드를 복사하지 않고 @front-react/hooks-and-events를 직접 소비해야 한다.
- debounced search와 pagination이 같은 UI에서 함께 동작해야 한다.
- metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다.
- shared runtime consumer app
- debounced search
- load-more pagination
- render metrics panel
- integration-style 검증
- ts/에 실행 가능한 runtime consumer app 구현
- shared runtime consumption과 limitation을 설명하는 공개 문서
- debounce, pagination, metrics를 검증하는 테스트

## 제외 범위

- 실제 infinite scroll observer
- network layer와 persistence
- production-grade performance profiling

## 성공 체크리스트

- 핵심 흐름은 `PAGE_SIZE`와 `DEBOUNCE_MS`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `runtime demo app`와 `filters results after the debounce window and updates metrics`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/react-internals/04-runtime-demo-app/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `cd study && npm run verify --workspace @front-react/runtime-demo-app`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/runtime-demo-app
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`04-runtime-demo-app_answer.md`](04-runtime-demo-app_answer.md)에서 확인한다.
