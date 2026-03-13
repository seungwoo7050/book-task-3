# Quality Bar

## Command

```bash
cd study
npm run verify --workspace @front-react/realtime-collab-workspace
```

## What Is Verified

- unit
  - optimistic patch merge
  - queued replay
  - conflict banner state
- integration
  - local optimistic update 후 remote overwrite 반영
  - presence 반영과 activity log 노출
- E2E
  - 두 탭 간 동기화
  - disconnect 후 reconnect replay
  - 충돌 배너 노출

## Notes

- transport와 persistence는 mock boundary다.
- 이 품질 기준의 목표는 sync UX와 상태 설명 가능성을 보여 주는 것이지 production backend correctness를 주장하는 것이 아니다.
