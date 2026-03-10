# Knowledge Index — Realtime Chat

## 연결된 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| `offline-sync-foundations` | 이 프로젝트의 선행 과제. queue/retry/DLQ 기초를 여기서 먼저 다졌다. |
| `app-distribution` | 이 프로젝트의 후행 과제. 여기서 만든 앱을 스냅샷해서 배포 리허설에 사용한다. |
| `incident-ops-mobile` | 실제 WebSocket 서버와 연결해서 replay를 검증하는 캡스톤 과제. |
| `incident-ops-mobile-client` | 이 프로젝트의 WebSocket replay 패턴을 실제 제품으로 구현한 최종 캡스톤. |

## 재사용 가능한 패턴

### clientId / serverId 이중 identity 패턴
로컬에서 먼저 생성하고 서버가 나중에 확인하는 모든 리소스에 적용할 수 있다.
`offline-sync-foundations`의 `localId` / `serverId`와 동일한 원리다.

### eventId + serverId 이중 필터 replay 패턴
`applyReplayEvents`(시간순 컷오프) + `dedupeReplay`(identity 기준 중복 제거) 조합은
채팅뿐 아니라 알림, 피드, 실시간 로그 등 모든 이벤트 스트림 재연결에 재사용 가능하다.

### ephemeral vs. durable 분리 원칙
typing/presence처럼 휘발성 상태는 DB에 넣지 않는다.
이 원칙은 connection 상태, 로딩 상태, 에러 상태 등 다른 앱에서도 동일하게 적용된다.

## 핵심 파일 참조

| 파일 | 역할 |
|------|------|
| `react-native/src/chatModel.ts` | 핵심 도메인 로직 (순수 함수) |
| `react-native/src/storageSchema.ts` | WatermelonDB 스키마 정의 |
| `react-native/src/RealtimeChatStudyApp.tsx` | FlashList 기반 UI shell |
| `react-native/tests/realtime-chat.test.ts` | ack, replay, dedupe, typing 테스트 |
| `docs/concepts/replay-and-ack.md` | 공개 문서용 개념 설명 |

## 이 프로젝트에서 사용한 도구와 버전

- React Native 0.84.1
- WatermelonDB ^0.28.0
- FlashList (Shopify) ^2.2.0
- NetInfo ^12.0.1
- TypeScript ^5.8.3
- Jest ^29.6.3
