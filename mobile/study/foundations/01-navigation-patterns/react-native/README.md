# React Native Implementation

Status: verified

이 앱은 `study/foundations/01-navigation-patterns`의 실행 가능한 파일럿 구현이다.
Stack, Tab, Drawer, Deep Linking 요구를 하나의 독립 React Native CLI 앱으로 묶었다.

## Commands

```bash
npm install
npm run typecheck
npm test
npm run verify
```

## Manual Deep Link Checks

```bash
xcrun simctl openurl booted "myapp://detail/abc123"
adb shell am start -W -a android.intent.action.VIEW -d "myapp://notifications"
```

## Covered Behaviors

- typed navigation params
- custom stack transition
- custom drawer content with conditional actions
- tab badge and styled tab bar
- nested deep link mapping with unknown route fallback

## Limits

- universal link hosting and entitlement wiring are not fully validated in this repository
- JS/type/test are the canonical verification gate
