# 03-realtime-collab-workspace 문제지

## 왜 중요한가

Realtime Collab Workspace는 협업 보드와 문서 편집기를 같은 화면 안에 놓고, "동기화가 보이는 제품"을 만드는 capstone이다. 핵심은 단순한 라이브 업데이트가 아니라, local optimistic patch, collaborator presence, reconnect replay, conflict banner를 어디까지 노출해야 사용자가 현재 상태를 이해할 수 있는가에 있다.

## 목표

시작 위치의 구현을 완성해 외부 backend 없이 완결된 데모여야 한다, 브라우저 탭 두 개만으로 협업 시나리오를 재현할 수 있어야 한다, disconnect/reconnect, queued replay, 충돌 노출이 테스트 가능해야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/frontend-portfolio/03-realtime-collab-workspace/next/app/case-study/page.tsx`
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/app/layout.tsx`
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/app/page.tsx`
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/src/components/workspace-shell.tsx`
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/tests/e2e/realtime-collab.spec.ts`
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/tests/integration/realtime-collab-workspace.test.tsx`
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/tsconfig.json`
- `../study/frontend-portfolio/03-realtime-collab-workspace/package.json`

## starter code / 입력 계약

- `../study/frontend-portfolio/03-realtime-collab-workspace/next/app/case-study/page.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 외부 backend 없이 완결된 데모여야 한다.
- 브라우저 탭 두 개만으로 협업 시나리오를 재현할 수 있어야 한다.
- disconnect/reconnect, queued replay, 충돌 노출이 테스트 가능해야 한다.
- shared board cards
- shared doc blocks
- collaborator presence
- optimistic patch apply
- disconnected queue와 reconnect replay
- conflict banner와 activity log
- same-origin BroadcastChannel 기반 mock transport
- next/에 실행 가능한 협업 워크스페이스 구현
- patch/presence/conflict 경계를 설명하는 공개 문서와 발표 자료
- typecheck, unit/integration, E2E를 포함한 검증 체계

## 제외 범위

- 실제 auth/backend/persistence
- CRDT/OT 기반 텍스트 병합
- cursor presence, comment thread, fine-grained ACL

## 성공 체크리스트

- 핵심 흐름은 `metadata`와 `relativeTime`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `syncs board edits and presence across two pages`와 `replays queued patches after reconnect and surfaces conflicts`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/frontend-portfolio/03-realtime-collab-workspace/next/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `cd study && npm run verify --workspace @front-react/realtime-collab-workspace`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/realtime-collab-workspace
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/03-realtime-collab-workspace && npm run test -- --run
```

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/03-realtime-collab-workspace && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-realtime-collab-workspace_answer.md`](03-realtime-collab-workspace_answer.md)에서 확인한다.
