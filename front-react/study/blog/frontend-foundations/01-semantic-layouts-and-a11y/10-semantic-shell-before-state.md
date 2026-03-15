# Semantic Shell Before State

이 프로젝트를 다시 읽으면서 가장 먼저 고쳐 잡은 해석은 "접근성 좋은 폼 예제"라는 축소였다. 실제로는 폼보다 먼저 semantic shell을 고정하는 연습에 더 가깝다. `workspaceName` 검증이나 email 정규식은 그다음 문제이고, 진짜 출발점은 skip link와 landmark, 그리고 읽기 순서가 코드 첫 화면에서 이미 드러나느냐였다.

## 구조를 먼저 고정하니 나중 로직이 DOM을 흔들지 않았다

핵심 구현은 [`vanilla/src/app.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts)의 `getAppMarkup()`에서 시작한다. 여기서 첫 줄이 skip link라는 점이 중요했다.

```ts
export function getAppMarkup(): string {
  return `
    <a class="skip-link" href="#main-content">Skip to main content</a>
    <div class="shell">
      <header class="topbar">
      ...
      <div class="workspace-grid" data-testid="workspace-grid">
        <nav class="nav-card" aria-label="Settings sections">
        ...
        <main id="main-content" tabindex="-1">
        ...
        <aside class="panel review-panel" id="review" aria-labelledby="review-heading">
```

이 마크업만 봐도 이 화면의 탐색 경로가 거의 정해진다.

- banner
- navigation
- main
- complementary aside
- skip link로 `#main-content` 점프

React도 없고 state store도 없지만, 화면을 "어떤 순서로 통과하게 만들 것인가"는 이미 여기서 끝난다. 이 순서가 먼저 고정돼 있기 때문에 뒤에서 validation 메시지와 focus 이동을 붙여도 구조를 다시 설계할 필요가 없다.

## validation은 규칙보다 projection이 더 중요했다

검증 규칙 자체는 단순하다. [`vanilla/src/validation.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts)는 trim과 email pattern만 다룬다.

```ts
if (name.length < 3) {
  errors.workspaceName =
    "Workspace name must be at least 3 characters long.";
}

if (!EMAIL_PATTERN.test(email)) {
  errors.supportEmail = "Enter a valid support email address.";
}
```

하지만 이 프로젝트가 괜찮은 이유는 규칙보다 projection이 명확하기 때문이다. `app.ts`는 같은 오류 결과를 세 군데에 동시에 투영한다.

- `aria-invalid`
- inline error text
- status live region

그리고 submit이 실패하면 첫 invalid field로 focus를 되돌린다.

```ts
if (hasValidationErrors(errors)) {
  const count = Object.values(errors).filter(Boolean).length;
  status.textContent = `Fix ${count} field${count > 1 ? "s" : ""} before saving.`;
  focusFirstInvalidField(form, errors);
  return;
}
```

blur 시점 검증도 같은 규칙 위에서만 동작한다.

```ts
FIELD_IDS.forEach((field) => {
  const input = getFieldInput(form, field);

  input?.addEventListener("blur", () => {
    runValidation(field);
  });
});
```

즉 이 화면의 포인트는 "validation 함수를 만들었다"가 아니라, semantic shell 위에 오류 상태를 일관되게 입혔다는 데 있다. 그래서 keyboard 사용자와 시각적 사용자가 같은 위치에서 같은 피드백을 받게 된다.

## responsive도 시각 효과보다 reading order 유지가 우선이었다

[`vanilla/src/styles.css`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/styles.css)를 보면 레이아웃도 꽤 의도적으로 잡혀 있다.

- 기본: 3-column grid
- `max-width: 1100px`: review panel이 아래로 내려감
- `max-width: 820px`: `grid-template-columns: 1fr`

특히 820px 이하에서 `nav-card`, `review-panel`, `main`의 order를 다시 주는 부분이 중요하다. 반응형의 목표가 단순히 "좁아지면 한 줄"이 아니라, mobile에서도 main content가 먼저 오도록 읽기 순서를 보존하는 데 있기 때문이다.

이 판단은 Playwright가 grid column 수를 직접 확인하는 이유와도 연결된다. 테스트는 추상적인 "모바일 친화적" 표현 대신, 실제 `gridTemplateColumns`가 데스크톱에서는 여러 칼럼이고 모바일에서는 한 칼럼인지 본다.

## 마지막 검증은 keyboard-only 흐름을 브라우저에서 끝까지 재생한다

이번 Todo에서 다시 돌린 검증은 아래 셋이다.

```bash
npm run build --workspace @front-react/semantic-layouts-a11y
npm run test --workspace @front-react/semantic-layouts-a11y
npm run e2e --workspace @front-react/semantic-layouts-a11y
```

결과는 다음과 같았다.

- `vite build` 통과
- `vitest`: `validation.test.ts` 2개, `shell.test.ts` 3개 통과
- `playwright`: 2개 시나리오 통과

특히 e2e는 그냥 렌더만 보는 테스트가 아니다. 실제로

1. `Tab`으로 skip link에 도달하고
2. form 필드까지 keyboard로 이동한 뒤
3. 잘못된 값을 넣어 submit 실패를 만들고
4. `"Fix 2 fields before saving."`를 확인하고
5. 첫 invalid field에 focus가 돌아오는지 확인한 다음
6. 값을 고쳐 `"Settings saved for Ops Seoul (Asia/Seoul)."`까지 확인한다

여기까지 통과한다. 이 흐름이 중요한 이유는, semantic shell이 정말로 상태 없는 정적 골격이 아니라 keyboard interaction을 버틸 수 있는 기반인지 브라우저에서 확인해 준다는 점이다.

## 그래서 이 프로젝트의 진짜 성과는 작지만 선명하다

여기에는 persistence도 없고 routing도 없고 fetch도 없다. 하지만 바로 그 제한 덕분에 한 가지가 또렷해진다. 상태를 붙이기 전에 semantic shell을 먼저 고정하면, 이후 로직은 화면 구조를 흔드는 대신 이미 읽히는 골격 위에 얹히게 된다.

다음 단계인 `02-dom-state-and-events`는 그 위에서야 비로소 묻게 된다. 구조가 고정된 뒤, URL state와 local state를 어디서 나눌 것인가. 이 프로젝트는 그 질문보다 앞선, 더 기초적이고 더 자주 흔들리는 부분을 먼저 고쳐 놓는 역할을 한다.
