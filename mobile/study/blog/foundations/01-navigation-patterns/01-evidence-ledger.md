# Evidence Ledger: 01 Navigation Patterns

## 독립 프로젝트 판정

- 판정: 처리
- 근거: 자체 `README.md`, `problem/README.md`, `react-native/package.json`, `react-native/__tests__/navigation.test.tsx`, deep link 수동 점검 명령을 모두 갖춘 가장 작은 RN 파일럿이다.
- 소스 경로: `mobile/study/foundations/01-navigation-patterns`

## 사용한 근거

- `mobile/study/foundations/01-navigation-patterns/README.md`
- `mobile/study/foundations/01-navigation-patterns/problem/README.md`
- `mobile/study/foundations/01-navigation-patterns/react-native/README.md`
- `mobile/study/foundations/01-navigation-patterns/docs/concepts/deep-link-state-mapping.md`
- `mobile/study/foundations/01-navigation-patterns/docs/concepts/typed-navigation-params.md`
- `mobile/study/foundations/01-navigation-patterns/react-native/src/navigation/types.ts`
- `mobile/study/foundations/01-navigation-patterns/react-native/src/navigation/RootNavigator.tsx`
- `mobile/study/foundations/01-navigation-patterns/react-native/src/navigation/linking.ts`
- `mobile/study/foundations/01-navigation-patterns/react-native/src/screens/AppScreens.tsx`
- `mobile/study/foundations/01-navigation-patterns/react-native/__tests__/navigation.test.tsx`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/01-navigation-patterns/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | navigator 계약을 먼저 닫는다

- 당시 목표: Stack, Tab, Drawer가 서로 기대하는 param shape를 먼저 고정한다.
- 변경 단위: `react-native/src/navigation/types.ts`, `react-native/src/navigation/RootNavigator.tsx`
- 처음 가설: 화면보다 타입이 먼저 닫히면 nested navigation이 커져도 route 해석이 흔들리지 않는다.
- 실제 조치: `HomeStackParamList`, `RootTabParamList`, `RootDrawerParamList`, `RootStackParamList`를 분리하고 `NavigatorScreenParams`로 중첩 state를 연결했다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- 현재 replay에서 `tsc --noEmit`가 통과했다.
- `navigation.navigate()` 호출이 타입 수준에서 `Detail`, `ProfileDetail` param shape를 강제한다.
- 핵심 코드 앵커:
```ts
export type RootTabParamList = {
  HomeTab: NavigatorScreenParams<HomeStackParamList>;
  SearchTab: undefined;
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>;
};
```
- 새로 배운 것: navigation 구조를 화면 목록이 아니라 계약 그래프로 잡아야 deep link와 screen props가 같은 언어를 쓴다.
- 다음: 타입 계약 위에 custom drawer/tab UI와 실제 화면 흐름을 올린다.

### Phase 2 | deep link가 nested state를 복원하도록 만든다

- 당시 목표: URL 하나가 Drawer -> Tab -> Inner Stack까지 복원되게 만든다.
- 변경 단위: `react-native/src/navigation/linking.ts`, `react-native/src/screens/AppScreens.tsx`
- 처음 가설: `detail/:id` 같은 path는 화면 이름만 찾는 게 아니라 누락된 title 같은 state도 hydration해야 한다.
- 실제 조치: `normalizePath()`, `resolveNavigationState()`를 두고 `Detail` route에 title을 보강했다. 화면 쪽에는 stack step, tab state, fallback route를 각각 분리해 deep link 결과가 눈에 보이게 했다.
- CLI:
```bash
xcrun simctl openurl booted "myapp://detail/abc123"
adb shell am start -W -a android.intent.action.VIEW -d "myapp://notifications"
```
- 검증 신호:
- `resolveNavigationState('myapp://detail/abc123')`는 `Detail`과 `{ id, title }`을 포함한 nested state를 만든다.
- unknown path는 `NotFound`로 내려간다.
- 핵심 코드 앵커:
```ts
if (params?.id && !params.title) {
  route.params = {
    ...params,
    title: buildDetailTitle(params.id),
  };
}
```
- 새로 배운 것: deep link는 화면 점프가 아니라 상태 복원이다. URL에 없는 값도 state hydration 규칙으로 보완해야 한다.
- 다음: typed route call과 fallback 경로를 테스트로 잠근다.

### Phase 3 | Jest가 route 계약을 공개 게이트가 된다

- 당시 목표: typed navigation call, deep link mapping, fallback 경로를 JS 테스트로 재현한다.
- 변경 단위: `react-native/__tests__/navigation.test.tsx`, `react-native/package.json`
- 처음 가설: 디바이스 없이도 가장 중요한 판단은 route call과 state mapping 테스트로 고정할 수 있다.
- 실제 조치: `HomeScreen`, `DetailScreen`, `SettingsScreen`, `NotFoundScreen`을 직접 렌더링해서 navigation call을 검증하고, `resolveNavigationState()`로 deep link/fallback을 비교했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS __tests__/navigation.test.tsx`
- `Test Suites: 1 passed`, `Tests: 3 passed`
- 핵심 코드 앵커:
```ts
expect(homeNavigate).toHaveBeenCalledWith('Detail', {
  id: 'abc123',
  title: 'On-call deep link drill',
});
```
- 새로 배운 것: navigation 프로젝트의 최소 공용 게이트는 “화면이 뜬다”가 아니라 “route 계약과 URL 매핑이 변형되지 않는다”다.
- 다음: 다음 프로젝트에서는 route 구조 대신 같은 데이터셋을 두 렌더링 전략에 올려 성능 비교를 숫자로 남긴다.
