# 문제 정의 — Realtime Collab Workspace

## 왜 이 프로젝트인가

앞선 포트폴리오 프로젝트 두 개는 "혼자 쓰는 제품"에 가까웠다. `01-ops-triage-console`은 운영자의 dense workflow를, `02-client-onboarding-portal`은 고객-facing flow를 보여 줬다. 하지만 협업 제품에서는 다른 긴장이 생긴다. 값이 바뀌는 순간뿐 아니라, 누가 보고 있는지, 연결이 끊겼는지, 나중에 다시 붙었을 때 무엇이 replay되는지까지 함께 설계해야 한다.

`Realtime Collab Workspace`는 이 빈자리를 채운다. 실제 backend 없이도 collaboration mental model을 충분히 설명할 수 있는지를 묻는 프론트 capstone이다.

## 사용자 시나리오

1. 두 명의 사용자가 같은 워크스페이스를 두 탭에서 연다.
2. 보드 카드나 문서 블록을 수정하면 다른 탭에 반영된다.
3. 한 탭이 잠깐 끊긴 상태에서도 수정은 이어지고, 다시 연결되면 queued patch가 replay된다.
4. 같은 항목을 짧은 시간 안에 서로 다르게 수정하면 conflict banner가 뜬다.

## 이 프로젝트가 보여 주는 역량

- optimistic patch와 queue/replay 모델 설계
- collaborator presence를 데이터 변경과 분리한 event 모델
- product surface로서의 conflict banner와 activity log
- mock transport와 deterministic 테스트 경계 설계

## 기술 선택 이유

| 기술 | 이유 |
| --- | --- |
| Next.js 16 | App Router와 시연용 case-study route 구성 |
| React 19 | `useEffectEvent`, `startTransition`, `useDeferredValue` 활용 |
| BroadcastChannel | backend 없이 same-origin multi-tab sync 재현 |
| Memory transport | unit/integration에서 deterministic 테스트 확보 |
| Vitest + Testing Library | 상태 모델과 UI 반영을 빠르게 검증 |
| Playwright | 두 탭 협업 시나리오를 브라우저 수준에서 검증 |
