# Debug Log — Gestures

## Reanimated worklet 에러

`getSwipeDecision` 함수를 처음 Gesture Handler의 `onEnd` 콜백 안에서 직접 호출했을 때, "Tried to synchronously call a non-worklet function" 에러가 발생했다. Reanimated의 worklet 환경에서는 일반 JS 함수를 직접 호출할 수 없기 때문이다.

해결 방법은 두 가지였다:
1. 함수에 `'worklet'` 디렉티브를 추가
2. `runOnJS`로 감싸서 JS 스레드에서 실행

`gestureMath.ts`의 함수들은 순수 계산이므로 worklet으로 마킹하는 것이 성능상 맞았다. 다만 테스트와의 호환성을 유지하기 위해, 함수 자체에는 worklet 디렉티브를 넣지 않고 컴포넌트에서 인라인으로 같은 계산을 수행하는 방식으로 타협했다.

## sharedTransitionTag가 작동하지 않는 문제

`Animated.View`에 `sharedTransitionTag`를 설정했는데 화면 전환 시 shared element animation이 보이지 않았다. Reanimated 4의 shared transition은 `@react-navigation/native-stack`의 특정 버전과 조합에서만 동작하며, 기본 `stack` navigator에서는 지원되지 않았다.

`createNativeStackNavigator`를 사용하고, 화면 전환 시 animation 모드를 확인하는 것으로 해결했다. 시뮬레이터 환경에서는 shared transition이 미묘하게만 보이는데, 이는 성능보다는 렌더링 타이밍 차이 때문이다.

## Vibration API의 Android 차이

`Vibration.vibrate(10)`이 iOS에서는 미세한 진동을 주지만, Android에서는 최소 진동 시간이 더 길어서 체감이 다르다. 이 프로젝트에서는 iOS 데모용으로 두고, 실제 프로덕션에서는 `react-native-haptic-feedback` 같은 네이티브 모듈을 사용해야 할 것이다.

## interpolate 범위 클램핑

`interpolate(translateX, [0, SWIPE_THRESHOLD], [0, 1])`에서 translateX가 threshold를 넘어가면 opacity가 1을 초과할 수 있다. Reanimated의 `interpolate`는 기본적으로 extrapolation을 허용하므로, `Extrapolation.CLAMP`를 명시하거나 CSS opacity가 자연스럽게 1 이상을 무시하는 것에 의존해야 한다.
