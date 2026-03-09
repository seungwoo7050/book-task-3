# 디버그 기록: 상태 동기화에서 부딪힌 것들

## 필터 변경 후 선택이 사라지는 문제

필터를 바꿨을 때, 이전에 선택한 행이 필터 결과에 없으면 어떻게 해야 할까? 처음에는 `selectedId`를 그대로 유지했는데, 디테일 패널이 "선택된 항목의 정보"를 보여 주려고 하면서 빈 데이터를 참조해 깨지는 문제가 생겼다.

해결은 `reconcileSelection()` 함수를 만든 것이다. render 직전에 호출되는 이 함수가 "현재 보이는 항목 중에 선택된 것이 있는가"를 확인하고, 없으면 첫 번째 보이는 항목으로 자동 전환한다. editingId도 마찬가지다.

이 함수가 없었으면 **"상태는 유효하지만 화면에서는 의미 없는" 상태**가 계속 남았을 것이다. "상태 정합성(state consistency)"이 단순히 값이 맞는지가 아니라, 현재 UI 맥락에서 의미가 있는지까지 포함한다는 걸 배웠다.

## URL과 localStorage의 우선순위 충돌

처음에는 localStorage 값을 먼저 로드하고 URL을 무시했다. 그런데 이러면 `?status=done` 같은 공유 링크가 작동하지 않는다. 내 로컬에 저장된 필터가 항상 이기기 때문이다.

수정은 `createInitialBoardState()`에서 merge 순서를 바꾸는 것이었다.

```typescript
const query = {
  ...DEFAULT_QUERY,        // 1. 기본값
  ...(persisted?.query),   // 2. localStorage 복원
  ...parseQuery(search),   // 3. URL이 최종 덮어쓰기
};
```

이 순서를 정하고 나서야 "URL은 현재 뷰를 강제하고, localStorage는 개인 맥락을 복원한다"는 역할 구분이 명확해졌다.

## innerHTML 교체 후 포커스 소실

가장 많이 부딪힌 문제다. `container.innerHTML = getMarkup(state)`를 호출하면 기존 DOM이 전부 교체되면서, 사용자가 마지막으로 포커스하고 있던 요소가 사라진다.

예를 들어 검색창에 타이핑하면, 글자 하나마다 `input` 이벤트가 발생하고, 상태가 바뀌고, render가 호출되어 전체 DOM이 교체된다. 그럼 검색창의 포커스가 날아가서 더 이상 타이핑할 수 없다.

해결은 render 함수에서 **상태별로 focus 대상을 명시적으로 지정**하는 것이었다.

- 검색 중이면 → `#searchInput`에 focus
- 편집 중이면 → `[data-edit-id]` input에 focus + select
- 행 선택 시 → 해당 행의 select 버튼에 focus

이 문제를 겪으면서 "Virtual DOM과 reconciliation이 왜 필요한지"를 정말로 체감했다. React의 diff/patch는 바뀐 부분만 업데이트하기 때문에 포커스가 유지된다. 전체를 교체하는 방식은 단순하지만, UI가 조금만 복잡해져도 포커스 관리가 급격히 어려워진다.

## Enter 키 저장과 form submit 충돌

편집 input에서 Enter를 누르면 저장되게 하고 싶었는데, input이 form 안에 있어서 Enter가 form submit을 트리거하는 문제가 있었다. 검색/필터 form과 테이블이 같은 main 안에 있었기 때문이다.

해결은 `keydown` 이벤트에서 `event.preventDefault()`를 호출하는 것이었다. `[data-edit-id]` 선택자에 매칭되는 input에서 Enter가 눌리면, 기본 submit 동작을 막고 직접 save 로직을 실행한다.

## selectionState 변경 시 notice 메시지 누락

처음에는 selection이 바뀔 때 `notice`를 업데이트하지 않았다. 화면에서는 디테일 패널이 바뀌니까 시각적으로는 문제가 없어 보였지만, `aria-live="polite"` 영역이 변화를 알려 주지 않으니 스크린리더 사용자는 무엇이 바뀌었는지 알 수 없었다.

모든 상태 전이에 notice 메시지를 추가하니, 선택, 편집 시작, 저장, 취소 각각의 동작이 명시적으로 알려졌다. "Selected task-102", "Editing task-102", "Saved title update for task-102" 같은 메시지가 `role="status"` 영역에 표시된다.
