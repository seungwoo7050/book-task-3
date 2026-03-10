# 05 — Development Timeline: 개발 환경·도구 기록

이 문서는 소스 코드만으로는 알 수 없는 CLI 명령, 패키지 설치 순서, 시뮬레이터 설정, 디바이스 테스트 과정을 기록한다.

---

## Step 1: 프로젝트 초기화

React Native 0.84.1 기반 프로젝트 생성. 공통 템플릿에서 시작했다.

```bash
cd study/Mobile-Foundations/navigation/react-native
npm install
```

Node 22.11.0 이상 필요 (`engines` 필드 지정).

## Step 2: React Navigation 패키지 설치

React Navigation v7은 core와 navigator가 분리되어 있다.
필요한 navigator 종류에 따라 패키지를 선택적으로 설치한다.

```bash
# Core
npm install @react-navigation/native

# Navigator별 패키지
npm install @react-navigation/stack
npm install @react-navigation/bottom-tabs
npm install @react-navigation/drawer

# 필수 피어 의존성
npm install react-native-gesture-handler
npm install react-native-reanimated
npm install react-native-screens
npm install react-native-safe-area-context
```

설치 순서가 중요한 이유:
- `react-native-gesture-handler`는 앱 진입점(`index.js` 또는 `App.tsx`)에서 가장 먼저 import되어야 한다.
- `react-native-reanimated`는 babel plugin(`react-native-reanimated/plugin`)을 `babel.config.js`에 등록해야 한다. 이 플러그인은 반드시 plugins 배열의 **마지막**에 위치해야 한다.

## Step 3: iOS 네이티브 설정

```bash
cd ios
bundle install        # Gemfile에 명시된 CocoaPods 버전 설치
bundle exec pod install
cd ..
```

React Navigation의 Drawer와 gesture 지원을 위해 `ios/Podfile`에 추가 설정이 필요할 수 있다:
- `react-native-screens`가 설치되면 `AppDelegate`에서 `UIViewController` 기반 rendering이 활성화된다.
- `react-native-gesture-handler`의 native module이 pod install을 통해 자동으로 연결된다.

## Step 4: Android 네이티브 설정

Android는 대부분 auto-linking으로 처리되지만, `react-native-gesture-handler`는 `MainActivity`에 추가 설정이 필요하다:

```kotlin
// MainActivity.kt (또는 .java)
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(null)  // savedInstanceState 대신 null 전달
}
```

이 설정이 없으면 gesture handler가 configuration change 후 올바르게 동작하지 않는다.

## Step 5: Reanimated Babel Plugin 설정

```javascript
// babel.config.js
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    // ... 다른 플러그인
    'react-native-reanimated/plugin', // 반드시 마지막!
  ],
};
```

Reanimated plugin 위치를 잘못 넣으면 빌드는 성공하지만 런타임에 worklet 관련 에러가 발생한다.
증상이 모호하기 때문에 문제 원인을 찾기 어렵다.

## Step 6: 타입 체크 및 테스트

```bash
# TypeScript 타입 체크 (빌드 없이)
npm run typecheck

# Jest 테스트 실행
npm test

# 둘 다 한 번에
npm run verify
```

`make app-build`는 내부적으로 `npm run typecheck`를 실행한다.
이 프로젝트에서 "빌드"는 네이티브 바이너리 생성이 아니라 타입 체크를 의미한다.

## Step 7: 시뮬레이터 실행

```bash
# iOS 시뮬레이터
npm run ios
# 또는
make run-ios

# Android 에뮬레이터
npm run android
# 또는
make run-android
```

Metro bundler가 별도 터미널에서 실행 중이어야 한다:
```bash
npm start
```

## Step 8: Deep Link 테스트 (시뮬레이터)

실제 디바이스 없이 시뮬레이터에서 deep link를 테스트하는 방법:

### iOS

```bash
# Makefile 타겟 사용
make test-deeplink-ios

# 또는 직접 실행
xcrun simctl openurl booted "myapp://detail/123"
xcrun simctl openurl booted "myapp://profile/user42"
xcrun simctl openurl booted "myapp://notifications"
xcrun simctl openurl booted "myapp://unknown/path"
```

### Android

```bash
# Makefile 타겟 사용
make test-deeplink-android

# 또는 직접 실행
adb shell am start -W -a android.intent.action.VIEW -d "myapp://detail/123"
adb shell am start -W -a android.intent.action.VIEW -d "myapp://profile/user42"
```

deep link 테스트 시 앱이 이미 실행 중인 상태에서 URL을 보내면 `linking`의 `subscribe`가 이벤트를 받아 처리한다.
앱이 종료된 상태에서 URL을 보내면 `getInitialURL`로 처리된다.

## Step 9: 검증 스크립트

```bash
# problem 디렉터리의 검증 스크립트
make verify
# 내부적으로 script/verify_task.sh 실행
```

## 사용된 도구 정리

| 도구 | 버전/용도 |
|------|-----------|
| Node.js | >= 22.11.0 |
| npm | 패키지 관리 |
| CocoaPods | iOS native dependency |
| Xcode / xcrun simctl | iOS 시뮬레이터 + deep link 테스트 |
| Android Studio / adb | Android 에뮬레이터 + deep link 테스트 |
| Metro Bundler | JS 번들링 + HMR |
| TypeScript 5.8+ | 타입 체크 (`--noEmit`) |
| Jest 29.6+ | 테스트 러너 |
| ESLint 8.x | 린팅 |

## 트러블슈팅 체크리스트

- [ ] Metro 캐시가 의심되면: `npm start -- --reset-cache`
- [ ] Pod 설치 오류 시: `cd ios && bundle exec pod install --repo-update`
- [ ] Reanimated 워크렛 에러 시: babel.config.js에서 plugin 순서 확인
- [ ] Gesture handler 미동작 시: MainActivity의 `onCreate(null)` 확인
- [ ] Deep link 미동작 시: `linking.prefixes` 배열에 URL scheme 포함 여부 확인
