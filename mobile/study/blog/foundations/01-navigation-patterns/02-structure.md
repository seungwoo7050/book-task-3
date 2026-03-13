# Structure Plan: 01 Navigation Patterns

## 글의 중심 질문

- 이 프로젝트의 시작점은 화면 꾸미기가 아니라 route 계약이었다. Stack, Tab, Drawer, deep link를 한 앱 안에 넣으려면 먼저 nested navigator state를 타입과 path로 설명 가능하게 만들어야 했다.

## 구현 순서 요약

- `types.ts`에서 nested navigator contract를 먼저 닫는다.
- `RootNavigator.tsx`와 `linking.ts`로 custom UI와 deep link hydration을 연결한다.
- `navigation.test.tsx`로 typed route call, deep link mapping, fallback path를 공개 게이트로 만든다.

## 섹션 설계

1. Phase 1: `NavigatorScreenParams`를 써서 route graph를 먼저 고정한다.
변경 단위: `react-native/src/navigation/types.ts`, `react-native/src/navigation/RootNavigator.tsx`
코드 앵커: `RootTabParamList`, `RootDrawerParamList`
2. Phase 2: URL에서 nested state를 복원하고 누락된 title을 hydration한다.
변경 단위: `react-native/src/navigation/linking.ts`, `react-native/src/screens/AppScreens.tsx`
코드 앵커: `resolveNavigationState()`
3. Phase 3: Jest로 typed call, known deep link, fallback path를 잠근다.
변경 단위: `react-native/__tests__/navigation.test.tsx`
코드 앵커: `expect(homeNavigate).toHaveBeenCalledWith(...)`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `1`개 suite, `3`개 테스트 통과
- manual deep link examples: `myapp://detail/abc123`, `myapp://notifications`
- concept: deep link는 화면 점프가 아니라 nested navigation state 복원이다

## 개념 설명 포인트

- 새로 이해한 것: typed params와 deep link mapping은 따로 놀면 안 된다
- `detail/:id`가 `Detail` screen으로만 끝나지 않고 `title` hydration까지 해야 실제 앱 상태를 설명할 수 있다

## 마무리 질문

- 다음 프로젝트에서는 route graph 대신 같은 10k 데이터셋을 두 렌더링 전략에 태워 비교 가능한 benchmark로 바꾼다.
