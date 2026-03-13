# 01 Semantic Layouts And A11y development timeline

`01-semantic-layouts-and-a11y`의 git 기록은 세세한 commit slice보다 2026-03-08의 큰 landing이 더 강하게 남아 있다. 그래서 이 글은 `study/frontend-foundations/01-semantic-layouts-and-a11y`의 README, `problem/`, `vanilla/`, 테스트, 그리고 2026-03-13 재검증 CLI를 바탕으로 semantic shell이 어떤 순서로 굳었는지 다시 세운 chronology다.

## 구현 순서 요약

1. README와 `package.json`으로 이 프로젝트가 landmark, label, keyboard flow를 검증하는 독립 과제라는 점을 먼저 고정했다.
2. `vanilla/src/app.ts`와 `validation.ts`를 따라가며 semantic 마크업과 validation/focus 루프가 같은 control flow 안에 묶이는 지점을 찾았다.
3. 마지막에는 `npm run verify --workspace @front-react/semantic-layouts-a11y` 출력과 Playwright smoke를 연결해 "읽히는 구조"가 실제 interaction까지 닫히는지 확인했다.

## 2026-03-08 / Phase 1 - public surface를 먼저 고정한다

- 당시 목표:
  이 프로젝트가 단순한 폼 데모가 아니라 semantic shell 과제라는 사실을 public surface에서 먼저 고정한다.
- 변경 단위:
  `README.md`, `problem/README.md`, `vanilla/README.md`, `package.json`
- 처음 가설:
  validation helper만 보면 이 프로젝트를 "폼 검증 예제"로 오해하기 쉽다. 먼저 README와 verify surface를 읽어야 landmark와 keyboard flow가 본론이라는 점이 보일 거라고 봤다.
- 실제 진행:
  루트와 프로젝트 README를 읽고 `npm run verify --workspace @front-react/semantic-layouts-a11y`가 이 프로젝트의 canonical contract라는 점을 먼저 고정했다. 그 다음 `git log --reverse --stat`로 2026-03-08의 large commit이 `README`, `problem`, `vanilla`, `tests`, `vite/vitest/playwright`를 한 번에 넣었다는 사실을 확인했다.

CLI:

```bash
$ git log --reverse --stat -- study/frontend-foundations/01-semantic-layouts-and-a11y | sed -n '1,24p'
commit 46051f3e897f38aacdfce37bcd5119e61c79ebea
Author: seungwoo <seungwoo7050@naver.com>
Date:   Sun Mar 8 19:03:24 2026 +0900

    A large commit

... README.md
... problem/README.md
... vanilla/src/app.ts
... vanilla/src/validation.ts
... vanilla/tests/semantic-layout.spec.ts

$ sed -n '1,80p' study/frontend-foundations/01-semantic-layouts-and-a11y/README.md
# 01 Semantic Layouts And A11y
...
- `playwright`: landmark 탐색과 keyboard submission `2`개 시나리오 통과
```

검증 신호:

- `git log`만 봐도 이 디렉터리가 문제 정의, 구현, 테스트, 검증 설정을 스스로 가진 독립 프로젝트라는 점이 분명했다.
- README의 핵심 질문이 "semantic 구조와 접근성"에 맞춰져 있어서, 이후 코드를 읽을 때도 visual polish보다 DOM 구조를 먼저 봐야 한다는 기준이 생겼다.

핵심 코드:

```ts
function updateErrorState(form: HTMLFormElement, errors: SettingsErrors): number {
  let errorCount = 0;

  FIELD_IDS.forEach((field) => {
    const input = getFieldInput(form, field);
    const errorText = form.querySelector<HTMLElement>(`#${getFieldErrorId(field)}`);
    const message = errors[field];
```

왜 이 코드가 중요했는가:

이 프로젝트의 첫 전환점은 "semantic markup를 그려 놓는다"에서 끝나지 않는다는 점이다. `updateErrorState`는 label, inline error, `aria-invalid`를 한 묶음으로 다루면서 접근성이 별도 후처리가 아니라 상태 전이의 일부라는 사실을 드러낸다.

새로 배운 것:

- accessible form에서 중요한 건 문구 자체보다 `label/help/error`가 입력 필드와 어떤 관계로 연결되는지, 그리고 에러가 났을 때 focus가 어디로 이동하는지다.

다음:

- submit과 blur가 같은 validation 루프를 공유하는 지점을 본다.

## 2026-03-08 / Phase 2 - validation과 focus 이동을 같은 루프로 묶는다

- 당시 목표:
  semantic shell 설명을 실제 interaction loop까지 끌어내린다.
- 변경 단위:
  `vanilla/src/app.ts`, `vanilla/src/validation.ts`
- 처음 가설:
  blur validation과 submit validation이 따로 놀면 keyboard-only 흐름이 금방 끊길 거라고 봤다.
- 실제 진행:
  `rg -n`으로 `updateErrorState`, `focusFirstInvalidField`, `mountSettingsShell`, `validateSettings` 위치를 다시 잡은 뒤, `mountSettingsShell`이 submit과 blur 이벤트를 모두 같은 `runValidation` 경로로 모은다는 점을 중심으로 읽었다.

CLI:

```bash
$ rg -n 'updateErrorState|mountSettingsShell|validateSettings|focusFirstInvalidField' \
  study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts \
  study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts
study/.../app.ts:28:function updateErrorState(...)
study/.../app.ts:55:function focusFirstInvalidField(...)
study/.../app.ts:190:export function mountSettingsShell(...)
study/.../validation.ts:14:export function validateSettings(...)
```

검증 신호:

- interaction 관련 symbol이 모두 `app.ts`의 한 루프에 모여 있어서, 구조와 상호작용을 억지로 나눈 프로젝트가 아니라는 점이 분명해졌다.
- `validation.ts`가 순수 함수로 분리되어 있어서 DOM wiring과 rule 자체를 분리해서 설명할 수 있었다.

핵심 코드:

```ts
const runValidation = (targetField?: typeof FIELD_IDS[number]) => {
  const errors = validateSettings(extractValues(form));
  if (targetField) {
    const targetErrors: SettingsErrors = { [targetField]: errors[targetField] };
    updateErrorState(form, targetErrors);
    return errors;
  }
  updateErrorState(form, errors);
  return errors;
};
```

왜 이 코드가 중요했는가:

여기서 처음 명확해지는 건 validation이 단순히 submit 전에 한 번 검사하는 절차가 아니라, blur와 submit을 같은 규칙 세트로 묶는 "interaction contract"라는 점이다. field 단위 검사와 form 전체 검사가 같은 함수에 매달려 있으니, keyboard-only 사용자가 어느 순간에 어떤 피드백을 받는지도 예측 가능해진다.

새로 배운 것:

- accessibility에서 focus 복원은 장식이 아니다. 에러가 난 뒤 첫 invalid field로 이동시켜야 keyboard 경로가 끊기지 않는다.

다음:

- 구조 검증과 keyboard smoke가 이 루프를 실제로 보증하는지 확인한다.

## 2026-03-12 to 2026-03-13 / Phase 3 - verify와 public contract로 마무리한다

- 당시 목표:
  README의 품질 설명이 실제 테스트와 정확히 맞물리는지 닫는다.
- 변경 단위:
  `README.md`, `problem/README.md`, `docs/README.md`, `vanilla/tests/*`
- 처음 가설:
  unit test만 적어 두면 semantic 구조가 실제 keyboard 흐름까지 닫힌다고 과장하게 될 수 있다고 봤다.
- 실제 진행:
  2026-03-12의 README/problem/docs polish가 포함/제외 범위를 정리한 점을 확인한 뒤, 2026-03-13에 canonical verify를 다시 실행했다. vitest는 구조/validation을, Playwright는 landmark 탐색과 keyboard submission을 맡는다.

CLI:

```bash
$ cd study
$ npm run verify --workspace @front-react/semantic-layouts-a11y
✓ vanilla/tests/validation.test.ts (2 tests)
✓ vanilla/tests/shell.test.ts (3 tests)
Test Files  2 passed (2)
Tests  5 passed (5)
Running 2 tests using 1 worker
✓ exposes landmarks, labels, and responsive grid behavior
✓ supports keyboard-only submission with visible validation messaging
2 passed (7.3s)
```

검증 신호:

- unit test `5 passed`가 구조와 validation helper를 닫았다.
- Playwright `2 passed`가 landmark 탐색과 keyboard-only submit 흐름을 따로 확인해 줬다.

핵심 코드:

```ts
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const errors = runValidation();
  if (hasValidationErrors(errors)) {
    focusFirstInvalidField(form, errors);
    return;
  }
});
```

왜 이 코드가 중요했는가:

최종적으로 이 프로젝트를 "semantic shell"이라고 부를 수 있는 이유는 submit handler가 validation 메시지와 focus 이동을 동시에 책임지기 때문이다. markup, error text, keyboard flow가 한 블록에서 만나는 순간이라서, 테스트도 바로 이 지점을 기준으로 읽히게 된다.

새로 배운 것:

- semantic 품질은 static HTML 설명만으로는 끝나지 않는다. landmark가 보이는 것과 keyboard path가 실제로 닫히는 것은 다른 문제이고, 이 프로젝트는 둘 다 verify에 포함한다.

다음:

- local persistence, routing, network state는 아직 없다. 다음 단계 `02-dom-state-and-events`에서 브라우저 state 동기화가 본격적으로 시작된다.

## 남은 경계

- local persistence와 URL state는 아직 없다.
- 실제 데이터 fetching과 라우팅은 다루지 않는다.
- keyboard interaction은 form submission 중심 흐름에 맞춰 최소 범위로 유지한다.
