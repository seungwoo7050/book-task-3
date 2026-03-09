# 디버그 기록: 부딪힌 것들과 해결 과정

## aria-describedby 순서 문제

처음에 `aria-describedby`에 error만 연결하고 help text를 빠뜨렸다. 스크린리더로 테스트해 보니 입력 필드에 포커스했을 때 "Workspace name"이라는 label만 읽히고, 그 필드가 뭘 위한 것인지 설명이 없었다. help text의 id를 `aria-describedby`에 추가하니 "Workspace name, Shown in internal dashboards and review queues"로 읽혀서 맥락이 드러났다.

이 경험에서 배운 건, **`aria-describedby`는 공백으로 여러 id를 받을 수 있고, 나열 순서대로 읽힌다**는 점이다. help을 먼저, error를 뒤에 두면 평소에는 도움말이 읽히고, 에러가 있을 때는 도움말 뒤에 에러가 이어진다.

## hidden error element의 존재 이유

처음에는 에러가 없을 때 error element를 아예 DOM에서 제거했다. 제출 시 동적으로 삽입하는 방식이었는데, 이러면 `aria-describedby`가 가리키는 id가 일시적으로 존재하지 않는 상태가 된다. 일부 스크린리더는 이 불일치를 조용히 무시하지만, 일부는 오류를 발생시킨다.

해결은 단순했다. error element를 항상 DOM에 두되 `hidden` 속성으로 가린다. 에러가 생기면 `hidden`을 제거하고 텍스트를 채우고, 에러가 해소되면 다시 `hidden`과 빈 텍스트로 되돌린다. DOM 구조가 변하지 않으니 `aria-describedby` 관계가 항상 유효하다.

## 포커스가 안 보이는 문제

초기 CSS에서 `outline: none`을 전역으로 넣어 놓았다가, 키보드로 탭했을 때 현재 어떤 요소에 포커스가 있는지 전혀 알 수 없는 상태가 됐다. 마우스 클릭 시에는 괜찮지만; 키보드 사용자에게는 치명적이다.

`:focus-visible`을 사용해서 키보드 포커스일 때만 outline을 보이게 수정했다. 마우스 클릭에는 outline이 나타나지 않고, Tab 키로 이동할 때만 선명한 outline이 보인다.

## submit 타이밍과 aria-live 충돌

submit 핸들러에서 `status.textContent`를 갱신한 뒤에 `focusFirstInvalidField()`를 호출했는데, 스크린리더가 상태 메시지와 포커스 이동을 거의 동시에 읽으려고 해서 하나가 씹히는 현상이 있었다.

해결은 순서를 조정하는 것이었다. 먼저 `updateErrorState()`로 개별 필드의 시각적/ARIA 상태를 갱신하고, 그 다음에 상태 텍스트를 업데이트하고, 마지막에 포커스를 옮겼다. `aria-live="polite"`는 현재 읽고 있는 내용이 끝난 뒤에 알려 주기 때문에, 포커스 이동 후에 자연스럽게 상태 메시지가 읽힌다.

## Playwright에서 포커스 검증

E2E 테스트에서 키보드만으로 폼을 조작하는 시나리오를 작성할 때, Tab 키를 몇 번 눌러야 원하는 필드에 도달하는지를 정확히 세야 했다. skip link가 첫 번째 focusable이고, 그 다음이 nav 링크 3개, 그 다음이 input 필드라는 순서를 코드에서 직접 확인하고 테스트에 반영했다.

이 과정에서 "포커스 순서가 DOM 순서를 따른다"는 원칙을 실제로 체감했다. CSS로 시각적 위치를 바꿔도 Tab 순서는 DOM 순서를 그대로 따르기 때문에, **마크업 순서를 먼저 올바르게 잡는 것이 접근성의 기초**라는 확신이 생겼다.
