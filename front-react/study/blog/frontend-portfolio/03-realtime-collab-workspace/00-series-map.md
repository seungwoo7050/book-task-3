# 03 Realtime Collab Workspace

이 capstone은 "실시간으로 같이 편집된다"를 보여 주는 데서 멈추지 않는다. 실제 구현이 더 강조하는 것은 협업 상태를 숨기지 않는 화면, optimistic patch와 remote overwrite의 구분, 연결이 끊겼을 때 queue가 어떻게 쌓이고 다시 replay되는지, 그리고 충돌을 토스트가 아니라 배너로 드러내는 product surface다. backend 없이도 multi-user mental model을 설명 가능한 프론트엔드 프로젝트로 만들려는 의도가 코드와 테스트 모두에 남아 있다.

이번 재작성은 기존 blog 문장을 입력으로 쓰지 않고 다음 근거만 사용했다. 문제와 범위는 `front-react/study/frontend-portfolio/03-realtime-collab-workspace/problem/README.md`, 공개 설계 관점은 `README.md`, `docs/README.md`, `docs/concepts/information-architecture.md`, `docs/concepts/presence-and-patch-flow.md`, 구현 경계는 `next/README.md`, `next/src/components/workspace-shell.tsx`, `next/src/hooks/use-realtime-workspace.ts`, `next/src/lib/storage.ts`, `next/src/lib/transport.ts`, `next/src/lib/workspace-state.ts`, 검증 근거는 `next/tests/unit/workspace-state.test.ts`, `next/tests/integration/realtime-collab-workspace.test.tsx`, `next/tests/e2e/realtime-collab.spec.ts`, 그리고 2026-03-14에 재실행한 `npm run verify --workspace @front-react/realtime-collab-workspace`다.

## 이 프로젝트를 읽는 질문

- 협업 앱에서 어떤 상태를 UI 표면에 노출해야 다른 사람이 모델을 이해할 수 있는가
- optimistic patch와 reconnect replay는 hook/state 계층에서 어떻게 나뉘는가
- conflict는 어떤 조건에서만 띄우고, 어디까지를 현재 구현의 한계로 남겼는가

## 문서 순서

1. [10-building-a-visible-collab-surface.md](10-building-a-visible-collab-surface.md)
   - board, doc, presence, activity, conflict banner를 왜 같은 shell에 붙였는지 정리한다.
2. [20-making-reconnect-and-presence-explicit.md](20-making-reconnect-and-presence-explicit.md)
   - optimistic patch, disconnect queue, reconnect replay, heartbeat presence가 어떻게 하나의 runtime으로 묶이는지 따라간다.
3. [30-proving-conflict-and-replay-behavior.md](30-proving-conflict-and-replay-behavior.md)
   - unit/integration/E2E가 어떤 경계를 고정하고 무엇은 아직 고정하지 않는지 살핀다.

## 이번에 다시 확인한 검증 상태

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study
npm run verify --workspace @front-react/realtime-collab-workspace
```

- `typecheck`: 통과
- `vitest`: 2개 파일, 5개 테스트 통과
- `playwright`: 2개 시나리오 통과
- `vitest` 중 Vite deprecation warning이 찍히지만 검증 자체는 green이다.

## 지금 문서에서 분명히 남기는 한계

- transport는 same-origin `BroadcastChannel`과 test용 memory transport뿐이다.
- conflict resolution은 last-write-wins overwrite를 배너로 드러내는 수준이지 merge 전략이 아니다.
- conflict window는 서버 시간이 아니라 각 patch의 `createdAt` 클라이언트 타임스탬프 비교에 의존한다.
- Playwright의 "두 사용자"도 실제로는 같은 browser context 안 두 페이지다. 즉 cross-device arbitration이 아니라 same-browser collaboration surface 검증에 가깝다.
- text sync는 block 단위 교체이고 cursor/selection/comment/ACL은 범위 밖이다.
