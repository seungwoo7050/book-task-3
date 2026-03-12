# React Native Implementation

Status: verified

이 앱은 기존 `incident-ops-mobile` 캡스톤을 대체하지 않고, 같은 도메인을 RN 채용 제출용 완성작으로 다시 구현한 최종 클라이언트다.

## Stack

- React Native CLI + TypeScript
- React Navigation
- TanStack Query
- AsyncStorage
- NetInfo
- React Hook Form + Zod

## Commands

```bash
npm install
npm run typecheck
npm test
npm run verify
```

## Manual Run

```bash
cd ../node-server
npm install
npm start
```

그 다음 새 터미널에서:

```bash
npm start -- --reset-cache
npx react-native run-ios --simulator "iPhone 16" --no-packager
npx react-native run-android
```

기본 server target은 `http://127.0.0.1:4100`이며 Settings 탭에서 바꿀 수 있다.
공유 HTTP/WS 계약은 `problem/code/contracts`를 로컬 package alias인 `@incident-ops/contracts`로 그대로 소비한다.

## Covered Behaviors

- auth stack with role selection
- incident feed with cursor pagination
- create form validation
- audit timeline
- persistent outbox with failed-state retry
- websocket replay cursor tracking

## Maestro

- `maestro/01-portfolio-core.yaml`
- `maestro/02-portfolio-outbox-recovery.yaml`
- `maestro/smoke-login-create.yaml`
- `maestro/approval-review.yaml`

```bash
export PATH="$PATH:$HOME/.maestro/bin"
maestro test maestro/01-portfolio-core.yaml --device "<simulator-udid>"
maestro test maestro/02-portfolio-outbox-recovery.yaml --device "<simulator-udid>"
```

저장소 공용 게이트는 JS/type/test이며, 디바이스 flow는 Maestro가 설치된 환경에서 추가로 돌린다.
