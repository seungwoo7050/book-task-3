# 20 Making Reconnect And Presence Explicit

두 번째 전환점은 [`use-realtime-workspace.ts`](../../../frontend-portfolio/03-realtime-collab-workspace/next/src/hooks/use-realtime-workspace.ts)를 읽을 때 드러난다. 이 hook은 local edit를 먼저 `applyOptimisticPatch()`로 반영하고, transport가 끊겨 있으면 `queuePatch()`로 돌려 세운다. reconnect 시에는 queued patch를 다시 보내고 `flushQueuedPatches()`로 log를 남긴다.

presence도 같은 hook 안에 있지만 mutation과는 분리된 event type으로 유지했다. 이 결정이 중요한 이유는 collaborator 존재 신호와 데이터 변경 신호가 사용자의 해석 방식이 다르기 때문이다. patch는 값을 바꾸고, presence는 "지금 협업이 살아 있다"는 신뢰를 준다.

이 프로젝트가 backend-less mock transport를 택한 이유도 여기서 분명해진다. 실제 서버 없이도 optimistic patch, disconnect, replay, presence heartbeat의 mental model은 충분히 검증할 수 있기 때문이다.
