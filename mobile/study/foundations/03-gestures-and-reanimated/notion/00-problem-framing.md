# Problem Framing — Gestures

## 이 프로젝트는 어떤 질문에서 시작했나

모바일 앱에서 제스처는 단순한 버튼 클릭과 근본적으로 다르다. 손가락이 화면 위를 움직이는 동안 UI가 실시간으로 반응해야 하고, 손가락을 떼는 순간 "의도"가 결정되며, 그 이후에는 물리 엔진처럼 자연스러운 애니메이션이 이어져야 한다.

이 모든 것이 JS 스레드가 아닌 UI 스레드에서 일어나야 한다는 제약이, React Native에서 제스처를 어렵게 만드는 핵심이다.

이 프로젝트는 세 가지 서로 다른 제스처 패턴 — Swipe Card, Drag-to-Reorder, Shared Transition — 을 하나의 앱에서 구현함으로써, Reanimated 4와 Gesture Handler 2의 상호작용을 체감하는 과제다.

## 풀어야 했던 세 가지 문제

1. **Tinder-style Swipe Card** — Pan 제스처를 따라 카드가 움직이고, threshold를 넘으면 날아가고, 아니면 spring으로 돌아오는 패턴
2. **Drag-to-Reorder List** — 아이템을 길게 눌러 들어올리고, 드래그해서 위치를 바꾸는 패턴
3. **Shared Element Transition** — 화면 전환 시 같은 요소가 자연스럽게 이동하고, 아래로 스와이프하면 되돌아가는 패턴

## 세 패턴에 공통된 질문

세 데모 모두 같은 세 가지 질문을 다룬다:
- 사용자의 터치 입력이 "의도"로 바뀌는 기준은 어디인가? (threshold)
- threshold를 넘지 못했을 때 상태는 어떻게 복원되나? (spring back)
- threshold를 넘었을 때 어떤 전환이 일어나나? (timing/spring으로 최종 상태)

## 명시적으로 하지 않은 것

- 복잡한 multi-touch 제스처 (pinch-to-zoom 등)
- 실제 이미지/데이터를 사용한 카드 스택
- Haptic 피드백의 네이티브 모듈 연동 (Vibration API만 사용)
- 자동화된 제스처 시뮬레이션 테스트

## 이 과제가 학습 경로에서 차지하는 위치

`foundations` 그룹의 첫 번째 과제로서, React Native에서 가장 "네이티브 느낌"이 중요한 영역을 다룬다. 이후 `navigation`에서는 화면 전환 구조를, `virtualized-list`에서는 대량 데이터 렌더링 성능을 다룬다.
