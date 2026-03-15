# mobile 핵심 문제지

여기서 `essential`은 모바일 학습에서 가장 먼저 읽어야 하는 핵심 경로라는 뜻입니다. 화면 구조, 성능, 제스처, offline/realtime 같은 제품 앱의 바닥 문제만 남깁니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-navigation-patterns-react-native](01-navigation-patterns-react-native.md) | Stack, Tab, Drawer를 중첩한 React Native 앱을 만들고, external URL이 특정 화면으로 바로 진입하도록 Deep Linking까지 연결하는 과제다. | `make test` |
| [01-offline-sync-foundations-react-native](01-offline-sync-foundations-react-native.md) | deterministic fake sync service를 사용해 outbox, retry, DLQ, idempotency, pull-after-push merge 규칙을 검증한다. | `make test && make app-build && make app-test` |
| [02-realtime-chat-react-native](02-realtime-chat-react-native.md) | offline send, ack reconcile, replay from lastEventId, typing/presence update를 하나의 local-first message model로 검증하는 채팅 과제다. | `make test && make app-build && make app-test` |
| [02-virtualized-list-performance-react-native](02-virtualized-list-performance-react-native.md) | 같은 10k 데이터셋을 FlatList baseline과 FlashList v2 optimized path에 적용해 pagination, mount count, benchmark summary를 비교하는 앱을 만든다. | `make test && make app-build && make app-test && make benchmark` |
| [03-gestures-and-reanimated-react-native](03-gestures-and-reanimated-react-native.md) | Swipe card, reorder list, shared transition 세 기능을 구현해 Gesture Handler와 Reanimated 기반 상호작용을 검증한다. 핵심은 애니메이션이 UI thread 중심으로 동작하고, gesture 종료 조건과 spring 동작을 설명 가능하게 만드는 것이다. | `make test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
