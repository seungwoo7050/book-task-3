# Node Server Implementation

Status: verified

## Problem Scope Covered

최종 RN 클라이언트가 소비하는 로컬 API, realtime, audit backend 구현을 보관한다.

## Build Command

```bash
cd study/capstone/02-incident-ops-mobile-client/node-server
npm install
npm start
```

## Test Command

```bash
cd study/capstone/02-incident-ops-mobile-client/node-server
npm test
```

## Known Gaps

- 서버는 기존 캡스톤 구현을 그대로 재사용하므로, 모바일 UX 요구를 위해 필요한 API는 현재 계약 범위 안에서만 사용한다.

## Implementation Notes

- 이 구현은 기존 `incident-ops-mobile` study 프로젝트에서 복사해 왔다.
- 공통 계약은 `problem/code/contracts`를 기준으로 유지한다.
- 수동 앱 확인이 필요할 때는 `npm start`로 고정 포트 서버를 띄울 수 있다.
