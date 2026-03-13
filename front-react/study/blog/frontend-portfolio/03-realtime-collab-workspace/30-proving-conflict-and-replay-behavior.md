# 30 Proving Conflict And Replay Behavior

마지막 장면은 테스트와 debug log가 경계를 어떻게 닫는가다. [`workspace-state.test.ts`](../../../frontend-portfolio/03-realtime-collab-workspace/next/tests/unit/workspace-state.test.ts)는 optimistic patch, queued replay, conflict banner를 함수 단위로 고정한다. [`realtime-collab-workspace.test.tsx`](../../../frontend-portfolio/03-realtime-collab-workspace/next/tests/integration/realtime-collab-workspace.test.tsx)는 remote presence와 overwrite가 실제 UI 표면으로 번역되는지 확인한다.

브라우저 검증의 중심은 [`realtime-collab.spec.ts`](../../../frontend-portfolio/03-realtime-collab-workspace/next/tests/e2e/realtime-collab.spec.ts)다. 두 탭을 열고, 한 탭을 끊고, patch를 queue에 쌓고, 다시 붙인 뒤 remote overwrite로 conflict banner를 띄운다. 이 흐름을 통과하면 "협업 상태가 보인다"는 주장이 단순 데모가 아니라 검증된 계약이 된다.

실패 기록도 의미가 있었다. `useEffectEvent`를 dependency에 넣어 mount effect가 재실행되던 문제와 Next route announcer가 `role="alert"`를 공유하던 문제를 고친 덕분에, 지금의 verify는 단순 green check가 아니라 현재 경계가 어디인지 보여 주는 증거가 됐다.
