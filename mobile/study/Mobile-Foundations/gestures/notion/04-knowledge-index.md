# Knowledge Index — Gestures

## 연결된 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| `navigation` | 같은 그룹의 후행 과제. 여기서 사용한 `@react-navigation/native-stack`을 navigation에서 더 깊이 다룬다. |
| `native-modules` | Haptics 네이티브 모듈 spec이 이 프로젝트의 `Vibration.vibrate()` 대체안이다. |
| `incident-ops-mobile-client` | 캡스톤 앱에서 제스처/애니메이션을 적용하는 최종 소비자. |

## 재사용 가능한 패턴

### 제스처 판단 로직 분리 패턴
`getSwipeDecision(translateX, threshold)` 같은 순수 함수를 worklet 외부에 두면, Jest로 테스트할 수 있고 다른 컴포넌트에서도 같은 판단 기준을 공유할 수 있다.

### Threshold + Spring-back 패턴
모든 제스처 인터랙션에 적용 가능: 입력값이 threshold를 넘으면 action, 아니면 spring으로 원위치. Swipe dismiss, pull-to-refresh, sheet dragging 등에 동일하게 적용된다.

### GestureHandlerRootView 최상위 배치 원칙
모든 제스처 기반 앱에서 `GestureHandlerRootView`는 앱 root에 한 번만 배치한다. navigation container보다 바깥에 있어야 한다.

## 핵심 파일 참조

| 파일 | 역할 |
|------|------|
| `react-native/src/gestureMath.ts` | 제스처 판단 순수 함수 (swipe, reorder, dismiss) |
| `react-native/src/GesturesStudyApp.tsx` | 세 데모를 포함하는 메인 앱 |
| `react-native/tests/gestures.test.tsx` | 제스처 판단 로직 테스트 |
| `docs/concepts/gesture-workflow.md` | 세 데모의 공통 질문과 규칙 |

## 이 프로젝트에서 사용한 도구와 버전

- React Native 0.84.1
- react-native-reanimated ^4.2.2
- react-native-gesture-handler ^2.30.0
- @react-navigation/native ^7.1.33
- @react-navigation/native-stack ^7.14.4
- react-native-safe-area-context ^5.5.2
- react-native-screens ^4.24.0
- TypeScript ^5.8.3
- Jest ^29.6.3
