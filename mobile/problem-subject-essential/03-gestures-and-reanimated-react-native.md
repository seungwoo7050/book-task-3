# 03-gestures-and-reanimated-react-native 문제지

## 왜 중요한가

navigation과 list 성능이 "구조"를 다뤘다면, 이 프로젝트는 "체감 품질"을 다룬다. 이 단계가 있어야 이후 제품형 앱에서 사용자의 손맛과 복귀 애니메이션을 설계 관점으로 설명할 수 있다.

## 목표

Swipe card, reorder list, shared transition 세 기능을 구현해 Gesture Handler와 Reanimated 기반 상호작용을 검증한다. 핵심은 애니메이션이 UI thread 중심으로 동작하고, gesture 종료 조건과 spring 동작을 설명 가능하게 만드는 것이다.

## 시작 위치

- `../study/foundations/03-gestures-and-reanimated/react-native/src/gestureMath.ts`
- `../study/foundations/03-gestures-and-reanimated/react-native/src/GesturesStudyApp.tsx`
- `../study/foundations/03-gestures-and-reanimated/react-native/.eslintrc.js`
- `../study/foundations/03-gestures-and-reanimated/react-native/.prettierrc.js`
- `../study/foundations/03-gestures-and-reanimated/react-native/tests/gestures.test.tsx`
- `../study/foundations/03-gestures-and-reanimated/problem/script/verify_task.sh`
- `../study/foundations/03-gestures-and-reanimated/react-native/app.json`
- `../study/foundations/03-gestures-and-reanimated/react-native/ios/NavigationPatternsStudy/Images.xcassets/AppIcon.appiconset/Contents.json`

## starter code / 입력 계약

- `../study/foundations/03-gestures-and-reanimated/react-native/src/gestureMath.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 기존 gestures 과제 요구사항
- threshold와 spring snap이 있는 swipe card
- long press 기반 reorder list
- haptic feedback과 visual feedback

## 제외 범위

- `../study/foundations/03-gestures-and-reanimated/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `getSwipeDecision`와 `getDismissProgress`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `gesture math helpers`와 `calculates swipe decisions from threshold`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/foundations/03-gestures-and-reanimated/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test`가 통과한다.

## 검증 방법

```bash
make test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/03-gestures-and-reanimated/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/03-gestures-and-reanimated/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-gestures-and-reanimated-react-native_answer.md`](03-gestures-and-reanimated-react-native_answer.md)에서 확인한다.
