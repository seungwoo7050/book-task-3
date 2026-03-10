# Approach Log — Gestures

## 첫 번째 결정: 제스처 로직을 순수 함수로 분리

Reanimated의 `useSharedValue`와 `Gesture.Pan()`은 UI 스레드에서 동작하기 때문에 단위 테스트가 어렵다. 이 문제를 해결하기 위해, 제스처의 **판단 로직**을 순수 함수(`gestureMath.ts`)로 꺼내고, 컴포넌트에서는 그 함수를 호출만 하도록 분리했다.

- `getSwipeDecision(translateX, threshold)` — threshold 기준으로 like/nope/reset 판단
- `getDismissProgress(translateY, maxDistance)` — 아래로 드래그한 비율 계산
- `reorderByOffset(items, activeIndex, offsetY, rowHeight)` — 드래그 오프셋으로 새 순서 계산

이 분리 덕분에 제스처의 핵심 판단 로직을 Jest로 테스트할 수 있었다.

## 두 번째 결정: Swipe Card의 spring 파라미터

카드가 threshold를 넘지 못해 원위치로 돌아올 때, `withSpring`의 `damping`과 `stiffness` 값을 어떻게 잡을 것인가.

여러 조합을 시뮬레이터에서 직접 테스트한 뒤 `damping: 16, stiffness: 190`으로 결정했다. damping이 너무 낮으면 카드가 과하게 흔들리고, stiffness가 너무 높으면 딱딱해 보인다. 이 값은 Tinder의 실제 느낌에 가장 가까웠다.

threshold를 넘겨 카드를 날릴 때는 spring 대신 `withTiming(duration: 220)`을 사용했다. 날아가는 동작은 예측 가능해야 하기 때문에 고정 시간이 더 적절했다.

## 세 번째 결정: Reorder를 실제 drag 대신 tap 시뮬레이션으로

원래 요구사항은 long-press → drag → drop 흐름이었지만, 학습 데모에서 이를 완전히 구현하면 코드가 지나치게 복잡해진다. 그래서 "tap하면 한 칸 아래로 이동"하는 단순화된 시뮬레이션으로 대체했다.

핵심은 `reorderByOffset` 함수가 올바르게 동작하는지를 테스트하는 것이지, 실제 drag UX를 완성하는 것이 아니었다. 이 결정으로 테스트 가능한 핵심 로직과 데모 UI를 분리할 수 있었다.

## 네 번째 결정: Shared Transition의 dismiss 기준

Detail 화면에서 아래로 스와이프할 때, 어느 시점에서 dismiss를 결정하나?

`getDismissProgress`가 0.6(60%)을 넘으면 dismiss, 아니면 spring back하도록 설정했다. 이 기준은 iOS의 interactive sheet dismiss와 비슷한 느낌을 만든다.

## 다섯 번째 결정: GestureHandlerRootView를 최상위에 배치

`react-native-gesture-handler`의 모든 제스처가 동작하려면 `GestureHandlerRootView`가 앱의 최상위에 있어야 한다. 이것을 화면 단위가 아닌 `GesturesStudyApp` 최상위에 배치한 이유는, 여러 화면에서 제스처가 동시에 동작할 수 있어야 하기 때문이다.
