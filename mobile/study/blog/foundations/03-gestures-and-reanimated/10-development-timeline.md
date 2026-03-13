# 03 Gestures And Reanimated

gesture 프로젝트는 자칫 데모 모음집처럼 보이기 쉽다. 이 앱이 더 흥미로운 지점은 swipe card, reorder list, shared transition dismiss를 서로 다른 기능으로 두지 않고, 모두 threshold와 복귀 규칙으로 읽히게 만들었다는 데 있다.

## 이번 글에서 따라갈 구현 순서

- `gestureMath.ts`에서 swipe/reorder/dismiss 규칙을 순수 함수로 뽑는다.
- `GesturesStudyApp.tsx`에서 세 데모를 한 앱에 묶는다.
- `gestures.test.tsx`로 threshold와 progress 계산을 잠근다.

## 새로 이해한 것: interaction 품질은 “언제가 의도인가”를 먼저 정하는 일이다

이 프로젝트의 핵심은 Reanimated API 자체가 아니다. 사용자가 어느 정도까지 움직였을 때 dismiss로 보고, 못 넘으면 어디로 spring back 시키는지, reorder는 몇 row를 넘어야 swap으로 인정하는지 같은 규칙이 먼저 있어야 animation도 설명 가능해진다.

## Phase 1
### gesture 규칙을 순수 함수로 먼저 뽑는다

- 당시 목표: swipe, reorder, dismiss의 기준을 UI 코드 밖에서 먼저 설명 가능하게 만든다.
- 변경 단위: `react-native/src/gestureMath.ts`
- 처음 가설: threshold와 progress 계산이 component 안에 섞이면 데모를 늘릴수록 규칙도 같이 흐려진다.
- 실제 진행: `getSwipeDecision()`, `getDismissProgress()`, `reorderByOffset()`를 만들고, intent 판정과 clamp 로직을 함수로 분리했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/03-gestures-and-reanimated/react-native
npm test
```

검증 신호:

- swipe threshold는 `like`, `nope`, `reset` 세 결과만 만든다.
- reorder는 row height 하나를 넘겼을 때만 index를 바꾼다.

핵심 코드:

```ts
if (translateX >= threshold) {
  return 'like';
}
if (translateX <= -threshold) {
  return 'nope';
}
return 'reset';
```

왜 이 코드가 중요했는가:

애니메이션 연출 이전에 “의도 판정”을 함수로 고정하는 지점이기 때문이다.

새로 배운 것:

- interaction 품질은 frame 효과보다 먼저 threshold 규칙을 닫는 일이다.

다음:

- 이 규칙을 실제 swipe/reorder/shared transition 데모에 연결한다.

## Phase 2
### 세 데모를 같은 vocabulary로 묶는다

- 당시 목표: swipe card, reorder list, dismiss gesture가 모두 threshold/spring/progress 언어로 읽히게 만든다.
- 변경 단위: `react-native/src/GesturesStudyApp.tsx`
- 처음 가설: 데모를 별개로 만들면 화려해 보일 수는 있어도, 왜 같은 학습 단계인지 설명하기 어렵다.
- 실제 진행: `SwipeCardDemo`는 threshold 미달 시 `withSpring(0)`으로 복귀하고, `ReorderDemo`는 `reorderByOffset()`을 호출하며, `SharedDetailScreen`은 `getDismissProgress(..., 160) > 0.6`일 때만 reverse dismiss를 수행한다.

CLI:

```bash
npm run typecheck
```

검증 신호:

- swipe/dismiss 모두 threshold를 넘지 못하면 복귀한다.
- shared transition도 dismiss progress가 충분할 때만 뒤로 간다.

핵심 코드:

```ts
if (getDismissProgress(translateY.value, 160) > 0.6) {
  translateY.value = 0;
  navigation.goBack();
  return;
}
```

왜 이 코드가 중요했는가:

shared transition을 “별도의 특수 효과”가 아니라 threshold를 공유하는 interaction으로 다시 읽게 해 주기 때문이다.

새로 배운 것:

- 서로 다른 gesture 데모도 같은 recovery rule을 공유하면 공용 vocabulary로 묶을 수 있다.

다음:

- threshold와 progress 계산이 실제 public gate가 되도록 JS 테스트로 잠근다.

## Phase 3
### JS 테스트가 gesture 규칙의 공용 게이트가 된다

- 당시 목표: 디바이스 체감과 별개로, 가장 중요한 판단 규칙은 저장소에서 깨지지 않게 만든다.
- 변경 단위: `react-native/tests/gestures.test.tsx`
- 처음 가설: UI-thread animation fidelity는 디바이스에서 확인하더라도, threshold math는 Jest가 잡아야 한다.
- 실제 진행: swipe decision, reorder offset, dismiss progress clamp를 각각 테스트해 세 데모가 같은 규칙을 쓰는지 확인했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS tests/gestures.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 3 passed`

핵심 코드:

```ts
expect(getDismissProgress(80, 160)).toBe(0.5);
expect(getDismissProgress(300, 160)).toBe(1);
```

왜 이 코드가 중요했는가:

dismiss progress가 0과 1 사이에서 어떻게 해석되는지 테스트가 직접 보여 주기 때문이다.

새로 배운 것:

- gesture 프로젝트의 저장소 공용 게이트는 “멋져 보인다”가 아니라 규칙 함수가 안정적이다.

다음:

- 다음 단계에서는 interaction 규칙 대신 JS/native 경계를 benchmark와 spec으로 옮겨 다룬다.

## 여기까지 정리

- 이 프로젝트가 실제로 남긴 것은 세 개의 데모보다, threshold와 recovery rule을 공용 vocabulary로 만들었다는 사실이다.
- 다음 단계의 질문: runtime boundary와 native module boundary는 어떤 식으로 재생 가능한 증거를 만들 수 있을까?
