# 00 — Problem Framing: 네비게이션 패턴 중첩 설계

## 문제의 출발점

모바일 앱에서 네비게이션은 "화면 이동"이 아니라 "상태 트리 조작"이다.
React Navigation이 제공하는 Stack, Tab, Drawer는 각각 독립된 상태 컨테이너이기 때문에,
이 세 가지를 하나의 앱에 결합하는 순간 **중첩된 상태 트리**가 만들어진다.
외부에서 URL 하나로 특정 화면을 열려면 이 트리의 모든 레이어를 정확하게 복원해야 한다.

이 프로젝트는 "React Native 앱에서 Stack, Tab, Drawer, Deep Linking을 모두 사용하는 네비게이션 구조를 설계하고,
TypeScript 타입으로 안전하게 잠그는 것"을 목표로 한다.

## 왜 이 문제가 중요한가

실무에서 네비게이션 구조는 앱의 첫 번째 아키텍처 결정이다.
한 번 잡으면 쉽게 바꾸기 어렵고, 화면 수가 늘어날수록 잘못된 구조의 비용이 기하급수적으로 커진다.
특히 다음 세 가지 상황이 문제를 복잡하게 만든다:

1. **탭 안에 Stack이 있고, 그 바깥에 Drawer가 있는 3중 중첩** — 어떤 navigator가 어떤 화면을 소유하는지 명확하지 않으면 `navigate()` 호출이 의도와 다른 화면으로 이동한다.
2. **Deep Link가 중첩 상태를 한 번에 복원해야 할 때** — `myapp://detail/abc123` 하나가 RootStack → Drawer → Tabs → HomeStack → Detail 순서로 4단계 상태를 만들어야 한다.
3. **TypeScript 없이 route params를 관리하면** — 화면 간 데이터 전달이 런타임 에러의 온상이 된다. 문자열 기반 navigate는 리팩터링에 취약하다.

## 설계 방향

### Navigator 계층 구조

```
RootStack (headerShown: false)
└── DrawerNavigator
    ├── Main (TabNavigator)
    │   ├── HomeTab (HomeStack)
    │   │   ├── Home
    │   │   ├── Detail (vertical transition)
    │   │   ├── Settings
    │   │   └── ProfileDetail (fade from center)
    │   ├── SearchTab (단일 화면, 탭 상태 유지 검증)
    │   └── ProfileTab (ProfileStack)
    │       ├── ProfileHub
    │       └── EditProfile
    ├── Notifications (Drawer 직접 소유)
    └── About (Drawer 직접 소유)
```

이 구조에서 핵심은 **RootStack이 Drawer 위에 존재**한다는 점이다.
NotFound 화면을 modal로 띄우려면 Drawer 바깥에 Stack이 하나 더 필요하다.
이 결정이 deep link fallback 처리를 자연스럽게 만든다.

### 타입 안전성 전략

`NavigatorScreenParams`를 사용해 상위 navigator가 하위 navigator의 params를 합성한다.
이렇게 하면 `navigation.navigate('Main', { screen: 'HomeTab', params: { screen: 'Detail', params: { id: '...', title: '...' } } })`
같은 중첩 호출도 타입 체크가 가능해진다.

### Deep Link 설계 원칙

- URL에는 최소한의 식별자만 넣고, 부가 정보는 state hydration 단계에서 보완한다.
- `detail/:id`에서 title은 URL에 포함하지 않고 `resolveNavigationState()`가 id로부터 생성한다.
- 등록되지 않은 path는 wildcard `*`로 NotFound 화면에 매핑한다.

## 학습 범위

| 영역 | 구체적 목표 |
|------|-------------|
| Stack | push/pop 흐름, custom transition animation, custom header |
| Tab | 3탭 구성, lazy loading, badge 표시, 탭 전환 시 상태 유지 |
| Drawer | custom drawer content, conditional items (인증 상태 기반), gesture 제어 |
| Deep Link | URL scheme + universal link, 중첩 state 복원, fallback 처리 |
| TypeScript | ParamList 정의 → NavigatorScreenParams 합성 → Screen Props 추출 |

## Problem → Solution 설계서와의 관계

`problem/README.md`에 4개 Part(Stack, Tab, Drawer, Deep Linking)로 나뉜 요구사항이 정의되어 있다.
이 문서는 그 요구사항을 왜 이 구조로 풀었는지를 설명하는 보완 관계다.
