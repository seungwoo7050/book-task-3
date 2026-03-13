# 접근 과정 — Realtime Collab Workspace 구현 기록

## 상태 모델부터 먼저 고정

이 프로젝트의 시작점은 화면이 아니라 `PatchEnvelope`였다. board card와 doc block이 시각적으로는 다르지만, 협업 규칙은 거의 같다고 판단했다. 그래서 `entityType`, `entityId`, `field`, `value`, `createdAt`, `clientLabel`을 가진 공통 patch shape를 먼저 만들고 두 surface가 모두 이 경로를 타게 했다.

## transport를 두 종류로 분리

브라우저 데모용으로는 `BroadcastChannelTransport`가 가장 자연스러웠다. 하지만 테스트까지 같은 transport를 쓰면 재현성이 떨어진다. 그래서 `MemoryCollabTransport`를 따로 두어 integration test에서는 직접 remote presence와 patch를 주입할 수 있게 만들었다.

## conflict를 감추지 않기

overwrite를 조용히 적용해도 앱은 "동작"한다. 하지만 학습용 capstone으로는 설명이 빈약해진다. 그래서 최근 local patch와 remote patch가 같은 entity를 짧은 시간 안에 덮어쓸 때 banner를 올리는 규칙을 남겼다. 이 선택 덕분에 sync가 깨지는 순간도 UI에서 읽을 수 있게 됐다.
