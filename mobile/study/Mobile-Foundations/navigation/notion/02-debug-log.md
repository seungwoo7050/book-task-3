# 02 — Debug Log: 네비게이션 디버깅 기록

## Issue 1: 중첩 navigator에서 dispatch가 올바른 레이어에 도달하지 않는 문제

### 증상

HomeScreen에서 Drawer를 열려고 `navigation.dispatch(DrawerActions.openDrawer())`를 호출했으나 아무 반응이 없었다.
에러는 발생하지 않고 단순히 무시되었다.

### 원인

HomeScreen의 `navigation`은 HomeStack의 navigator에 바인딩되어 있다.
Stack navigator는 drawer action을 처리할 수 없으므로 dispatch가 무시된다.
Drawer action을 처리하려면 DrawerNavigator 레벨의 navigation 객체가 필요하다.

### 해결

`navigation.getParent()`를 사용해 상위 navigator의 navigation 객체를 얻었다.
HomeScreen 기준으로 부모 체인은 HomeStack → Tabs → Drawer이므로 `getParent()?.getParent()`로 두 단계를 거슬러 올라갔다:

```typescript
navigation.getParent()?.getParent()?.dispatch(DrawerActions.openDrawer())
```

SearchScreen에서는 부모 체인이 Tabs → Drawer이므로 `getParent()` 한 번만 호출하면 된다.
이 차이는 SearchScreen이 Stack 없이 Tab에 직접 등록된 화면이기 때문이다.

### 교훈

`getParent()` 체인의 깊이는 navigator 중첩 구조에 따라 달라진다.
하드코딩된 `getParent()?.getParent()`는 구조가 바뀌면 깨지므로, 실무에서는 navigator에 `id`를 부여하고
`getParent(id)`로 특정 navigator를 직접 참조하는 방식이 안전하다.

---

## Issue 2: Deep Link에서 Detail 화면의 title이 undefined로 표시

### 증상

`myapp://detail/abc123` URL로 앱을 열면 Detail 화면은 도달하지만, `route.params.title`이 undefined였다.
화면의 제목 영역이 비어 있었다.

### 원인

linking config에서 `'detail/:id'`는 URL의 `:id` 부분만 params로 추출한다.
`title`은 URL에 포함되지 않으므로 `getStateFromPath()`가 생성한 state에 title이 없다.

### 해결

`resolveNavigationState()` 함수에서 state를 순회하며 Detail route를 찾아 title을 보완하는 로직을 추가했다:

```typescript
visitRoutes(state, route => {
  if (route.name !== 'Detail') return;
  const params = route.params as { id: string; title?: string } | undefined;
  if (params?.id && !params.title) {
    route.params = { ...params, title: buildDetailTitle(params.id) };
  }
});
```

`buildDetailTitle()`은 id에서 하이픈/언더스코어를 공백으로 바꿔 읽기 좋은 제목을 생성한다.
state를 deep-clone한 뒤 수정하므로 원본 state에는 영향을 주지 않는다.

### 교훈

URL에는 식별자만 넣고, 표시용 데이터는 state hydration 단계에서 보완하는 패턴이 유용하다.
URL을 깨끗하게 유지하면서도 화면에 필요한 모든 데이터를 채울 수 있다.

---

## Issue 3: Notification badge가 Drawer 상태 변화를 반영하지 않음

### 증상

Drawer에서 Sign out한 뒤에도 SearchTab의 badge 숫자가 그대로 남아 있었다.

### 원인

초기 구현에서 `notificationCount`를 MainTabs 내부의 별도 state로 관리했다.
Drawer의 session 상태와 연동되지 않아 값이 동기화되지 않았다.

### 해결

`notificationCount`를 `DrawerNavigator`의 `SessionState`에 통합하고,
`MainTabs`에 prop으로 전달하는 구조로 변경했다:

```typescript
function DrawerNavigator() {
  const [session, setSession] = useState<SessionState>({
    isSignedIn: true,
    notificationCount: 3,
  });
  // ...
  <MainTabs notificationCount={session.notificationCount} />
}
```

이렇게 하면 session 상태가 바뀔 때 badge도 함께 업데이트된다.

### 교훈

중첩 navigator 사이에서 공유 상태를 전달하는 가장 간단한 방법은 prop drilling이다.
규모가 커지면 Context나 전역 상태 관리가 필요하지만,
학습 프로젝트 수준에서는 명시적인 prop 전달이 데이터 흐름을 이해하기 가장 좋다.

---

## Issue 4: 탭 전환 시 Stack 화면이 초기화되는 것처럼 보이는 현상

### 증상

HomeTab에서 Detail → Settings까지 push한 후 SearchTab으로 이동했다가 다시 HomeTab으로 돌아오면,
Settings 화면이 아닌 Home 화면이 보였다.

### 분석

이것은 버그가 아니라 React Navigation의 기본 동작이다.
탭 전환 시 Stack의 mount 상태는 유지되지만, 탭의 기본 동작은 해당 탭의 initial route로 돌아가는 것이다.
`tabBarButton`의 기본 `onPress`가 `popToTop()`과 유사한 동작을 한다.

### 해결

이 프로젝트에서는 기본 동작을 그대로 유지하기로 결정했다.
대부분의 앱에서 탭을 누르면 해당 탭의 첫 화면으로 돌아가는 것이 사용자 기대와 일치하기 때문이다.
만약 Stack 상태를 유지하고 싶다면 `unmountOnBlur: false`(기본값)와 함께 탭 버튼의 `onPress`를 커스터마이징해야 한다.

### 교훈

mount/unmount와 focus/blur는 별개의 개념이다.
탭 전환 시 컴포넌트가 unmount되지 않더라도 navigation state는 리셋될 수 있다.
`useFocusEffect`와 `useIsFocused`로 focus 상태에 반응하는 것이 탭 기반 앱에서 올바른 패턴이다.

---

## Issue 5: Custom header에서 drawer open이 Stack 하위 화면에서도 동작하는 문제

### 증상

Detail 화면에서 AppHeader의 왼쪽 버튼이 Back이어야 하는데 Menu 버튼이 표시되거나,
반대로 Home 화면에서 Back 버튼이 표시되는 경우가 있었다.

### 원인

`StackHeaderProps`의 `back` 프로퍼티를 확인하지 않고 항상 같은 동작을 실행했다.

### 해결

`back`이 존재하면 `goBack()`, 없으면 `DrawerActions.openDrawer()`를 실행하도록 분기했다:

```typescript
if (back) {
  navigation.goBack();
  return;
}
navigation.dispatch(DrawerActions.openDrawer());
```

또한 버튼 레이블도 `back ? 'Back' : 'Menu'`로, mode chip도 `back ? 'Flow' : 'Root'`로 상태를 시각적으로 표현했다.

### 교훈

Custom header는 Stack navigator의 context 정보(`back`, `route`, `options`)를 모두 활용해야
기본 header와 동일한 수준의 동작을 보장할 수 있다.
