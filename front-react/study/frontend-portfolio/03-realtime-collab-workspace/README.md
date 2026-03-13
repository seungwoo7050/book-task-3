# 03 Realtime Collab Workspace

상태: `verified`

## 무슨 문제인가

실시간 협업 앱은 "두 탭에서 값이 같이 바뀐다"만으로는 충분하지 않다. presence, optimistic patch, reconnect replay, conflict surface를 어디까지 드러낼지까지 함께 설계해야 제품처럼 읽힌다. 이 프로젝트는 외부 backend 없이도 그 판단을 설명 가능한 프론트 capstone으로 만드는 문제를 푼다.

## 왜 필요한가

`01-ops-triage-console`이 내부도구형 밀도와 optimistic mutation을, `02-client-onboarding-portal`이 고객-facing route/form 흐름을 보여 줬다면, 이 프로젝트는 그 다음 단계인 multi-user mental model을 채운다. 같은 포트폴리오 트랙 안에서도 "혼자 쓰는 앱"과 "같이 쓰는 앱"의 설계 긴장을 분리해 보여 주는 역할이다.

## 내가 만든 답

shared board cards, shared doc blocks, collaborator presence, optimistic patch apply, reconnect replay, conflict banner, activity log를 갖춘 Next.js 협업 워크스페이스를 구현했다. transport는 실제 서버 대신 same-origin `BroadcastChannel`을 사용해 협업 감각을 재현하고, 테스트에서는 `MemoryCollabTransport`로 deterministic하게 검증한다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [next/README.md](next/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `next/src/components/workspace-shell.tsx`에서 board, doc, presence, activity, conflict surface를 하나의 product shell로 묶는다.
- `next/src/hooks/use-realtime-workspace.ts`에서 local optimistic patch, transport event, reconnect replay를 한 state machine처럼 조율한다.
- `next/src/lib/workspace-state.ts`, `transport.ts`, `storage.ts`에서 patch envelope, conflict window, mock transport, viewer identity를 분리한다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/realtime-collab-workspace
npm run verify --workspace @front-react/realtime-collab-workspace
```

- 검증 기준일: 2026-03-13
- `typecheck`: `next/tsconfig.json` 기준 타입 검사 통과
- `vitest`: optimistic patch merge, presence update, queued replay, conflict banner integration 확인
- `playwright`: 두 탭 간 동기화, offline queue 후 reconnect replay, conflict banner 노출 확인

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [next/README.md](next/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 실제 backend, auth, durable persistence, CRDT/OT 엔진은 포함하지 않는다.
- same-origin 브라우저 탭 기준 mock collaboration만 다룬다.
- production-grade offline merge, cursor presence, 권한 모델은 후속 확장으로 남긴다.
