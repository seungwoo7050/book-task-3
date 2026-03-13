# 01 Navigation Patterns

이 프로젝트의 출발점은 “화면이 많아지면 navigation이 복잡해진다”는 막연한 감상이 아니었다. Stack, Tab, Drawer, Deep Linking을 같은 앱 안에 넣되, route와 params를 계속 설명 가능한 상태로 유지할 수 있느냐가 실제 질문이었다. 그래서 구현 순서를 일부러 route contract -> deep link hydration -> 테스트 고정 순으로 잡았다.

## 이번 글에서 따라갈 구현 순서

- `types.ts`에서 nested navigator contract를 먼저 닫는다.
- `RootNavigator.tsx`와 `linking.ts`에서 custom drawer/tab UI와 deep link state 복원을 연결한다.
- `navigation.test.tsx`로 typed route call, known link, fallback path를 재현한다.

## 새로 이해한 것: deep link는 화면 이동이 아니라 상태 복원이다

`myapp://detail/abc123` 같은 URL은 화면 이름 하나만 정하는 게 아니다. root stack, drawer, tab, inner stack, 그리고 URL에 없는 `title` 같은 보강값까지 한 번에 맞아야 한다. 그래서 이 프로젝트의 핵심은 navigator 개수를 늘리는 데 있지 않고, 그 상태를 타입과 함수로 복원 가능하게 만드는 데 있었다.

## Phase 1
### navigator 계약을 먼저 닫는다

- 당시 목표: Stack, Tab, Drawer가 서로 기대하는 param shape를 먼저 고정한다.
- 변경 단위: `react-native/src/navigation/types.ts`, `react-native/src/navigation/RootNavigator.tsx`
- 처음 가설: 화면보다 타입이 먼저 닫히면 nested navigation이 커져도 route 해석이 흔들리지 않는다.
- 실제 진행: `HomeStackParamList`, `ProfileStackParamList`, `RootTabParamList`, `RootDrawerParamList`, `RootStackParamList`를 따로 선언하고 `NavigatorScreenParams`로 이어 붙였다. 그런 다음 `RootNavigator.tsx`에서 home stack, profile stack, bottom tab, custom drawer를 이 그래프 위에 올렸다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/01-navigation-patterns/react-native
npm run typecheck
```

검증 신호:

- current replay에서 `tsc --noEmit`가 통과했다.
- `Detail`, `ProfileDetail` 같은 화면은 잘못된 param shape로 호출할 수 없게 됐다.

핵심 코드:

```ts
export type RootTabParamList = {
  HomeTab: NavigatorScreenParams<HomeStackParamList>;
  SearchTab: undefined;
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>;
};
```

왜 이 코드가 중요했는가:

navigation을 “스크린 모음”이 아니라 “계약 그래프”로 바꾸는 순간, 뒤에서 deep link와 screen props가 같은 구조를 바라보게 된다.

새로 배운 것:

- nested navigation은 화면 트리보다 state graph로 설명해야 덜 흔들린다.

다음:

- URL 하나가 이 계약 그래프를 실제 state로 복원하도록 만든다.

## Phase 2
### deep link가 nested state를 복원하도록 만든다

- 당시 목표: URL 하나가 Drawer -> Tab -> Inner Stack까지 복원되게 만든다.
- 변경 단위: `react-native/src/navigation/linking.ts`, `react-native/src/screens/AppScreens.tsx`
- 처음 가설: `detail/:id`는 path match만으로 끝나지 않고, URL에 없는 title까지 hydration해야 실제 Detail 화면이 설명 가능해진다.
- 실제 진행: `normalizePath()`로 scheme과 host를 정리하고, `resolveNavigationState()`에서 `Detail` route를 찾아 `{ id, title }`을 완성했다. 화면 쪽에는 `Home -> Detail -> Settings -> ProfileDetail` 흐름, stateful `SearchTab`, conditional drawer action, fallback `NotFound`를 각각 분리해 deep link 결과가 눈에 보이게 했다.

CLI:

```bash
xcrun simctl openurl booted "myapp://detail/abc123"
adb shell am start -W -a android.intent.action.VIEW -d "myapp://notifications"
```

검증 신호:

- `resolveNavigationState('myapp://detail/abc123')` 결과에는 `Detail`, `id: abc123`, `title: Detail route for abc123`가 함께 들어간다.
- unknown path는 `NotFound` state로 떨어진다.

핵심 코드:

```ts
if (params?.id && !params.title) {
  route.params = {
    ...params,
    title: buildDetailTitle(params.id),
  };
}
```

왜 이 코드가 중요했는가:

URL에 없는 값을 state hydration으로 메우는 지점이어서, deep link가 “화면 이름 파싱”을 넘어 실제 앱 상태 복원으로 바뀐다.

새로 배운 것:

- deep link 설계의 핵심은 path grammar보다 state hydration 규칙이다.

다음:

- typed route call과 fallback path를 JS 테스트로 고정한다.

## Phase 3
### Jest가 공개 검증 게이트가 된다

- 당시 목표: typed navigation call, known deep link, fallback 경로를 디바이스 없이 재생한다.
- 변경 단위: `react-native/__tests__/navigation.test.tsx`
- 처음 가설: 이 파일럿의 핵심은 animation fidelity보다 route contract와 URL mapping이므로, Jest만으로도 대부분의 위험을 잡을 수 있다.
- 실제 진행: `HomeScreen`, `DetailScreen`, `SettingsScreen`, `NotFoundScreen`을 직접 렌더링해서 navigation call을 검증하고, `resolveNavigationState()`로 known/unknown path를 비교했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS __tests__/navigation.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 3 passed`

핵심 코드:

```ts
expect(homeNavigate).toHaveBeenCalledWith('Detail', {
  id: 'abc123',
  title: 'On-call deep link drill',
});
```

왜 이 코드가 중요했는가:

typed route contract가 실제 UI event에서 어떻게 소비되는지 바로 보여 주기 때문이다.

새로 배운 것:

- navigation 프로젝트의 최소 공용 게이트는 “화면이 뜬다”가 아니라 “route 계약과 URL 매핑이 변하지 않는다”다.

다음:

- 다음 프로젝트에서는 route 구조 대신 같은 10k 데이터셋을 두 리스트 전략에 태워 성능 차이를 수치와 artifact로 남긴다.

## 여기까지 정리

- 이 프로젝트가 남긴 핵심은 navigation 복잡도를 줄인 것이 아니라, nested navigator state를 타입과 deep link 함수로 복원 가능하게 만든 것이다.
- 다음 단계의 질문: 같은 조건 비교를 강제하려면 데이터셋과 pagination부터 어떻게 고정해야 할까?
