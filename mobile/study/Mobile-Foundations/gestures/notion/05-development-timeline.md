# Development Timeline — Gestures

이 문서는 프로젝트의 전체 개발 과정을 시간순으로 기록한다.
소스코드만으로는 알 수 없는 CLI 명령, 설치 과정, 설정 변경, 의사결정 맥락을 포함한다.

---

## Phase 1: 프로젝트 초기화

### React Native 프로젝트 생성

```bash
npx @react-native-community/cli init GesturesStudy --version 0.84.1
cd GesturesStudy
```

### 핵심 의존성 설치

제스처와 애니메이션을 위한 라이브러리 설치:

```bash
npm install react-native-gesture-handler@^2.30.0
npm install react-native-reanimated@^4.2.2
npm install @react-navigation/native@^7.1.33
npm install @react-navigation/native-stack@^7.14.4
npm install react-native-safe-area-context@^5.5.2
npm install react-native-screens@^4.24.0
npm install @testing-library/react-native@^13.3.3
```

Gesture Handler와 Reanimated는 이 프로젝트의 핵심이다. Navigation은 Shared Transition 데모를 위해 필요했다.

### babel.config.js 수정

Reanimated를 사용하려면 Babel plugin 설정이 필요하다:

```javascript
// babel.config.js의 plugins 배열에 추가
plugins: ['react-native-reanimated/plugin']
```

이 플러그인은 반드시 plugins 배열의 **마지막**에 위치해야 한다. 순서가 틀리면 worklet 변환이 제대로 되지 않는다.

### iOS 네이티브 의존성

```bash
cd ios && bundle install && bundle exec pod install && cd ..
```

Gesture Handler와 Reanimated 모두 네이티브 코드를 포함하므로 Pod install이 필수다.

---

## Phase 2: 제스처 수학 함수 구현

### gestureMath.ts 작성

제스처의 판단 로직을 순수 함수로 먼저 작성했다:

1. **`getSwipeDecision(translateX, threshold)`** — 수평 이동량으로 like/nope/reset 판단
2. **`getDismissProgress(translateY, maxDistance)`** — 수직 이동 비율 계산 (0~1로 정규화)
3. **`reorderByOffset(items, activeIndex, offsetY, rowHeight)`** — 드래그 오프셋으로 배열 재정렬

함수 설계 원칙:
- 모든 입력은 숫자 또는 배열
- 모든 출력은 새 값 (원본 변경 없음)
- 어떤 외부 상태에도 의존하지 않음

---

## Phase 3: 테스트 작성

### gestures.test.tsx

세 가지 테스트 그룹:

```bash
npm test -- --verbose
```

1. **Swipe 판단 테스트** — `180 >= 120` → like, `-180 <= -120` → nope, `40 < 120` → reset
2. **Reorder 테스트** — `offset = 58, rowHeight = 58` → 한 칸 이동
3. **Dismiss progress 클램프 테스트** — 0에서 시작, 절반이면 0.5, 초과하면 1로 클램프

테스트에서 `gestureMath.ts`만 import하기 때문에 Reanimated나 Gesture Handler의 네이티브 바인딩이 필요 없다.

---

## Phase 4: Swipe Card 데모 구현

### SwipeCardDemo 컴포넌트

`GesturesStudyApp.tsx`에서 SwipeCardDemo를 작성했다:

1. `useSharedValue(0)`으로 translateX, translateY 초기화
2. `Gesture.Pan()`의 `onUpdate`에서 좌표값 추적
3. `onEnd`에서 `getSwipeDecision`의 결과에 따라:
   - `reset` → `withSpring(0, { damping: 16, stiffness: 190 })`
   - `like`/`nope` → `withTiming(±360, { duration: 220 })`
4. `useAnimatedStyle`로 transform(translate + rotate)과 LIKE/NOPE label opacity 연결

Spring 파라미터(`damping: 16, stiffness: 190`)는 시뮬레이터에서 여러 번 테스트하며 결정했다.

---

## Phase 5: Reorder와 Shared Transition 데모

### ReorderDemo 컴포넌트

실제 drag 대신 tap 시뮬레이션으로 단순화:
- 아이템을 탭하면 `reorderByOffset`으로 한 칸 이동
- `Vibration.vibrate(10)`으로 햅틱 피드백 시뮬레이션

### SharedGalleryScreen / SharedDetailScreen

Navigation Stack으로 두 화면을 구성:
- Gallery 화면: SwipeCard + Reorder + 갤러리 카드
- Detail 화면: `sharedTransitionTag`로 연결된 expanded view
- Detail에서 아래로 드래그하면 `getDismissProgress > 0.6` 시 goBack

```bash
# 시뮬레이터에서 확인
npm run ios
```

---

## Phase 6: 앱 구조 완성

### GesturesStudyApp export

`GestureHandlerRootView`를 최상위에 배치하고, 그 안에 `NavigationContainer`와 `Stack.Navigator`를 넣었다. 이 순서가 중요하다 — Gesture Handler가 Navigation보다 바깥에 있어야 제스처가 모든 화면에서 동작한다.

---

## Phase 7: 빌드 검증

```bash
npm run typecheck    # TypeScript 검증
npm test             # Jest 실행
npm run verify       # typecheck + test

# Make 기반 검증
cd problem
make test            # verify_task.sh
make app-build       # npm install + typecheck
make app-test        # npm install + jest

# 시뮬레이터 실행
make run-ios         # iOS 시뮬레이터
make run-android     # Android 에뮬레이터
```

---

## 사용한 CLI 명령 전체 요약

| 단계 | 명령 | 목적 |
|------|------|------|
| 초기화 | `npx @react-native-community/cli init` | RN 프로젝트 생성 |
| 의존성 | `npm install react-native-gesture-handler react-native-reanimated ...` | 제스처/애니메이션 라이브러리 |
| Babel | `babel.config.js`에 `reanimated/plugin` 추가 | worklet 변환 활성화 |
| iOS | `cd ios && bundle install && bundle exec pod install` | 네이티브 의존성 |
| 테스트 | `npm test` | Jest 실행 |
| 실행 | `npm run ios` | iOS 시뮬레이터 실행 |
| 검증 | `npm run verify` | typecheck + test |
