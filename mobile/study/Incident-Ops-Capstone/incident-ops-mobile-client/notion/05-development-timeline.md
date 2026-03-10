# 05 — Development Timeline: Incident Ops Mobile Client 개발 타임라인

> 소스코드만으로는 알 수 없는 CLI 명령어, 설치 과정, 도구 사용 이력을 기록한다.

## Step 1: 프로젝트 초기화

```bash
npx @react-native-community/cli init IncidentOpsMobileClient --template @react-native-community/template
cd IncidentOpsMobileClient
```

React Native 0.84.1 기반. incident-ops-mobile(harness)과 별도의 react-native 디렉토리다.

## Step 2: contracts 패키지 연결

```bash
npm install ../problem/code/contracts
```

harness와 동일한 contracts 패키지를 `file:` 프로토콜로 공유.
→ `node_modules/@incident-ops/contracts` 심볼릭 링크 생성.

```bash
ls -la node_modules/@incident-ops/contracts
# -> ../../problem/code/contracts
```

## Step 3: 핵심 의존성 설치

### 폼 + 검증

```bash
npm install react-hook-form @hookform/resolvers zod
```

### 서버 상태 캐시

```bash
npm install @tanstack/react-query
```

### 네비게이션

```bash
npm install @react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context react-native-gesture-handler
```

### 영속화 + 네트워크

```bash
npm install @react-native-async-storage/async-storage @react-native-community/netinfo
```

### iOS 네이티브 연동

```bash
cd ios && pod install && cd ..
```

react-native-screens, AsyncStorage, NetInfo 등의 네이티브 모듈이 CocoaPods으로 링크된다.

## Step 4: 서버 설정과 시작

```bash
cd node-server
npm install
npm start
# 서버가 http://127.0.0.1:4100 에서 시작
```

클라이언트의 `DEFAULT_BASE_URL`이 `http://127.0.0.1:4100`이므로
서버를 먼저 시작한 후 앱을 실행해야 한다.

### 서버 테스트

```bash
cd node-server
npm test
```

## Step 5: Metro 번들러 설정

```bash
# contracts 심볼릭 링크 해석을 위해 캐시 초기화 필요할 수 있음
npx react-native start --reset-cache
```

metro.config.js에서 contracts 경로가 번들에 포함되는지 확인.
`Unable to resolve module '@incident-ops/contracts'` 에러가 나면:

```bash
watchman watch-del-all
npx react-native start --reset-cache
```

## Step 6: 앱 실행

### iOS 시뮬레이터

```bash
npx react-native run-ios --simulator "iPhone 16"
```

### Android 에뮬레이터

```bash
npx react-native run-android
```

서버가 로컬에서 실행 중이므로 Android에서는 포트 포워딩이 필요:

```bash
adb reverse tcp:4100 tcp:4100
```

## Step 7: 테스트 실행

```bash
# 전체 테스트
npm test

# 타입 체크
npm run typecheck

# 검증 (typecheck + test)
npm run verify
```

### Makefile로 전체 파이프라인

```bash
cd problem
make app-build    # tsc --noEmit
make app-test     # jest
make server-test  # node-server npm test
make demo-e2e     # server demo-e2e + maestro (선택)
```

## Step 8: Maestro e2e 설정

### Maestro 설치

```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
export PATH="$PATH:$HOME/.maestro/bin"
maestro --version
# Maestro 2.2.0
```

### e2e 플로우 실행

```bash
# 시뮬레이터 UDID 확인
xcrun simctl list devices booted

# 핵심 플로우
maestro test maestro/01-portfolio-core.yaml --device "<simulator-udid>"

# 장애 복구 플로우
maestro test maestro/02-portfolio-outbox-recovery.yaml --device "<simulator-udid>"
```

### 스크린샷 캡처 (포트폴리오용)

```bash
maestro test maestro/01-portfolio-core.yaml \
  --device "<simulator-udid>" \
  --test-output-dir ../docs/assets/portfolio

maestro test maestro/02-portfolio-outbox-recovery.yaml \
  --device "<simulator-udid>" \
  --test-output-dir ../docs/assets/portfolio
```

캡처된 스크린샷이 `docs/assets/portfolio/screenshots/`에 저장된다.
portfolio-presentation.md에서 이 이미지들을 참조한다.

## Step 9: 포트폴리오 데모 재현 전체 순서

```bash
# 터미널 1: 서버
cd study/Incident-Ops-Capstone/incident-ops-mobile-client/node-server
npm install
npm start

# 터미널 2: 번들러
cd study/Incident-Ops-Capstone/incident-ops-mobile-client/react-native
npm install
npm start -- --reset-cache

# 터미널 3: 시뮬레이터
npx react-native run-ios --simulator "iPhone 16" --no-packager

# 터미널 4: Maestro (선택)
maestro test maestro/01-portfolio-core.yaml
maestro test maestro/02-portfolio-outbox-recovery.yaml
```

## 도구 요약

| 도구 | 용도 | 명령어 |
|------|------|--------|
| npm | 패키지 관리 | `npm install`, `npm test` |
| TypeScript | 타입 체크 | `npm run typecheck` (tsc --noEmit) |
| Jest | 단위/통합 테스트 | `npm test` |
| Make | 빌드/테스트 통합 | `make app-build`, `make app-test` |
| CocoaPods | iOS 네이티브 의존성 | `cd ios && pod install` |
| Metro | JS 번들러 | `npx react-native start --reset-cache` |
| React Native CLI | 앱 실행 | `npx react-native run-ios` |
| Maestro | e2e 자동화 | `maestro test maestro/*.yaml` |
| watchman | 파일 감시 (metro 의존) | `watchman watch-del-all` |
| adb | Android 포트 포워딩 | `adb reverse tcp:4100 tcp:4100` |
| xcrun simctl | 시뮬레이터 관리 | `xcrun simctl list devices booted` |

## 특이사항

### contracts 변경 반영

contracts 파일을 수정하면 metro 캐시 때문에 변경이 즉시 보이지 않을 수 있다.

```bash
npx react-native start --reset-cache
```

### node-server demo-e2e

```bash
cd node-server
npm run demo-e2e
```

이 명령은 서버를 실행하고 자동화 시나리오를 수행한 후 결과를 `demo/` 디렉토리에 JSON으로 저장한다.
`audit-log.json`, `e2e-summary.json`, `structured-logs.json`이 생성된다.

### 오프라인 테스트

시뮬레이터의 네트워크를 끄거나, SettingsScreen에서 잘못된 base URL을 입력하면
오프라인 시나리오를 재현할 수 있다.
mutation이 outbox에 쌓이고, 복구 후 flush 시 서버에 반영되는 것을 확인한다.
