# Testing Pyramid And Demo Checklist

## Repository Gate

- `npm run typecheck`
- `npm test`
- `npm run verify`
- `npm test` in `node-server`
- `npm run demo-e2e` in `node-server`

## App Test Focus

- 세션/설정 복구
- outbox retry와 DLQ 상태 전이
- form validation
- 로그인 후 incident feed 진입

## Manual Demo Checklist

- reporter로 로그인 후 incident 생성
- operator로 ack와 request-resolution 처리
- approver로 approve/reject 분기 확인
- 오프라인 상태에서 mutation queue 적재 후 reconnect flush
- websocket replay로 missed event 복구 확인
- outbox failed 항목 수동 retry 확인
