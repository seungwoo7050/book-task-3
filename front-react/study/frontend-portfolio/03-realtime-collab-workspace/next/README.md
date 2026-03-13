# Next.js 구현

상태: `verified`

## 이 구현이 답하는 범위

- same-origin multi-tab collaboration
- optimistic board/doc patch
- reconnect replay와 queued patch drain
- presence heartbeat
- visible conflict surface
- unit, integration, E2E 검증

## 핵심 파일

- `app/`: App Router 엔트리와 case-study route
- `src/components/workspace-shell.tsx`: board, doc, presence, conflict UI
- `src/hooks/use-realtime-workspace.ts`: transport lifecycle과 optimistic state orchestration
- `src/lib/workspace-state.ts`: patch/replay/conflict 규칙
- `src/lib/transport.ts`: `BroadcastChannelTransport`, `MemoryCollabTransport`
- `tests/`: unit, integration, E2E 검증

## 실행과 검증

```bash
cd study
npm run dev --workspace @front-react/realtime-collab-workspace
npm run verify --workspace @front-react/realtime-collab-workspace
```

## 현재 한계

- 실제 서버와 durable event log는 없다.
- 같은 entity를 마지막 write로 덮어쓰는 단순 conflict surface만 다룬다.
- 문서 편집은 block-level patch이며 rich text merge는 포함하지 않는다.
