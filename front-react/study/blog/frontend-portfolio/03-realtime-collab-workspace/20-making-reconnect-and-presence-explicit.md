# Making Reconnect And Presence Explicit

visible surface를 세운 뒤 실제로 더 흥미로운 부분은 hook과 state 계층이다. 이 프로젝트는 realtime이라고 부르지만, 진짜로 푸는 문제는 transport가 언제 끊기고, local edit를 언제 먼저 보여 주고, reconnect 때 무엇을 replay하며, collaborator presence를 어느 빈도로 갱신할지다. `useRealtimeWorkspace()`와 `workspace-state.ts`는 이 질문을 한 군데로 모아 둔다.

## local patch는 먼저 적용하고, 전송 여부는 연결 상태가 결정한다

card/doc 수정은 모두 `sendPatch()`를 지난다.

```tsx
const patch = createPatchEnvelope({
  clientId: viewer.clientId,
  clientLabel: viewer.label,
  entityType,
  entityId,
  field,
  value,
  createdAt: Date.now(),
});
```

이후 흐름은 두 갈래다.

- 연결되어 있으면: `applyOptimisticPatch()`로 즉시 UI에 반영한 뒤 transport로 보낸다.
- 끊겨 있으면: optimistic apply는 그대로 하되 `queuePatch()`로 `queuedPatches`에 남긴다.

즉 사용자가 보는 값과 transport 전달 성공은 일부러 분리된다. 이 분리 덕분에 disconnected 상태에서도 편집은 계속되지만, shell에는 queued count가 쌓여 "아직 밖으로 나가지 않은 변경"임을 설명해 준다.

`workspace-state.ts`도 이 의도를 그대로 갖고 있다. optimistic patch는 `recentLocal`에 entity key별 마지막 local patch를 기록하고, activity 맨 앞에 `Optimistic ... patch` 이벤트를 남긴다. 나중에 remote overwrite가 왔을 때 conflict window를 계산할 수 있는 근거도 여기서 생긴다.

## reconnect는 단순히 online badge를 켜는 것이 아니라 queued replay를 drain하는 순간이다

`reconnect()`는 세 가지 동작을 같은 함수에서 수행한다.

1. transport를 다시 `connect()`한다.
2. online presence를 다시 broadcast한다.
3. `stateRef.current.queuedPatches`를 순서대로 `sendPatch()`한 뒤 `flushQueuedPatches()`로 큐를 비운다.

```tsx
for (const patch of stateRef.current.queuedPatches) {
  transport.sendPatch(patch);
}
startTransition(() => {
  setState((current) =>
    flushQueuedPatches(markConnected(applyPresencePing(current, onlinePresence))),
  );
});
```

이 설계가 좋은 이유는 reconnect를 "상태 표시 변경"이 아니라 "보류했던 work를 다시 내보내는 복구 시점"으로 만든다는 점이다. E2E도 정확히 이걸 확인한다. atlas 탭을 disconnect하고 `card-2`를 수정하면 rio 탭에는 값이 안 바뀐다. reconnect 후에는 그 queued patch가 replay되어 rio 쪽 값도 업데이트된다.

현재 구현의 경계도 여기서 분명하다. queue는 브라우저 메모리에만 있고, reconnect는 현재 탭의 `stateRef`에 남은 순서대로 patch를 다시 보내는 수준이다. durable offline cache나 server ack는 없다.

## presence는 patch와 같은 hook에 있지만 별도 event type으로 유지된다

presence가 중요한 이유는 데이터 동기화보다 더 직접적으로 "협업이 살아 있다"는 감각을 만들기 때문이다. 이 프로젝트는 patch와 presence를 같은 transport에서 보내지만 event type은 분리한다.

```ts
export type CollabTransportEvent =
  | { type: "patch"; patch: PatchEnvelope }
  | { type: "presence"; presence: PresenceState };
```

`useRealtimeWorkspace()`는 mount 시 online presence를 한 번 보내고, 기본 설정에서는 2.5초 heartbeat를 반복한다. remote presence는 `applyPresencePing()`으로 `presence` map에 합쳐진다. disconnect할 때는 자신의 status를 offline으로 한 번 broadcast하고, reconnect 때는 다시 online으로 전환한다.

이 구조 덕분에 presence는 데이터 mutation과 독립적으로 읽힌다. card/doc patch가 없더라도 collaborator rail은 살아 있을 수 있다. 반대로 remote patch가 도착하면 `applyRemotePatch()`가 없는 collaborator 정보를 fallback color와 label로 보강해 presence에도 반영한다. 즉 patch와 heartbeat 두 경로가 presence list를 갱신한다.

## conflict detection은 merge 전략이 아니라 "짧은 시간 내 remote overwrite"를 설명하는 배너다

`applyRemotePatch()`는 remote patch가 왔을 때 local viewer patch와 같은 entity key를 공유하고, 값이 다르고, `CONFLICT_WINDOW_MS` 12초 안이면 conflict banner를 띄운다.

```ts
const inConflictWindow =
  localPatch &&
  localPatch.value !== patch.value &&
  patch.createdAt - localPatch.createdAt <= CONFLICT_WINDOW_MS;
```

즉 현재 conflict는 sophisticated merge가 아니다. 최근 local edit 위에 remote overwrite가 들어왔다는 사실을 표면으로 올리는 규칙이다. overwrite 자체는 막지 않고, 결과 state는 remote patch 값으로 바뀐다. 이 점을 숨기지 않는 것이 오히려 이 프로젝트의 장점이다. "해결했다"가 아니라 "어디서 깨지는지 보이게 했다"에 가깝기 때문이다.

그리고 이 규칙은 서버 조정 시간 대신 클라이언트 patch의 `createdAt` 차이에 직접 기대고 있다. 즉 current conflict banner는 distributed consensus나 central ordering이 아니라 "같은 브라우저/테스트 환경에서 충분히 비슷한 시계"라는 전제 위에서만 단순하게 동작한다.

다음 글에서는 이 모델이 실제로 어떤 테스트와 브라우저 시나리오로 고정되는지 정리한다.
