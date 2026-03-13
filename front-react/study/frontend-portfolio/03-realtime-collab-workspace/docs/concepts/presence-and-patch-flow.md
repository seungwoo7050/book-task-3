# Presence And Patch Flow

이 프로젝트의 핵심 상태 모델은 form validation이 아니라 patch 흐름이다. `workspace-state.ts`는 board card와 doc block을 같은 `PatchEnvelope`로 다루고, `use-realtime-workspace.ts`는 그 patch를 optimistic apply, queue, replay, remote apply의 네 단계로 흘린다.

## 핵심 선택

- local edit는 먼저 UI에 적용한다.
- transport가 끊기면 patch를 버리지 않고 queue에 쌓는다.
- reconnect되면 queued patch를 순서대로 다시 보낸다.
- 같은 entity를 짧은 시간 안에 다른 탭이 덮어쓰면 conflict banner를 노출한다.

## 왜 presence를 별도 모델로 두는가

presence는 데이터 동기화보다 가벼운 heartbeat지만, 실제 사용자에게는 "협업이 살아 있다"는 가장 즉각적인 신호다. 그래서 patch 흐름과 같은 hook 안에서 처리하되, 데이터 mutation과는 별도 event type으로 유지했다.

## 현재 경계

- last-write-wins 이상의 merge 규칙은 없다.
- text patch는 block 전체를 교체한다.
- collaborator cursor나 selection broadcast는 아직 없다.
