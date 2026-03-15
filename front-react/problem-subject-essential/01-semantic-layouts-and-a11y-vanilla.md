# 01-semantic-layouts-and-a11y-vanilla 문제지

## 왜 중요한가

설정/대시보드 성격의 화면을 만들면서 semantic layout, form grouping, help/error text pairing, keyboard reachable interaction이 실제 DOM 구조에 어떻게 드러나는지 검증 가능한 형태로 구현한다.

## 목표

시작 위치의 구현을 완성해 React 없이 vanilla DOM과 CSS만 사용한다, 정적이지만 상호작용 가능한 UI shell이어야 한다, semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/main.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/semantic-layout.spec.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/shell.test.ts`

## starter code / 입력 계약

- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- React 없이 vanilla DOM과 CSS만 사용한다.
- 정적이지만 상호작용 가능한 UI shell이어야 한다.
- semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다.
- semantic landmarks
- responsive two-column to single-column layout
- labeled forms
- inline help and error pairing
- keyboard focus states
- vanilla/에 실행 가능한 UI shell 구현
- landmark, form, validation 흐름을 설명하는 공개 문서
- 구조적 검증과 keyboard smoke를 포함한 테스트

## 제외 범위

- 복잡한 데이터 fetching
- local persistence
- 실제 라우팅

## 성공 체크리스트

- 핵심 흐름은 `FIELD_IDS`와 `getFieldErrorId`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `exposes landmarks, labels, and responsive grid behavior`와 `supports keyboard-only submission with visible validation messaging`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd study && npm run verify --workspace @front-react/semantic-layouts-a11y`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/semantic-layouts-a11y
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-semantic-layouts-and-a11y-vanilla_answer.md`](01-semantic-layouts-and-a11y-vanilla_answer.md)에서 확인한다.
