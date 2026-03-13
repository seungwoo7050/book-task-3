# 03 Realtime Collab Workspace

이 프로젝트는 "동기화가 된다"보다 "동기화가 어떻게 보이고 언제 깨지는가"를 설명하는 쪽에 더 가깝다. board, doc, presence, reconnect replay, conflict banner를 같은 capstone 안에 두되, 실제 backend는 빼고 프론트 상태 모델만 남겼다.

## 왜 글을 세 편으로 나눴는가

구현 전환점이 세 번 분명하게 갈린다. 먼저 협업 UI의 표면을 고정하고, 다음에 patch/presence 흐름을 묶고, 마지막에 reconnect와 conflict를 검증으로 닫는다. 한 편에 모두 넣으면 product surface와 sync invariant가 서로를 가리기 쉬워서 본문을 분리했다.

## 근거로 사용한 자료

- `frontend-portfolio/03-realtime-collab-workspace/README.md`
- `frontend-portfolio/03-realtime-collab-workspace/docs/concepts/information-architecture.md`
- `frontend-portfolio/03-realtime-collab-workspace/docs/concepts/presence-and-patch-flow.md`
- `frontend-portfolio/03-realtime-collab-workspace/next/src/components/workspace-shell.tsx`
- `frontend-portfolio/03-realtime-collab-workspace/next/src/hooks/use-realtime-workspace.ts`
- `frontend-portfolio/03-realtime-collab-workspace/next/src/lib/workspace-state.ts`
- `frontend-portfolio/03-realtime-collab-workspace/next/src/lib/transport.ts`
- `frontend-portfolio/03-realtime-collab-workspace/next/tests/e2e/realtime-collab.spec.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/realtime-collab-workspace`
- 2026-03-13 replay 기준 typecheck 통과, `vitest` 5개, Playwright 2개 시나리오 통과

## 읽는 순서

1. [10-building-a-visible-collab-surface.md](10-building-a-visible-collab-surface.md)
   - board, doc, presence, activity를 왜 같은 shell에 두었는지
2. [20-making-reconnect-and-presence-explicit.md](20-making-reconnect-and-presence-explicit.md)
   - optimistic patch, queue, replay, presence heartbeat를 어떻게 하나의 hook에 묶었는지
3. [30-proving-conflict-and-replay-behavior.md](30-proving-conflict-and-replay-behavior.md)
   - E2E와 debug log가 어떤 경계를 고정하는지
