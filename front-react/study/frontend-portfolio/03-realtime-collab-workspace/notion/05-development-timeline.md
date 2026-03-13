# 개발 타임라인 — Realtime Collab Workspace

## Phase 0

- Next.js App Router + Vitest + Playwright scaffold 복사
- package 이름과 workspace 명령을 `@front-react/realtime-collab-workspace`로 정리

## Phase 1

- `PresenceState`, `PatchEnvelope`, `WorkspaceState` 정의
- board/doc 초기 상태와 viewer identity 설계
- `workspace-state.ts`에서 optimistic patch, queue, replay, conflict 규칙 구현

## Phase 2

- `BroadcastChannelTransport`와 `MemoryCollabTransport` 분리
- `use-realtime-workspace.ts`로 transport lifecycle, heartbeat, reconnect orchestration 구성
- `workspace-shell.tsx`에서 board/doc/presence/activity/conflict UI 완성

## Phase 3

- unit/integration/E2E 테스트 추가
- `useEffectEvent` dependency 버그 수정
- conflict banner selector 충돌 수정
- 최종 verify: `npm run verify --workspace @front-react/realtime-collab-workspace`
