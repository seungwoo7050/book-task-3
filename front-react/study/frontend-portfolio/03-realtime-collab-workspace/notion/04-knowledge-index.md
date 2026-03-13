# 지식 인덱스 — Realtime Collab Workspace

## 핵심 타입

- `PresenceState`: collaborator identity와 상태
- `PatchEnvelope`: optimistic/local/remote patch 공통 shape
- `WorkspaceState`: board, docs, presence, queue, activity, conflict를 묶은 루트 상태
- `ConflictResolutionState`: banner 노출과 entity key 추적

## 핵심 구현 앵커

- `next/src/components/workspace-shell.tsx`
- `next/src/hooks/use-realtime-workspace.ts`
- `next/src/lib/workspace-state.ts`
- `next/src/lib/transport.ts`
- `next/tests/unit/workspace-state.test.ts`
- `next/tests/integration/realtime-collab-workspace.test.tsx`
- `next/tests/e2e/realtime-collab.spec.ts`

## 핵심 질문

- optimistic patch를 언제 local에 먼저 적용하는가
- disconnect 동안 patch를 어떻게 보관하는가
- reconnect 시 어떤 순서로 replay하는가
- remote overwrite를 사용자에게 어디서 보여 주는가
