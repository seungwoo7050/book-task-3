# Evidence Ledger: 02 Realtime Chat

## 독립 프로젝트 판정

- 판정: 처리
- 근거: pending/ack/replay 문제를 local-first message model, schema, RN UI, tests로 독립 복원할 수 있다.
- 소스 경로: `mobile/study/product-systems/02-realtime-chat`

## 사용한 근거

- `mobile/study/product-systems/02-realtime-chat/README.md`
- `mobile/study/product-systems/02-realtime-chat/problem/README.md`
- `mobile/study/product-systems/02-realtime-chat/react-native/README.md`
- `mobile/study/product-systems/02-realtime-chat/docs/concepts/replay-and-ack.md`
- `mobile/study/product-systems/02-realtime-chat/react-native/src/chatModel.ts`
- `mobile/study/product-systems/02-realtime-chat/react-native/src/storageSchema.ts`
- `mobile/study/product-systems/02-realtime-chat/react-native/src/RealtimeChatStudyApp.tsx`
- `mobile/study/product-systems/02-realtime-chat/react-native/tests/realtime-chat.test.ts`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/02-realtime-chat/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | message lifecycle를 먼저 정의한다

- 당시 목표: pending send, ack reconcile, replay filter, dedupe 규칙을 순수 함수로 먼저 닫는다.
- 변경 단위: `react-native/src/chatModel.ts`
- 처음 가설: 채팅 UI보다 message identity 규칙이 먼저 정해져야 replay와 ack가 한 모델을 공유한다.
- 실제 조치: `createPendingMessage()`, `reconcileAck()`, `applyReplayEvents()`, `dedupeReplay()`, `updateTypingState()`를 분리했다.
- CLI:
```bash
npm test
```
- 검증 신호:
- ack는 `clientId`로 pending message를 찾고 `serverId`와 `sent` 상태를 채운다.
- replay는 `eventId > lastEventId`만 남기고 `serverId` 기준으로 dedupe한다.
- 핵심 코드 앵커:
```ts
export function reconcileAck(messages, ack) {
  return messages.map(message =>
    message.clientId === ack.clientId
      ? { ...message, serverId: ack.serverId, status: 'sent' }
      : message,
  );
}
```
- 새로 배운 것: pending/ack/replay는 별도 기능이 아니라 같은 identity rule의 다른 표면이다.
- 다음: 이 모델을 schema와 UI에 연결한다.

### Phase 2 | schema와 UI가 같은 모델을 읽는다

- 당시 목표: local-first message model이 storage schema와 화면에서 동시에 드러나게 만든다.
- 변경 단위: `react-native/src/storageSchema.ts`, `react-native/src/RealtimeChatStudyApp.tsx`
- 처음 가설: schema가 문서 밖에 있으면 replay-safe 모델을 사용자 경험과 연결하기 어렵다.
- 실제 조치: `chatSchemaSummary`로 table 이름을 요약하고, 앱은 pending message와 sent message를 같은 리스트에 렌더링하며 typing user 수와 schema table을 같이 보여 줬다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- schema는 `messages` 테이블 하나를 canonical source로 둔다.
- 화면은 `pending`과 `sent` 메시지를 같은 room list에서 보여 준다.
- 핵심 코드 앵커:
```ts
const messages = [
  createPendingMessage('general', 'client-1', 'Offline hello'),
  { clientId: 'client-2', serverId: 'srv-2', ..., status: 'sent' as const },
];
```
- 새로 배운 것: local-first 앱은 schema와 화면이 같은 lifecycle vocabulary를 공유할 때 설명 가능해진다.
- 다음: replay와 ack 규칙을 Jest로 잠근다.

### Phase 3 | replay와 ack를 저장소 공용 게이트로 만든다

- 당시 목표: 채팅 앱의 핵심 위험을 UI snapshot이 아니라 model test로 고정한다.
- 변경 단위: `react-native/tests/realtime-chat.test.ts`
- 처음 가설: 이 프로젝트의 핵심은 animation보다 message lifecycle이므로 JS 테스트만으로도 많은 리스크를 잡을 수 있다.
- 실제 조치: ack reconcile, `lastEventId` filtering, replay dedupe, typing state를 각각 테스트했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS tests/realtime-chat.test.ts`
- `Test Suites: 1 passed`, `Tests: 3 passed`
- 핵심 코드 앵커:
```ts
expect(
  applyReplayEvents(
    [{ eventId: 1, serverId: 'srv-1', text: 'old' }, { eventId: 2, serverId: 'srv-2', text: 'new' }],
    1,
  ),
).toEqual([{ eventId: 2, serverId: 'srv-2', text: 'new' }]);
```
- 새로 배운 것: 채팅 앱의 최소 공용 게이트는 “메시지가 보인다”가 아니라 “message identity rule이 깨지지 않는다”다.
- 다음: 다음 프로젝트에서는 검증된 chat snapshot을 release candidate로 복제해 배포 리허설 문제를 따로 다룬다.
