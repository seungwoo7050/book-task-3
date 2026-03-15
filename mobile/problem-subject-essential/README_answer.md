# mobile 핵심 답안지

이 문서는 모바일 핵심 과제를 source-first로 해설하는 답안지다. 각 항목은 실제 React Native source와 테스트만을 기준으로, 구현 순서와 판단 기준을 이 문서만 읽고도 재구성할 수 있게 적는다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-navigation-patterns-react-native](01-navigation-patterns-react-native_answer.md) | Stack, Tab, Drawer를 중첩한 React Native 앱을 만들고, external URL이 특정 화면으로 바로 진입하도록 Deep Linking까지 연결하는 과제다. 핵심은 titleMap와 AppHeader, styles 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test` |
| [01-offline-sync-foundations-react-native](01-offline-sync-foundations-react-native_answer.md) | deterministic fake sync service를 사용해 outbox, retry, DLQ, idempotency, pull-after-push merge 규칙을 검증한다. 핵심은 seeded와 snapshot, OfflineSyncStudyApp 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test` |
| [02-realtime-chat-react-native](02-realtime-chat-react-native_answer.md) | offline send, ack reconcile, replay from lastEventId, typing/presence update를 하나의 local-first message model로 검증하는 채팅 과제다. 핵심은 createPendingMessage와 reconcileAck, applyReplayEvents 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test` |
| [02-virtualized-list-performance-react-native](02-virtualized-list-performance-react-native_answer.md) | 같은 10k 데이터셋을 FlatList baseline과 FlashList v2 optimized path에 적용해 pagination, mount count, benchmark summary를 비교하는 앱을 만든다. 핵심은 SAMPLE_BENCHMARK와 computeBenchmarkSummary, ITEM_TYPES 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test && make benchmark` |
| [03-gestures-and-reanimated-react-native](03-gestures-and-reanimated-react-native_answer.md) | Swipe card, reorder list, shared transition 세 기능을 구현해 Gesture Handler와 Reanimated 기반 상호작용을 검증한다. 핵심은 애니메이션이 UI thread 중심으로 동작하고, gesture 종료 조건과 spring 동작을 설명 가능하게 만드는 것이다. 핵심은 getSwipeDecision와 getDismissProgress, reorderByOffset 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
