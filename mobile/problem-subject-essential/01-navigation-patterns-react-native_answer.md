# 01-navigation-patterns-react-native 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

Stack, Tab, Drawer를 중첩한 React Native 앱을 만들고, external URL이 특정 화면으로 바로 진입하도록 Deep Linking까지 연결하는 과제다. 핵심은 `titleMap`와 `AppHeader`, `styles` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 기존 navigation 과제 요구사항
- typed params를 사용하는 Stack navigator
- badge와 custom style을 갖춘 Bottom Tab navigator
- 첫 진입점은 `../study/foundations/01-navigation-patterns/react-native/src/components/AppHeader.tsx`이고, 여기서 `titleMap`와 `AppHeader` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/foundations/01-navigation-patterns/react-native/src/components/AppHeader.tsx`: `titleMap`, `AppHeader`, `styles`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/foundations/01-navigation-patterns/react-native/src/navigation/linking.ts`: `normalizePath`, `visitRoutes`, `buildDetailTitle`, `linking`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/foundations/01-navigation-patterns/react-native/src/navigation/RootNavigator.tsx`: `RootStack`, `Drawer`, `Tabs`, `HomeStack`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/foundations/01-navigation-patterns/react-native/src/navigation/types.ts`: 핵심 구현을 담는 파일이다.
- `../study/foundations/01-navigation-patterns/react-native/src/screens/AppScreens.tsx`: `ScreenShell`, `ActionButton`, `StatCard`, `HomeScreen`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/foundations/01-navigation-patterns/react-native/__tests__/navigation.test.tsx`: `navigation pilot`, `renders the stack screens and emits typed navigation calls`, `maps known deep links into nested navigation state`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/foundations/01-navigation-patterns/problem/script/verify_task.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/foundations/01-navigation-patterns/react-native/app.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/foundations/01-navigation-patterns/react-native/src/components/AppHeader.tsx`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `navigation pilot` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/01-navigation-patterns/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/01-navigation-patterns/react-native && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `navigation pilot`와 `renders the stack screens and emits typed navigation calls`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/foundations/01-navigation-patterns/react-native/src/components/AppHeader.tsx`
- `../study/foundations/01-navigation-patterns/react-native/src/navigation/linking.ts`
- `../study/foundations/01-navigation-patterns/react-native/src/navigation/RootNavigator.tsx`
- `../study/foundations/01-navigation-patterns/react-native/src/navigation/types.ts`
- `../study/foundations/01-navigation-patterns/react-native/src/screens/AppScreens.tsx`
- `../study/foundations/01-navigation-patterns/react-native/__tests__/navigation.test.tsx`
- `../study/foundations/01-navigation-patterns/problem/script/verify_task.sh`
- `../study/foundations/01-navigation-patterns/react-native/app.json`
- `../study/foundations/01-navigation-patterns/react-native/ios/NavigationPatternsStudy/Images.xcassets/AppIcon.appiconset/Contents.json`
- `../study/foundations/01-navigation-patterns/react-native/ios/NavigationPatternsStudy/Images.xcassets/Contents.json`
