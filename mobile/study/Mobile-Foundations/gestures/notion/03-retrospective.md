# Retrospective — Gestures

## 가장 크게 배운 것

제스처 구현에서 가장 어려운 부분은 제스처 인식이 아니라 **"의도 판단"과 "전환 애니메이션"**이었다.

Pan 제스처의 좌표값을 받는 건 라이브러리가 해준다. 하지만 "이 이동량이 swipe 의도인가, 실수인가?"를 판단하고, 의도라면 "어떤 물리적 느낌으로 전환할 것인가?"를 결정하는 건 전적으로 개발자의 몫이다. threshold, spring 파라미터, timing duration 같은 숫자 하나하나가 앱의 "느낌"을 결정한다.

## 예상과 달랐던 것

**순수 함수 분리가 제스처에서도 통했다.** 제스처는 "UI 스레드에서 돌아가는 코드"라서 테스트가 불가능할 거라 생각했는데, 판단 로직을 순수 함수로 꺼내니 JS 스레드에서 정상적으로 테스트할 수 있었다. 핵심은 "무엇을 할 것인가"와 "어떻게 보여줄 것인가"를 분리하는 것이었다.

**Spring 파라미터 튜닝에 생각보다 시간이 많이 들었다.** 코드로는 `damping: 16, stiffness: 190` 한 줄이지만, 이 값에 도달하기까지 시뮬레이터에서 수십 번 테스트했다. 이런 "느낌 튜닝"은 자동화된 테스트로 검증할 수 없고, 직접 만져봐야 알 수 있다.

## 약했던 점

- Reorder Demo가 실제 drag가 아닌 tap 시뮬레이션이어서, 진짜 drag-to-reorder의 UX 문제(auto-scroll, drop 위치 피드백)를 체험하지 못했다.
- Haptic 피드백이 `Vibration.vibrate()`로 대체되어 있어서, 실제 iOS Haptic Engine의 fine-grained control을 다루지 않았다.
- Shared Transition이 시뮬레이터에서는 미묘하게만 보여서, 실기기에서의 차이를 확인하지 못했다.

## 다음 단계에 넘긴 것

- 실제 drag-to-reorder with auto-scroll → 프로덕션 수준의 구현 필요 시
- Haptic Engine 네이티브 모듈 → `native-modules` 프로젝트에서 spec 정의
- 복잡한 multi-gesture composition → 후속 학습 과제
