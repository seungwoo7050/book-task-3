# 문제 정의

프로비넌스: `authored`

## 문제

`Realtime Collab Workspace`는 협업 보드와 문서 편집기를 같은 화면 안에 놓고, "동기화가 보이는 제품"을 만드는 capstone이다. 핵심은 단순한 라이브 업데이트가 아니라, local optimistic patch, collaborator presence, reconnect replay, conflict banner를 어디까지 노출해야 사용자가 현재 상태를 이해할 수 있는가에 있다.

## 제공 자산

- 이 문서: 제품 정의와 서비스 경계
- `data/`: 추가 fixture 없이 로컬 mock state를 유지하기 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder

## 제약

- 외부 backend 없이 완결된 데모여야 한다.
- 브라우저 탭 두 개만으로 협업 시나리오를 재현할 수 있어야 한다.
- disconnect/reconnect, queued replay, 충돌 노출이 테스트 가능해야 한다.

## 포함 범위

- shared board cards
- shared doc blocks
- collaborator presence
- optimistic patch apply
- disconnected queue와 reconnect replay
- conflict banner와 activity log
- same-origin `BroadcastChannel` 기반 mock transport

## 제외 범위

- 실제 auth/backend/persistence
- CRDT/OT 기반 텍스트 병합
- cursor presence, comment thread, fine-grained ACL
- cross-device sync와 durable offline cache

## 요구 산출물

- `next/`에 실행 가능한 협업 워크스페이스 구현
- patch/presence/conflict 경계를 설명하는 공개 문서와 발표 자료
- `typecheck`, unit/integration, E2E를 포함한 검증 체계

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/realtime-collab-workspace
```

- `typecheck`: Next.js 앱 타입 검사
- `vitest`: workspace state, transport orchestration, integration 흐름 확인
- `playwright`: 멀티탭 동기화, reconnect replay, conflict banner 확인
