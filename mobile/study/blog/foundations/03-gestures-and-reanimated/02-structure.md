# Structure Plan: 03 Gestures And Reanimated

## 글의 중심 질문

- 이 프로젝트는 “멋진 데모를 만든다”보다 “상호작용 규칙을 같은 vocabulary로 설명한다”에 더 가깝다. swipe, reorder, dismiss를 모두 threshold, spring, progress 언어로 묶는 순서가 핵심이다.

## 구현 순서 요약

- `gestureMath.ts`에서 swipe/reorder/dismiss 규칙을 순수 함수로 뽑는다.
- `GesturesStudyApp.tsx`에서 세 데모를 같은 규칙 위에 올린다.
- `gestures.test.tsx`로 threshold와 progress 계산을 공개 게이트로 만든다.

## 섹션 설계

1. Phase 1: gesture math를 먼저 뽑아 규칙을 고정한다.
변경 단위: `react-native/src/gestureMath.ts`
코드 앵커: `getSwipeDecision()`, `getDismissProgress()`
2. Phase 2: swipe, reorder, shared transition을 한 앱에서 같은 vocabulary로 묶는다.
변경 단위: `react-native/src/GesturesStudyApp.tsx`
코드 앵커: dismiss threshold `> 0.6`
3. Phase 3: JS 테스트로 규칙 함수를 잠근다.
변경 단위: `react-native/tests/gestures.test.tsx`
코드 앵커: `expect(getDismissProgress(...)).toBe(...)`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `1`개 suite, `3`개 테스트 통과
- concept: swipe, reorder, dismiss는 모두 threshold와 spring-back 규칙으로 설명할 수 있다

## 개념 설명 포인트

- 새로 이해한 것: interaction 품질은 애니메이션 구현보다 의도 판정 규칙을 먼저 닫는 일이다
- shared transition도 별도 장르가 아니라 dismiss threshold를 공유하는 흐름으로 읽을 수 있다

## 마무리 질문

- 다음 프로젝트에서는 체감 규칙 대신 JS/native 경계를 어떤 spec과 benchmark로 남길지 다룬다.
