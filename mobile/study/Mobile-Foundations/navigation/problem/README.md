# Problem: Navigation Patterns

> Status: PARTIAL
> Scope: 문제 정의 문서
> Last Checked: 2026-03-02


## Problem Statement

Build a React Native application with a complete navigation structure that uses **Stack**, **Tab**, and **Drawer** navigators in a nested configuration. The app must also support **Deep Linking** to allow external URLs to navigate directly to specific screens.

---

## Part 1: Stack Navigation

### Requirements

Implement a Stack navigator with at least 4 screens demonstrating:

1. **Screen transitions** — Push and pop screens with typed navigation params
2. **Custom animations** — Configure non-default transition animations (e.g., slide from bottom, fade)
3. **Header customization** — Custom header components with back button handling
4. **Params passing** — Pass data between screens using typed route params

### Screen Structure

```
HomeScreen
├── push → DetailScreen (receives: { id: string, title: string })
│   └── push → SettingsScreen
│       └── push → ProfileScreen (receives: { userId: string })
```

### Type Definition

```typescript
type RootStackParamList = {
  Home: undefined;
  Detail: { id: string; title: string };
  Settings: undefined;
  Profile: { userId: string };
};
```

### Custom Animation Example

At least one screen transition must use a custom animation config:

```typescript
const slideFromBottom = {
  gestureDirection: 'vertical',
  cardStyleInterpolator: ({ current, layouts }: StackCardInterpolationProps) => ({
    cardStyle: {
      transform: [
        {
          translateY: current.progress.interpolate({
            inputRange: [0, 1],
            outputRange: [layouts.screen.height, 0],
          }),
        },
      ],
    },
  }),
};
```

---

## Part 2: Tab Navigation

### Requirements

Implement a Bottom Tab navigator with at least 3 tabs:

1. **Tab icons** — Each tab must have a distinct icon (use a vector icon library or custom SVG)
2. **Badge support** — At least one tab must display a notification badge
3. **Tab bar styling** — Custom tab bar appearance (colors, height, shadow)
4. **Lazy loading** — Tabs should lazy-load their content (default behavior, verify it works)

### Tab Structure

```
BottomTabNavigator
├── HomeTab (Stack: Home → Detail → ...)
├── SearchTab
└── ProfileTab (Stack: Profile → EditProfile → ...)
```

### Tab Configuration

```typescript
type RootTabParamList = {
  HomeTab: NavigatorScreenParams<HomeStackParamList>;
  SearchTab: undefined;
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>;
};
```

---

## Part 3: Drawer Navigation

### Requirements

Implement a Drawer navigator that wraps the Tab navigator:

1. **Custom drawer content** — Render a custom drawer with user info and menu items
2. **Drawer items** — At least 4 drawer items, some navigating to screens, some performing actions
3. **Gesture control** — Drawer opens/closes with swipe gesture from the left edge
4. **Conditional items** — Show/hide drawer items based on a mock auth state

### Drawer Structure

```
DrawerNavigator
├── Main (TabNavigator from Part 2)
├── Notifications
├── About
└── Logout (action, not a screen)
```

---

## Part 4: Deep Linking

### Requirements

Configure Deep Linking so external URLs map to specific screens:

1. **URL scheme** — Register a custom URL scheme (e.g., `myapp://`)
2. **Universal links** — Configure path-based linking (e.g., `myapp://detail/123`)
3. **Nested linking** — Deep links must resolve to the correct nested navigator state
4. **Fallback** — Unknown routes should navigate to a "Not Found" screen

### Link Configuration

```typescript
const linking: LinkingOptions<RootParamList> = {
  prefixes: ['myapp://', 'https://myapp.example.com'],
  config: {
    screens: {
      Drawer: {
        screens: {
          Main: {
            screens: {
              HomeTab: {
                screens: {
                  Home: 'home',
                  Detail: 'detail/:id',
                },
              },
              ProfileTab: {
                screens: {
                  Profile: 'profile/:userId',
                },
              },
            },
          },
          Notifications: 'notifications',
        },
      },
      NotFound: '*',
    },
  },
};
```

### Deep Link Test Cases

| URL | Expected Screen | Params |
|-----|-----------------|--------|
| `myapp://home` | HomeScreen | none |
| `myapp://detail/abc123` | DetailScreen | `{ id: "abc123" }` |
| `myapp://profile/user42` | ProfileScreen | `{ userId: "user42" }` |
| `myapp://notifications` | NotificationsScreen | none |
| `myapp://unknown/path` | NotFoundScreen | none |

---

## Test Criteria

1. **Stack**: Push/pop works, params are received correctly, custom animation is visible
2. **Tab**: All tabs render, switching preserves state, badge displays
3. **Drawer**: Opens/closes with gesture, custom content renders, conditional items work
4. **Deep Linking**: All test URLs resolve to the correct screen with the correct params
5. **TypeScript**: Full type safety — no `any` types, all navigation params strictly typed
6. **Platform**: Works on both iOS and Android simulators

## Evaluation

```bash
make test
```
