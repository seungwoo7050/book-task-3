# 10 Building A Visible Collab Surface

첫 전환점은 sync 알고리즘이 아니라 화면 배치였다. [`workspace-shell.tsx`](../../../frontend-portfolio/03-realtime-collab-workspace/next/src/components/workspace-shell.tsx)는 board card, doc block, presence, activity, conflict banner를 한꺼번에 노출한다. 이 선택 덕분에 사용자는 값을 바꾸는 순간과 transport 상태를 같은 시야 안에서 읽을 수 있다.

흥미로운 점은 board와 doc가 시각적으로 달라도 상태 표면은 거의 같다는 것이다. 둘 다 entity id를 갖고, 수정자는 `updatedBy`로 남고, input/textarea에서 같은 patch 흐름을 탄다. 그래서 이 capstone은 화면 수를 늘리는 대신 "서로 다른 UI가 같은 sync 규칙을 공유한다"는 사실을 더 강하게 드러낸다.

결국 첫 장면의 메시지는 단순하다. 협업 앱에서 화면 밀도보다 중요한 것은 현재 sync 상황을 감추지 않는 배치다.
