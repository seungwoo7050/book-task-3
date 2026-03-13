# Semantic Shell Before State

이 프로젝트를 다시 읽다 보면 가장 먼저 드는 생각이 있다. 아직 데이터도 없고, 저장도 없고, 라우팅도 없는데 왜 이렇게 구조 이야기를 오래 하는가. 그런데 코드를 따라가 보면 바로 이유가 나온다. 이 화면의 출발점은 "무엇을 저장할 것인가"가 아니라 "사용자가 이 화면을 어떤 순서로 읽고 통과할 것인가"였기 때문이다.

설정형 UI는 대개 상태와 폼 검증 이야기로 바로 들어가기 쉽다. 하지만 여기서는 순서를 거꾸로 잡았다. 먼저 `header`, `main`, skip link, form grouping, status message가 놓일 자리를 고정하고, 그 다음에야 validation을 붙였다. 그 덕분에 뒤에 나오는 로직은 DOM을 다시 설계하는 대신 이미 정해 둔 구조를 채우는 쪽으로 흘렀다.

브라우저가 기본으로 주는 semantic surface를 충분히 믿어 보면, 접근성은 마지막 polish가 아니라 처음부터 선택해야 하는 아키텍처라는 사실이 선명해진다. 이 글은 바로 그 첫 선택이 어떻게 다음 단계의 복잡도를 줄였는지 복원하는 기록이다.

## 구현 순서를 먼저 짚으면

- semantic shell과 landmark를 먼저 만들어 "읽히는 순서"를 고정했다.
- validation은 `SettingsValues -> SettingsErrors`라는 순수 함수로 닫고, DOM 레이어는 그 결과를 투영하는 역할만 맡겼다.
- 마지막에는 `npm run verify`로 keyboard-only 흐름과 landmark 탐색이 실제 브라우저에서도 유지되는지 확인했다.

## 화면을 꾸미기 전에 먼저 읽히는 구조를 못 박았다

이 프로젝트의 첫 전환점은 화려한 위젯이 아니라 skip link였다. `getAppMarkup()`를 보면 제일 앞에 `Skip to main content`가 나오고, 그 뒤로 topbar와 settings form이 landmark 안에 배치된다. 이 짧은 마크업 조각이 이후 모든 판단의 기준점이 됐다.

```ts
export function getAppMarkup(): string {
  return `
    <a class="skip-link" href="#main-content">Skip to main content</a>
    <div class="shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Foundations 01</p>
          <h1 class="title">Accessible workspace settings shell</h1>
```

중요한 건 이 코드가 예뻐서가 아니다. landmark와 reading order를 먼저 못 박아 두니, 뒤에서 validation message를 넣거나 focus를 이동시킬 때 "어디에 붙여야 하는가"를 다시 고민할 필요가 없었다. 구조가 먼저 서 있으니 로직은 그 구조에 맞게만 흘렀다.

이 판단은 docs에서도 그대로 드러난다. `docs/concepts/semantic-layout-decisions.md`는 responsive 기준조차 "컬럼 수"가 아니라 "reading order 보존"으로 잡았다고 설명한다. 즉 이 프로젝트는 처음부터 레이아웃을 상태의 배경이 아니라 품질 기준 자체로 다룬 셈이다.

## validation을 DOM 바깥으로 밀어내자 흐름이 단순해졌다

두 번째 전환점은 검증 규칙을 `validation.ts`의 순수 함수로 밀어낸 것이다. `validateSettings()`는 trim과 email 정규식만 책임지고, `app.ts`는 그 결과를 받아 `aria-invalid`, inline error, status live region, focus 이동으로 바꾼다.

```ts
export function validateSettings(values: SettingsValues): SettingsErrors {
  const errors: SettingsErrors = {};
  const name = values.workspaceName.trim();
  const email = values.supportEmail.trim();

  if (name.length < 3) {
    errors.workspaceName = "Workspace name must be at least 3 characters long.";
  }
  if (!EMAIL_PATTERN.test(email)) {
    errors.supportEmail = "Enter a valid support email address.";
  }
  return errors;
}
```

이 분리가 좋았던 이유는 blur 검증과 submit 검증이 같은 규칙을 그대로 재사용할 수 있기 때문이다. 실제 `runValidation()`은 field-level 검증과 full-form 검증을 같은 함수로 처리하고, submit 시에는 첫 번째 invalid field로 focus를 되돌린다.

```ts
const runValidation = (targetField?: typeof FIELD_IDS[number]) => {
  const errors = validateSettings(extractValues(form));
  if (targetField) {
    updateErrorState(form, { [targetField]: errors[targetField] });
    return errors;
  }
  updateErrorState(form, errors);
  return errors;
};
```

여기서 배운 건 validation의 핵심이 정규식이 아니라 projection이라는 점이었다. 같은 오류 결과가 live region에도, inline text에도, focus 이동에도 동시에 반영되어야만 keyboard 사용자와 시각적 사용자가 같은 상태를 공유할 수 있다.

## 마지막에는 브라우저에서 keyboard path를 다시 확인했다

이 프로젝트는 코드만 보면 소박하지만, 검증은 소박하지 않다. 단위 테스트로 검증 규칙과 shell 구조를 먼저 고정하고, 그다음 Playwright로 landmark 탐색과 keyboard-only submit을 끝까지 재생한다.

```bash
cd study
npm run verify --workspace @front-react/semantic-layouts-a11y
```

2026-03-13 replay 기준으로 `vitest`는 5개 테스트가, `playwright`는 2개 시나리오가 모두 통과했다. 특히 브라우저 시나리오는 landmark 노출과 keyboard-only submission을 함께 다룬다. 이게 중요했던 이유는 접근성 품질이 함수 단위 검증만으로는 완성되지 않기 때문이다. 실제 focus 이동과 읽기 순서는 결국 브라우저에서 확인해야 한다.

blur 시점 검증을 붙인 부분도 같은 맥락에서 읽힌다. 저장 버튼을 누를 때만 갑자기 빨간 메시지를 쏟아내는 대신, 사용자가 필드를 빠져나가는 순간 현재 위치의 문제를 알려 주도록 한 것이다.

```ts
FIELD_IDS.forEach((field) => {
  const input = getFieldInput(form, field);
  input?.addEventListener("blur", () => {
    runValidation(field);
  });
});
```

이 조각은 작지만, 이 프로젝트가 접근성을 "나중에 붙이는 경고 문구"가 아니라 사용자가 화면을 통과하는 흐름 전체로 다뤘다는 사실을 잘 보여 준다.

## 무엇이 아직 남았는가

이 화면은 여전히 작다. persistence도 없고, 실제 라우팅도 없고, 네트워크 상태도 없다. 하지만 바로 그 제한 덕분에 하나는 분명하게 남았다. 상태 로직이 복잡해지기 전에 semantic shell을 먼저 고정하면, 나중에 붙는 기능이 구조를 흔드는 일이 훨씬 줄어든다.

다음 질문은 자연스럽다. 구조가 고정된 뒤에는 상태를 어디에 둘 것인가. `02-dom-state-and-events`는 바로 그 문제, 즉 URL state와 local UI state를 어떤 경계로 나눌지를 본격적으로 다룬다.
