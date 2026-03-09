# 접근 과정: 셸을 세우고 관계를 잡다

## 마크업 먼저, 스타일은 나중에

처음에는 빈 HTML 파일 하나와 TypeScript 진입점만 있었다. `index.html`에 `<div id="app">`을 놓고, `vanilla/src/main.ts`에서 그 컨테이너를 받아 `mountSettingsShell()`을 호출하는 구조다.

의식적으로 markup-first 접근을 택했다. `getAppMarkup()` 함수가 전체 HTML 문자열을 반환하는 방식인데, 이렇게 하면 시맨틱 구조를 **코드 안에서 한눈에 볼 수 있다.** JSX나 템플릿 분리 없이, HTML의 구조가 곧 설계 의도가 되는 셈이다.

마크업을 작성할 때 가장 먼저 고정한 것은 **landmark 순서**였다.

1. `<header>` — 페이지 제목과 학습 포커스 태그
2. `<nav aria-label="Settings sections">` — 섹션 내비게이션
3. `<main id="main-content">` — 핵심 폼 영역
4. `<aside aria-labelledby="review-heading">` — 검증 체크리스트

이 순서를 먼저 잡아 놓으니, 이후에 CSS grid를 붙이거나 반응형으로 바꿀 때도 DOM 순서를 건드릴 필요가 없었다.

## 폼 관계 설계: label만으로는 부족하다

폼을 만들 때 흔히 `<label for="...">`까지만 연결하고 끝내는 경우가 많다. 하지만 이 프로젝트에서는 **label, help text, error text 세 요소의 관계**를 명시적으로 고정하는 게 핵심이었다.

```html
<label for="workspaceName">Workspace name</label>
<input id="workspaceName" aria-describedby="workspaceName-help workspaceName-error" />
<p id="workspaceName-help">Shown in internal dashboards and review queues.</p>
<p id="workspaceName-error" hidden></p>
```

`aria-describedby`에 help과 error를 동시에 연결해 두면, 스크린리더가 입력 필드에 포커스했을 때 "Workspace name, Shown in internal dashboards..."를 읽어 준다. 에러가 있으면 에러 메시지도 함께 읽힌다. **에러가 없을 때도 error element는 DOM에 남겨 두되 `hidden`으로 처리**했는데, 이렇게 하면 에러가 발생했을 때 새 요소를 삽입하지 않고도 관계가 유지된다.

## validation 분리: UI와 로직의 경계

validation 로직은 `validation.ts`로 분리했다. `validateSettings()`는 순수 함수로, 값을 받아 에러 객체를 반환한다. DOM을 전혀 모르는 함수다.

이렇게 분리한 이유는 테스트 때문이다. DOM 테스트와 로직 테스트를 따로 돌릴 수 있고, validation 규칙이 바뀌어도 UI 코드를 건드리지 않아도 된다.

## 포커스 관리라는 숨은 난이도

"에러가 있으면 첫 번째 잘못된 필드로 포커스를 옮긴다"는 한 줄짜리 요구사항이지만, 실제로 구현하면 생각할 게 꽤 있다.

- `FIELD_IDS` 배열의 순서대로 검사해서 **첫 번째** invalid 필드를 찾는다.
- 해당 input에 `aria-invalid="true"`를 설정하고 `.focus()`를 호출한다.
- 상태 메시지를 `role="status" aria-live="polite"` 영역에 업데이트한다.

이 세 가지가 맞물려야 키보드 사용자가 "무엇이 잘못됐는지"와 "어디를 고쳐야 하는지"를 동시에 알 수 있다. 실제로 처음에는 `aria-live` 영역 업데이트 타이밍을 놓치는 실수가 있었는데, submit 핸들러 안에서 에러 카운트를 먼저 세고 나서 상태 텍스트를 갱신하는 순서로 해결했다.

## blur 재검증: 과하지 않은 피드백

한 가지 더 추가한 패턴이 있다. submit이 아니라 blur(포커스 이탈) 시에도 해당 필드만 검증하는 것이다.

```typescript
FIELD_IDS.forEach((field) => {
  input?.addEventListener("blur", () => {
    runValidation(field);
  });
});
```

전체 폼을 다시 검증하지 않고, 방금 떠난 필드만 얇게 검증한다. 이렇게 하면 사용자가 다른 필드를 작성하는 중에 불필요한 에러 메시지가 뜨지 않으면서도, 고친 필드의 에러가 바로 사라지는 피드백을 줄 수 있다.

## 반응형: 컬럼 수가 아니라 읽기 순서

CSS에서 `grid-template-columns: minmax(220px, 280px) minmax(0, 1fr) minmax(240px, 320px)`을 사용했다. 좁은 뷰포트에서는 자연스럽게 한 컬럼으로 쌓이는데, 이때 **DOM 순서상 main이 nav보다 뒤에 오지만, 한 컬럼에서는 nav → main → aside 순서가 유지**된다.

반응형 기준을 "몇 px에서 깨지는가"가 아니라 "reading order가 보존되는가"로 잡은 것은 접근성 관점에서 중요한 판단이었다. 스크린리더는 시각적 레이아웃이 아니라 DOM 순서를 따르기 때문이다.
