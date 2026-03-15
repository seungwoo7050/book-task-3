# 01-semantic-layouts-and-a11y-vanilla 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 React 없이 vanilla DOM과 CSS만 사용한다, 정적이지만 상호작용 가능한 UI shell이어야 한다, semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 `FIELD_IDS`와 `getFieldErrorId`, `getFieldInput` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- React 없이 vanilla DOM과 CSS만 사용한다.
- 정적이지만 상호작용 가능한 UI shell이어야 한다.
- semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다.
- 첫 진입점은 `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`이고, 여기서 `FIELD_IDS`와 `getFieldErrorId` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`: `FIELD_IDS`, `getFieldErrorId`, `getFieldInput`, `extractValues`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/main.ts`: `container`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts`: `EMAIL_PATTERN`, `validateSettings`, `hasValidationErrors`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/semantic-layout.spec.ts`: `exposes landmarks, labels, and responsive grid behavior`, `supports keyboard-only submission with visible validation messaging`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/shell.test.ts`: `mountSettingsShell`, `renders semantic landmarks and labeled controls`, `marks invalid fields and focuses the first invalid input on submit`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/validation.test.ts`: `validateSettings`, `returns errors for a short workspace name and invalid email`, `accepts valid values`가 통과 조건과 회귀 포인트를 잠근다.
- `FIELD_IDS` 구현은 `exposes landmarks, labels, and responsive grid behavior` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd study && npm run verify --workspace @front-react/semantic-layouts-a11y`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `exposes landmarks, labels, and responsive grid behavior` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd study && npm run verify --workspace @front-react/semantic-layouts-a11y`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd study && npm run verify --workspace @front-react/semantic-layouts-a11y
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `exposes landmarks, labels, and responsive grid behavior`와 `supports keyboard-only submission with visible validation messaging`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd study && npm run verify --workspace @front-react/semantic-layouts-a11y`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/main.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/semantic-layout.spec.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/shell.test.ts`
- `../study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/validation.test.ts`
