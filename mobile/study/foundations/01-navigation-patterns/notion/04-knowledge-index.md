# 04 — Knowledge Index: 네비게이션 패턴 빠른 참조

## 소스 파일 맵

| 파일 | 역할 |
|------|------|
| `react-native/App.tsx` | 진입점. NavigationContainer에 linking, theme, initialState 주입 |
| `src/navigation/types.ts` | 5개 ParamList 타입 + 10개 Screen Props 타입 정의 |
| `src/navigation/RootNavigator.tsx` | RootStack, Drawer, Tabs, HomeStack, ProfileStack 전체 navigator 트리 |
| `src/navigation/linking.ts` | Deep link URL → state 매핑 config + `resolveNavigationState()` |
| `src/screens/AppScreens.tsx` | 10개 화면 컴포넌트 (Home, Detail, Settings, ProfileDetail, Search, ProfileHub, EditProfile, Notifications, About, NotFound) |
| `src/components/AppHeader.tsx` | Custom Stack header. back 여부로 Back/Menu 전환 |
| `src/theme.ts` | palette 색상 토큰 + React Navigation theme 커스터마이징 |

## Navigator 계층 구조

```
RootStack (createStackNavigator)
├── Drawer (createDrawerNavigator)
│   ├── Main (createBottomTabNavigator)
│   │   ├── HomeTab → HomeStack (createStackNavigator)
│   │   │   ├── Home
│   │   │   ├── Detail (vertical transition)
│   │   │   ├── Settings
│   │   │   └── ProfileDetail (fade from center)
│   │   ├── SearchTab → SearchScreen (직접)
│   │   └── ProfileTab → ProfileStack (createStackNavigator)
│   │       ├── ProfileHub (initialParams: userId)
│   │       └── EditProfile
│   ├── Notifications
│   └── About
└── NotFound (presentation: modal)
```

## ParamList 타입 계층

```typescript
HomeStackParamList
  Home: undefined
  Detail: { id: string; title: string }
  Settings: undefined
  ProfileDetail: { userId: string }

ProfileStackParamList
  ProfileHub: { userId: string }
  EditProfile: undefined

RootTabParamList
  HomeTab: NavigatorScreenParams<HomeStackParamList>
  SearchTab: undefined
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>

RootDrawerParamList
  Main: NavigatorScreenParams<RootTabParamList>
  Notifications: undefined
  About: undefined

RootStackParamList
  Drawer: NavigatorScreenParams<RootDrawerParamList>
  NotFound: undefined
```

## Deep Link 경로 매핑

| URL | Navigator 경로 | 최종 화면 |
|-----|---------------|-----------|
| `myapp://home` | RootStack → Drawer → Main → HomeTab → Home | HomeScreen |
| `myapp://detail/:id` | RootStack → Drawer → Main → HomeTab → Detail | DetailScreen |
| `myapp://settings` | RootStack → Drawer → Main → HomeTab → Settings | SettingsScreen |
| `myapp://home-profile/:userId` | RootStack → Drawer → Main → HomeTab → ProfileDetail | ProfileDetailScreen |
| `myapp://search` | RootStack → Drawer → Main → SearchTab | SearchScreen |
| `myapp://profile/:userId` | RootStack → Drawer → Main → ProfileTab → ProfileHub | ProfileHubScreen |
| `myapp://profile/edit` | RootStack → Drawer → Main → ProfileTab → EditProfile | EditProfileScreen |
| `myapp://notifications` | RootStack → Drawer → Notifications | NotificationsScreen |
| `myapp://about` | RootStack → Drawer → About | AboutScreen |
| `myapp://unknown` | RootStack → NotFound | NotFoundScreen |

## 의존성 목록

### Navigation 핵심

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `@react-navigation/native` | ^7.1.33 | NavigationContainer, linking, hooks |
| `@react-navigation/stack` | ^7.8.4 | createStackNavigator, transition API |
| `@react-navigation/bottom-tabs` | ^7.15.5 | createBottomTabNavigator |
| `@react-navigation/drawer` | ^7.9.4 | createDrawerNavigator, DrawerItem |

### Navigation 필수 피어 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `react-native-gesture-handler` | ^2.30.0 | Drawer swipe gesture, Stack gesture |
| `react-native-reanimated` | ^4.2.2 | Drawer animation, Stack transition |
| `react-native-screens` | ^4.24.0 | native navigation container 최적화 |
| `react-native-safe-area-context` | ^5.5.2 | 안전 영역 inset 제공 |

### 프레임워크

| 패키지 | 버전 |
|--------|------|
| `react` | 19.2.3 |
| `react-native` | 0.84.1 |
| `typescript` | ^5.8.3 |

## Custom Transition 참조

### Vertical slide (Detail)

```typescript
const detailTransition = {
  gestureDirection: 'vertical',
  transitionSpec: { open: TransitionSpecs.TransitionIOSSpec, close: TransitionSpecs.TransitionIOSSpec },
  cardStyleInterpolator: ({ current, layouts }) => ({
    cardStyle: {
      opacity: current.progress.interpolate({ inputRange: [0, 1], outputRange: [0.82, 1] }),
      transform: [{ translateY: current.progress.interpolate({ inputRange: [0, 1], outputRange: [layouts.screen.height, 0] }) }],
    },
  }),
};
```

### Fade from center (ProfileDetail)

```typescript
options={{ cardStyleInterpolator: CardStyleInterpolators.forFadeFromCenter }}
```

## Makefile 타겟

| 타겟 | 동작 |
|------|------|
| `make test` / `make verify` | `script/verify_task.sh` 실행 |
| `make app-install` | `npm install` |
| `make app-build` | `npm run typecheck` |
| `make app-test` | `npm test` |
| `make run-ios` / `make run-android` | 시뮬레이터 실행 |
| `make test-deeplink-ios` | `xcrun simctl openurl booted "myapp://detail/123"` |
| `make test-deeplink-android` | `adb shell am start ... "myapp://detail/123"` |
| `make clean` | node_modules, ios/build, android/build 삭제 |

## 핵심 개념 문서

| 파일 | 내용 |
|------|------|
| `docs/concepts/navigation-lifecycle.md` | mount/unmount vs focus/blur 구분 |
| `docs/concepts/deep-link-state-mapping.md` | URL → 중첩 state 복원 과정 |
| `docs/concepts/typed-navigation-params.md` | ParamList 타입으로 navigate() 안전성 확보 |

## 연관 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| gestures | 같은 그룹의 선행 과제. GestureHandler 위에 네비게이션을 쌓는다 |
| virtualized-list | 같은 그룹의 후행 과제. FlatList/FlashList를 복잡한 네비게이션 안에서 사용 |
| incident-ops-mobile-client | 캔스톤 앱에서 Bottom Tabs + Stack 중첩 패턴을 적용 |
