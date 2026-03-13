# Evidence Ledger: 03 Gestures And Reanimated

## 독립 프로젝트 판정

- 판정: 처리
- 근거: gesture math, Reanimated UI, 테스트, 문제 정의를 모두 자기 폴더 안에 갖춘 독립 상호작용 앱이다.
- 소스 경로: `mobile/study/foundations/03-gestures-and-reanimated`

## 사용한 근거

- `mobile/study/foundations/03-gestures-and-reanimated/README.md`
- `mobile/study/foundations/03-gestures-and-reanimated/problem/README.md`
- `mobile/study/foundations/03-gestures-and-reanimated/react-native/README.md`
- `mobile/study/foundations/03-gestures-and-reanimated/docs/concepts/gesture-workflow.md`
- `mobile/study/foundations/03-gestures-and-reanimated/react-native/src/gestureMath.ts`
- `mobile/study/foundations/03-gestures-and-reanimated/react-native/src/GesturesStudyApp.tsx`
- `mobile/study/foundations/03-gestures-and-reanimated/react-native/tests/gestures.test.tsx`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/foundations/03-gestures-and-reanimated/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | 제스처 규칙을 순수 함수로 먼저 뽑는다

- 당시 목표: swipe, reorder, dismiss의 기준을 UI 코드 밖에서 먼저 설명 가능하게 만든다.
- 변경 단위: `react-native/src/gestureMath.ts`
- 처음 가설: threshold와 progress 계산이 컴포넌트 안에 섞이면 Reanimated 데모를 바꿀 때마다 규칙도 같이 흐려진다.
- 실제 조치: `getSwipeDecision()`, `getDismissProgress()`, `reorderByOffset()`를 순수 함수로 분리했다.
- CLI:
```bash
npm test
```
- 검증 신호:
- `getSwipeDecision(180, 120) -> like`
- `reorderByOffset(['a','b','c'], 0, 58, 58) -> ['b','a','c']`
- 핵심 코드 앵커:
```ts
if (translateX >= threshold) {
  return 'like';
}
...
return 'reset';
```
- 새로 배운 것: interaction 품질은 애니메이션 프레임보다 먼저 “언제가 의도인가”를 함수로 닫아야 한다.
- 다음: 이 규칙을 swipe/reorder/shared transition 데모에 연결한다.

### Phase 2 | 세 데모를 같은 vocabulary로 묶는다

- 당시 목표: swipe card, reorder list, dismiss gesture가 모두 threshold/spring/progress 언어로 읽히게 만든다.
- 변경 단위: `react-native/src/GesturesStudyApp.tsx`
- 처음 가설: 데모를 따로 만들면 화려하지만, 같은 규칙으로 설명하기는 어려워진다.
- 실제 조치: `SwipeCardDemo`, `ReorderDemo`, `SharedDetailScreen`을 한 앱에 넣고, Pan gesture와 shared transition tag를 같은 흐름으로 연결했다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- swipe는 threshold 미달 시 `withSpring(0)`으로 복귀한다.
- detail dismiss는 `getDismissProgress(..., 160) > 0.6`일 때만 뒤로 간다.
- 핵심 코드 앵커:
```ts
if (getDismissProgress(translateY.value, 160) > 0.6) {
  translateY.value = 0;
  navigation.goBack();
  return;
}
```
- 새로 배운 것: 서로 다른 interaction도 threshold와 복귀 규칙을 공유하면 같은 언어로 설명할 수 있다.
- 다음: gesture math가 실제 public gate가 되도록 테스트로 잠근다.

### Phase 3 | JS 테스트로 gesture 규칙을 고정한다

- 당시 목표: 디바이스 체감과 별개로, 가장 중요한 판단 규칙은 Jest에서 깨지지 않게 만든다.
- 변경 단위: `react-native/tests/gestures.test.tsx`
- 처음 가설: UI-thread fidelity는 디바이스에서 보더라도, threshold math는 JS 테스트에서 먼저 지켜야 한다.
- 실제 조치: swipe decision, reorder, dismiss progress clamp를 각각 테스트했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS tests/gestures.test.tsx`
- `Test Suites: 1 passed`, `Tests: 3 passed`
- 핵심 코드 앵커:
```ts
expect(getDismissProgress(80, 160)).toBe(0.5);
expect(getDismissProgress(300, 160)).toBe(1);
```
- 새로 배운 것: gesture 앱의 저장소 공용 게이트는 animation 체감이 아니라 규칙 함수의 안정성이다.
- 다음: 다음 단계에서는 UI interaction 대신 JS/native 경계 자체를 benchmark와 spec으로 설명한다.
