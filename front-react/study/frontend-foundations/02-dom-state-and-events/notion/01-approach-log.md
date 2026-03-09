# 접근 과정: 상태의 층을 나누고 이벤트를 모으다

## 타입부터 설계하기

코드를 작성하기 전에 먼저 `types.ts`에서 데이터 구조를 고정했다. `BoardItem`, `BoardQuery`, `SelectionState`, `BoardState`라는 네 개의 인터페이스가 전체 앱의 상태를 설명한다.

이 접근이 효과적이었던 이유는, 타입을 먼저 정의하면 "어떤 상태가 있는가"와 "어떤 상태가 변하는가"를 코드 작성 전에 명확히 볼 수 있기 때문이다. 예를 들어 `SelectionState.editingId`가 `string | null`이라는 사실 하나로, 편집 모드가 토글 방식이라는 걸 바로 알 수 있다.

특히 `PersistedBoardState`를 따로 분리한 게 중요했다. 전체 `BoardState`에는 `editingId`와 `notice`가 포함되지만, localStorage에 저장할 때는 이 임시 상태를 제외해야 한다. **"무엇을 저장하는가"와 "무엇으로 작동하는가"는 다른 질문**이라는 걸 타입 수준에서 보이게 만든 것이다.

## 상태의 세 층

상태 관리에서 가장 중요한 판단은 **어디에 저장하는가**였다. 세 층으로 나눴다.

### URL (query parameter)
- 검색어, 상태 필터, 정렬 순서
- `parseQuery()`와 `serializeQuery()`가 이 경계를 담당한다
- URL은 공유 가능해야 하므로, "이 링크를 열면 같은 뷰가 보인다"는 보장이 필요하다

### localStorage
- 태스크 항목의 편집 결과, 선택된 row
- `loadPersistedState()`와 `savePersistedState()`가 담당
- 새로고침 후에도 작업 맥락이 유지되어야 하지만, 다른 사람과 공유할 필요는 없는 정보

### 메모리 (in-memory only)
- 현재 편집 중인 row (`editingId`), 상태 알림 문구 (`notice`)
- 페이지를 떠나면 사라져도 되는 임시 상태

이 분리의 핵심 효과는 `createInitialBoardState()`에서 드러난다. 이 함수는 URL query를 먼저 파싱하고, localStorage에서 가져온 값 위에 URL 값을 덮어쓴다. **URL이 localStorage보다 우선한다.** 누군가가 `?status=done` 링크를 열면, 내 로컬에 `status=open`이 저장되어 있어도 done 필터가 적용된다.

## 이벤트 위임이라는 선택

task board에는 행마다 Select, Edit, Save, Cancel 버튼이 있다. rerender할 때마다 DOM이 새로 만들어지기 때문에, 각 버튼에 개별 listener를 붙이면 매번 다시 걸어야 한다.

대신 **컨테이너 한 곳에 listener를 걸고, `data-action`과 `data-id` 속성으로 행위와 대상을 식별**하는 방식을 택했다.

```typescript
container.addEventListener("click", (event) => {
  const target = (event.target as HTMLElement)?.closest<HTMLButtonElement>("[data-action]");
  const action = target?.dataset.action;
  const itemId = target?.dataset.id;
  // ...
});
```

이 패턴의 장점은:
- rerender 후에도 listener가 유효하다 (컨테이너는 바뀌지 않으니까)
- 새로운 행이 추가되어도 listener를 다시 걸 필요가 없다
- 모든 상태 전이가 한 파일(`app.ts`) 안에서 읽힌다

처음에는 이벤트 위임이 "성능 최적화 기법"이라고만 알고 있었는데, 직접 써 보니 **구조적 단순화**가 더 큰 이유였다. 리스너가 흩어지지 않으니 "이 버튼을 누르면 무슨 일이 일어나는가"를 추적하기가 훨씬 쉬웠다.

## render 사이클: 전체를 다시 그린다

상태가 바뀔 때마다 `render()` 함수가 호출된다. 이 함수는:

1. `reconcileSelection()` — 필터 결과에 선택된 항목이 없으면 선택을 초기화
2. `container.innerHTML = getMarkup(state)` — 전체 마크업을 다시 그린다
3. `syncUrl()` — URL query를 갱신
4. `savePersistedState()` — localStorage에 저장
5. 편집 중이면 input에 focus, 아니면 지정된 요소에 focus

"전체를 다시 그린다"는 게 비효율적으로 보일 수 있지만, 이 규모에서는 문제가 없다. 오히려 **부분 갱신의 복잡성을 피하고, 상태와 화면이 항상 일치한다는 보장**을 쉽게 얻을 수 있었다.

이 방식의 한계를 체감한 건 포커스 관리에서였다. innerHTML을 교체하면 포커스가 날아가기 때문에, render 후에 명시적으로 `focus()`를 호출해야 한다. 이 "상태는 바뀌었는데 포커스가 사라지는" 문제가 결국 React의 reconciliation이 왜 필요한지를 체감하게 만드는 지점이었다.

## 인라인 편집의 의외로 복잡한 흐름

"제목을 클릭해서 수정하고 저장한다"는 단순해 보이는 기능이지만, 실제로 구현하면 신경 쓸 게 많다.

- Edit 버튼을 누르면 `editingId`가 설정되고, 해당 셀에 input이 나타난다
- render 후 그 input에 자동으로 focus + select가 되어야 한다
- Save를 누르거나 Enter를 치면 저장된다
- Cancel을 누르면 원래 제목으로 돌아간다
- 빈 제목을 저장하려 하면 거부하고 input에 다시 focus

각 전환마다 `state.selection.editingId`와 `state.notice`가 바뀌고, render 후 focus 대상이 달라진다. 이 흐름을 코드에서 추적하면 "상태 전이(state transition)"가 무엇인지 자연스럽게 체감하게 된다.
