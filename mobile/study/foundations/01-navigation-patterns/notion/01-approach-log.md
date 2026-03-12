# 01 — Approach Log: 네비게이션 구현 과정

## Phase 1: 타입 정의부터 시작하기

네비게이션 구현의 첫 단추는 화면 목록이 아니라 **ParamList 타입 정의**였다.
`types.ts`에서 네 개의 ParamList를 선언했다:

```
HomeStackParamList   → Home, Detail({id, title}), Settings, ProfileDetail({userId})
ProfileStackParamList → ProfileHub({userId}), EditProfile
RootTabParamList     → HomeTab(↗HomeStack), SearchTab, ProfileTab(↗ProfileStack)
RootDrawerParamList  → Main(↗RootTab), Notifications, About
RootStackParamList   → Drawer(↗RootDrawer), NotFound
```

이 타입 계층이 중요한 이유는 `NavigatorScreenParams<>`가 하위 navigator의 params를 상위로 끌어올리기 때문이다.
`RootTabParamList`의 `HomeTab`은 `NavigatorScreenParams<HomeStackParamList>` 타입을 가지고,
이는 다시 `RootDrawerParamList.Main`으로, 최종적으로 `RootStackParamList.Drawer`로 합성된다.
덕분에 어디서든 `navigate()`를 호출하면 최하위 화면의 params까지 타입 체크가 걸린다.

각 화면의 Props도 React Navigation이 제공하는 제네릭으로 추출했다.
`StackScreenProps<HomeStackParamList, 'Detail'>`처럼 navigator 종류에 맞는 Props 타입을 사용하면
`navigation`과 `route` 객체가 정확한 타입을 가진다.

## Phase 2: HomeStack — 기본 Stack 흐름 구축

가장 안쪽 navigator인 HomeStack부터 만들었다.
네 개 화면(Home → Detail → Settings → ProfileDetail)을 Stack으로 연결하고,
각 화면에서 `navigation.navigate()`로 다음 화면을 push하는 기본 흐름을 확인했다.

이 단계에서 두 가지 커스터마이징을 적용했다:

### Detail 화면의 vertical transition

`detailTransition` 객체는 `gestureDirection: 'vertical'`과 커스텀 `cardStyleInterpolator`를 정의한다.
화면이 아래에서 위로 올라오면서 opacity가 0.82에서 1로 변하는 효과다.
`TransitionSpecs.TransitionIOSSpec`을 open/close 모두에 사용해 iOS 네이티브와 유사한 타이밍을 얻었다.

### ProfileDetail 화면의 fade from center

`CardStyleInterpolators.forFadeFromCenter`를 옵션으로 넘기면 화면이 중앙에서 fade-in된다.
같은 Stack 안에서도 화면마다 전환 애니메이션을 다르게 줄 수 있다는 것을 보여주는 예시다.

### Custom Header — AppHeader 컴포넌트

기본 header 대신 `AppHeader`를 모든 Stack 화면에 적용했다.
`StackHeaderProps`를 받아 `back` 존재 여부로 Back/Menu 버튼을 전환하고,
`titleMap` 딕셔너리로 route name을 사용자 친화적인 제목으로 매핑한다.
Root 화면에서는 Menu 버튼이 Drawer를 열고, 하위 화면에서는 Back 버튼이 `goBack()`을 호출한다.

## Phase 3: ProfileStack과 Tab Navigator 구성

HomeStack 옆에 ProfileStack을 만들고, 이 둘을 Bottom Tab Navigator로 묶었다.

```
MainTabs
├── HomeTab → HomeStackNavigator
├── SearchTab → SearchScreen (단독)
└── ProfileTab → ProfileStackNavigator
```

Tab 구성에서 주의한 점:

- **`headerShown: false`**: 탭 레벨에서는 header를 숨기고, 각 Stack navigator가 자체 header를 보여준다. SearchTab처럼 Stack 없이 바로 화면을 넣으면 header가 없으므로 ScreenShell 자체가 전체 UI를 담당한다.
- **`lazy: true`**: 탭 컨텐츠가 처음 방문할 때 mount된다. 이 설정이 없으면 모든 탭이 앱 시작 시 동시에 렌더링된다.
- **Badge**: SearchTab에 `tabBarBadge`로 `notificationCount`를 표시한다. 이 값은 Drawer의 session state에서 내려온다.
- **TabIcon**: 텍스트 기반 glyph(◎, ◇, ▲)를 사용한 간결한 아이콘 컴포넌트. focus 상태에 따라 배경색과 글자색이 바뀐다.

SearchScreen은 `useState`로 로컬 상태(tapCount, draft)를 유지하는 의도적인 설계다.
다른 탭으로 갔다가 돌아와도 카운터와 텍스트 입력이 그대로 남아 있어야 탭의 상태 보존 동작을 확인할 수 있다.

## Phase 4: Drawer Navigator — 인증 상태와 커스텀 컨텐츠

Drawer는 TabNavigator를 감싸는 바깥 레이어다.

```
DrawerNavigator
├── Main → MainTabs (headerShown: false)
├── Notifications → NotificationsScreen
└── About → AboutScreen
```

Drawer의 핵심은 `CustomDrawerContent`다. 단순한 메뉴 리스트가 아니라 다음 요소를 포함한다:

1. **Hero 영역**: "Nested navigation lab"이라는 제목과 설명, 로그인 상태 chip
2. **Conditional items**: `session.isSignedIn`이 true면 Notifications와 Log out이 보이고, false면 Sign in만 보인다.
3. **Sign in/out 동작**: Sign in하면 ProfileTab > ProfileHub로 이동하고, Log out하면 HomeTab으로 돌아간다.

session 상태는 `DrawerNavigator` 컴포넌트 내부의 `useState`로 관리한다.
`useMemo`로 `drawerContent` 렌더 함수를 메모이제이션해서 session이 바뀔 때만 drawer가 다시 그려지도록 했다.

`notificationCount`는 session state에서 MainTabs로 prop으로 전달되어 SearchTab의 badge에 반영된다.
이 흐름은 Drawer → Tab 간 데이터가 어떻게 흘러가는지 보여주는 예시이기도 하다.

## Phase 5: RootStack과 Deep Link 연결

모든 navigator 위에 RootStack을 하나 더 쌓았다.

```
RootStack
├── Drawer → DrawerNavigator
└── NotFound → NotFoundScreen (presentation: 'modal')
```

이 구조의 이유는 Deep Link에서 등록되지 않은 path를 `NotFound`로 보내기 위함이다.
NotFound가 Drawer 안에 있으면 drawer 메뉴가 함께 보이게 되는데, 이는 원치 않는 동작이다.
RootStack 레벨에 두고 `presentation: 'modal'`로 설정하면 기존 화면 위에 모달로 뜬다.

### linking.ts — URL to State 매핑

`linking` 객체는 `config.screens`에 중첩 navigator 구조를 그대로 반영한다:

```
Drawer → Main → HomeTab → Home: 'home'
                          Detail: 'detail/:id'
                          Settings: 'settings'
                          ProfileDetail: 'home-profile/:userId'
                SearchTab: 'search'
                ProfileTab → ProfileHub: 'profile/:userId'
                             EditProfile: 'profile/edit'
         Notifications: 'notifications'
         About: 'about'
NotFound: '*'
```

### resolveNavigationState — State Hydration

`resolveNavigationState()` 함수는 URL을 받아 React Navigation의 `getStateFromPath()`로 state를 만든 뒤,
`visitRoutes()`로 모든 route를 순회하면서 Detail 화면에 `title` 파라미터를 보완한다.
URL에는 `id`만 넣고 `title`은 `buildDetailTitle()`로 생성하는 전략이다.

이 접근이 의미 있는 이유는 URL을 깔끔하게 유지하면서도 화면에 필요한 데이터를 모두 채울 수 있기 때문이다.
실무에서는 이 단계에서 API 호출이나 캐시 조회가 들어갈 수 있다.

## Phase 6: App.tsx — 진입점 조립

`App.tsx`는 모든 것을 조립하는 지점이다:

1. `GestureHandlerRootView` — Drawer와 Stack의 gesture 지원
2. `SafeAreaProvider` — 노치/홈 인디케이터 영역 처리
3. `NavigationContainer` — `linking`, `navigationTheme`, `initialState` 주입
4. `RootNavigator` — 최상위 Stack

`initialState` prop은 테스트에서 특정 화면 상태로 앱을 시작할 때 사용한다.
프로덕션에서는 linking이 URL을 파싱해 initialState를 대신 생성한다.

## 전체 Navigator 동작 확인 체크리스트

- [x] Home → Detail(vertical slide) → Settings → ProfileDetail(fade) 순서 push/pop
- [x] 탭 전환 후 SearchTab 로컬 상태(tapCount, draft) 유지
- [x] Drawer에서 Sign in/out에 따라 메뉴 항목 변화
- [x] `myapp://detail/abc123` → RootStack → Drawer → Main → HomeTab → Detail 도달
- [x] `myapp://unknown` → NotFound modal 표시
- [x] 모든 navigate() 호출에 TypeScript 타입 에러 없음
