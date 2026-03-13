# 02 Realtime Chat

offline sync 기초를 분리해서 다룬 다음 단계에서 바로 필요한 것은, 그 규칙을 사용자 경험 안으로 밀어 넣어도 설명이 무너지지 않는지 확인하는 일이었다. 이 프로젝트는 채팅 UI를 만들었다기보다, pending send, ack reconcile, replay, typing/presence를 같은 message lifecycle로 묶는 데 집중한다.

## 이번 글에서 따라갈 구현 순서

- `chatModel.ts`에서 message identity rule을 먼저 닫는다.
- `storageSchema.ts`와 `RealtimeChatStudyApp.tsx`에서 schema와 화면이 같은 vocabulary를 쓰게 만든다.
- `realtime-chat.test.ts`로 ack/replay/dedupe를 공개 게이트로 만든다.

## 새로 이해한 것: ack reconcile과 replay dedupe는 같은 identity rule의 다른 얼굴이다

처음 보면 ack와 replay는 서로 다른 기능처럼 보인다. 하지만 코드로 내려오면 둘 다 “이 메시지가 이미 처리된 그 메시지인가”라는 질문을 푸는 규칙이다. `clientId`, `serverId`, `eventId`의 역할을 먼저 분리해야 UI와 storage schema도 흔들리지 않는다.

## Phase 1
### message lifecycle를 먼저 정의한다

- 당시 목표: pending send, ack reconcile, replay filter, dedupe 규칙을 UI 밖에서 먼저 닫는다.
- 변경 단위: `react-native/src/chatModel.ts`
- 처음 가설: 채팅 앱에서 가장 위험한 부분은 화면보다 identity rule이다.
- 실제 진행: `createPendingMessage()`, `reconcileAck()`, `applyReplayEvents()`, `dedupeReplay()`, `updateTypingState()`를 분리해 pending, sent, replay-safe 처리를 하나의 model vocabulary로 묶었다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/02-realtime-chat/react-native
npm test
```

검증 신호:

- ack는 `clientId`를 기준으로 pending message를 `sent`로 바꾼다.
- replay는 `eventId > lastEventId`만 통과시키고 `serverId`로 dedupe한다.

핵심 코드:

```ts
export function reconcileAck(messages, ack) {
  return messages.map(message =>
    message.clientId === ack.clientId
      ? { ...message, serverId: ack.serverId, status: 'sent' }
      : message,
  );
}
```

왜 이 코드가 중요했는가:

pending send와 server ack가 한 모델 안에서 만나는 지점이기 때문이다.

새로 배운 것:

- pending/ack/replay는 분리된 기능이 아니라 같은 identity rule의 다른 표면이다.

다음:

- schema와 UI가 이 모델을 그대로 읽도록 연결한다.

## Phase 2
### schema와 UI가 같은 모델을 읽는다

- 당시 목표: local-first message model이 storage schema와 화면에서 동시에 드러나게 만든다.
- 변경 단위: `react-native/src/storageSchema.ts`, `react-native/src/RealtimeChatStudyApp.tsx`
- 처음 가설: schema가 문서로만 남으면 replay-safe 채팅 모델을 실제 앱 흐름으로 설명하기 어렵다.
- 실제 진행: `chatSchemaSummary`로 `messages` 테이블을 요약하고, 앱은 pending message와 sent message를 같은 리스트에 렌더링하면서 typing user 수와 schema table 수를 함께 보여 줬다.

CLI:

```bash
npm run typecheck
```

검증 신호:

- schema는 `messages` 하나를 canonical table로 둔다.
- 화면은 `pending`과 `sent` 메시지를 같은 conversation list에 배치한다.

핵심 코드:

```ts
const messages = [
  createPendingMessage('general', 'client-1', 'Offline hello'),
  { clientId: 'client-2', serverId: 'srv-2', conversationId: 'general', text: 'Acked reply', status: 'sent' as const },
];
```

왜 이 코드가 중요했는가:

local-first 채팅 모델이 화면과 schema 둘 다에서 같은 lifecycle vocabulary를 유지하는 지점이기 때문이다.

새로 배운 것:

- schema와 UI가 같은 언어를 써야 local-first 모델이 “설명”이 아니라 “구현”이 된다.

다음:

- ack/replay/dedupe를 JS 테스트로 잠근다.

## Phase 3
### message lifecycle을 저장소 공용 게이트로 만든다

- 당시 목표: 채팅 앱의 핵심 위험을 UI snapshot이 아니라 model test로 고정한다.
- 변경 단위: `react-native/tests/realtime-chat.test.ts`
- 처음 가설: 이 프로젝트의 핵심은 animation보다 message lifecycle이므로 Jest만으로도 중요한 리스크를 잡을 수 있다.
- 실제 진행: ack reconcile, `lastEventId` filtering, replay dedupe, typing state를 각각 테스트했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS tests/realtime-chat.test.ts`
- `Test Suites: 1 passed`
- `Tests: 3 passed`

핵심 코드:

```ts
expect(
  applyReplayEvents(
    [
      { eventId: 1, serverId: 'srv-1', text: 'old' },
      { eventId: 2, serverId: 'srv-2', text: 'new' },
    ],
    1,
  ),
).toEqual([{ eventId: 2, serverId: 'srv-2', text: 'new' }]);
```

왜 이 코드가 중요했는가:

replay-safe rule이 실제로 무엇을 버리고 무엇을 남기는지 가장 짧게 보여 주기 때문이다.

새로 배운 것:

- 채팅 앱의 최소 공용 게이트는 메시지가 보이는지가 아니라 identity rule이 깨지지 않는지다.

다음:

- 검증된 chat snapshot을 이제 release candidate로 복제해 배포 discipline 문제를 따로 다룬다.

## 여기까지 정리

- 이 프로젝트가 실제로 만든 것은 채팅 화면보다, pending/ack/replay를 같은 lifecycle로 읽는 local-first message model이다.
- 다음 단계의 질문: 제품 동작이 검증된 뒤에는 release discipline을 어떤 artifact와 automation으로 남겨야 할까?
