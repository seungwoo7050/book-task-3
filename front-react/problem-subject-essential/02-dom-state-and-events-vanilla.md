# 02-dom-state-and-events-vanilla 문제지

## 왜 중요한가

task/workspace board에서 selection, filter, sort, inline edit, URL query state, local persistence를 동시에 다루면 이벤트 처리와 상태 저장 위치가 복잡해진다. 이 프로젝트는 브라우저 state를 어디에 두고 어떻게 다시 그릴지 설명 가능한 형태로 구현한다.

## 목표

시작 위치의 구현을 완성해 React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다, query state와 local UI state의 경계를 분리해야 한다, rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/data.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/main.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/state.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/board.spec.ts`
- `../study/frontend-foundations/02-dom-state-and-events/vanilla/tests/shell.test.ts`

## starter code / 입력 계약

- `../study/frontend-foundations/02-dom-state-and-events/vanilla/src/app.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다.
- query state와 local UI state의 경계를 분리해야 한다.
- rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다.
- filter and sort controls
- row selection and inline edit
- localStorage persistence
- URL query sync
- keyboard interaction
- vanilla/에 실행 가능한 board 구현
- query serialization, persistence, selection 규칙을 설명하는 공개 문서
- state helper와 핵심 keyboard 흐름을 검증하는 테스트

## 제외 범위

- 실제 network request
- complex authentication
- server cache

## 성공 체크리스트

- 핵심 흐름은 `syncUrl`와 `getSelectedItem`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `syncs filters to URL and persists edits across reload`와 `supports keyboard selection and inline edit submission`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd study && npm run verify --workspace @front-react/dom-state-and-events`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/dom-state-and-events
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-dom-state-and-events-vanilla_answer.md`](02-dom-state-and-events-vanilla_answer.md)에서 확인한다.
