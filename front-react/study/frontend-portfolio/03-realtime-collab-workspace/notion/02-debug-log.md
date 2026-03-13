# 디버그 기록 — Realtime Collab Workspace

## mount effect가 반복 실행되던 문제

`useEffectEvent`로 만든 transport handler를 effect dependency에 넣어 둔 상태에서 mount effect가 다시 돌고 있었다. 결과적으로 테스트는 멈추고, E2E에서는 disconnect 직후 상태가 다시 `Connected`로 돌아갔다. dependency에서 effect event를 제거해 transport 구독이 한 번만 잡히게 수정했다.

## copied onboarding 파일이 타입체크를 깨던 문제

초기 scaffold를 복사해 온 뒤 기존 onboarding 컴포넌트와 query provider 파일이 남아 있었다. 새 프로젝트에서는 쓰지 않지만 `tsc --noEmit`이 전부 읽기 때문에 모듈 누락 에러가 났다. 남은 복제 잔재를 삭제해 실제 표면만 남겼다.

## Next route announcer와 alert selector 충돌

Playwright에서 `getByRole("alert")`를 쓰니 Next의 route announcer와 conflict banner가 같이 잡혔다. banner에 전용 `data-testid="conflict-banner"`를 추가해 E2E selector를 분리했다.
