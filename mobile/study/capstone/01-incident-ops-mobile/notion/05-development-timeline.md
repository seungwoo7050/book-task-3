# 05 — Development Timeline: Contract Harness 개발 타임라인

> 소스코드만으로는 알 수 없는 CLI 명령어, 설치 과정, 도구 사용 이력을 기록한다.

## Step 1: 프로젝트 초기화

```bash
npx @react-native-community/cli init IncidentOpsHarness --template @react-native-community/template
cd IncidentOpsHarness
```

React Native 0.84.1 기반 프로젝트 생성.
capstone은 최상위 폴더에서 하위 두 프로젝트(harness, client)를 관리하므로
`react-native/` 디렉토리에 RN 프로젝트를 배치했다.

## Step 2: contracts 패키지 생성

```bash
mkdir -p problem/code/contracts
cd problem/code/contracts
npm init -y
```

`contracts.ts`를 작성하고, `package.json`의 main을 설정한다.
이 패키지가 서버와 클라이언트의 공유 지점이다.

## Step 3: file: 프로토콜로 contracts 연결

```bash
cd react-native
npm install ../problem/code/contracts
```

설치 후 `package.json`에 `"@incident-ops/contracts": "file:../problem/code/contracts"`가 추가된다.
`node_modules/@incident-ops/contracts/`에 심볼릭 링크가 생성된다.

### 확인

```bash
ls -la node_modules/@incident-ops/contracts
# -> ../../problem/code/contracts 심볼릭 링크 확인
```

## Step 4: TypeScript 설정

```bash
npx tsc --init
```

`tsconfig.json`에서 `strict: true`, `jsx: "react-jsx"` 등을 설정.
contracts 패키지의 타입이 정상적으로 resolve되는지 확인:

```bash
npx tsc --noEmit
```

## Step 5: 테스트 환경 구성

```bash
npm install --save-dev jest @types/jest ts-jest @testing-library/react-native @testing-library/jest-native
```

`jest.config.js`에서 `preset: 'react-native'`과 `transformIgnorePatterns` 설정.
`@incident-ops/contracts`가 심볼릭 링크이므로 transform 대상에 포함되는지 확인 필요.

```bash
npx jest --verbose
```

## Step 6: harnessModel.ts 개발

순수 함수 개발은 별도의 도구가 필요 없다.
코드 에디터에서 작성 → `npx tsc --noEmit`으로 타입 확인 → `npx jest`로 테스트.

```bash
# 타입 체크
npx tsc --noEmit

# 단일 파일 테스트
npx jest tests/incident-ops-harness.test.tsx --verbose
```

## Step 7: Makefile 설정

```bash
# 최초 실행으로 모든 타겟 확인
make test
```

Makefile의 각 타겟이 올바르게 작동하는지 확인:

```bash
make app-build    # tsc --noEmit
make app-test     # jest
make server-test  # node-server npm test
make demo-e2e     # demo run-e2e.mjs
```

## Step 8: iOS 시뮬레이터 실행 (선택)

```bash
cd ios && pod install && cd ..
npx react-native run-ios
```

harness UI를 시뮬레이터에서 확인.
역할 선택 → 버튼 → 상태 전이가 화면에 표시되는지 수동 검증.

## 도구 요약

| 도구 | 용도 | 명령어 |
|------|------|--------|
| npm | 패키지 관리, file: 프로토콜 | `npm install ../problem/code/contracts` |
| TypeScript | 타입 체크 | `npx tsc --noEmit` |
| Jest | 테스트 실행 | `npx jest --verbose` |
| Make | 빌드/테스트 통합 | `make test`, `make app-build` |
| CocoaPods | iOS 네이티브 의존성 | `cd ios && pod install` |
| React Native CLI | 앱 실행 | `npx react-native run-ios` |

## 특이사항

### contracts 변경 후 반영

contracts 코드를 수정한 후에는 `npm install`을 다시 해야 할 수 있다.
file: 프로토콜은 심볼릭 링크이므로 보통은 즉시 반영되지만,
TypeScript 캐시나 metro 번들러 캐시가 남아 있으면 변경이 보이지 않는다.

```bash
# metro 캐시 클리어
npx react-native start --reset-cache

# watchman 캐시 클리어
watchman watch-del-all
```

### node-server 실행 (client와 연동 시)

```bash
cd node-server
npm install
npm start
# 기본 포트: 3000
```

harness 자체는 서버가 필요 없지만,
incident-ops-mobile-client와 통합 테스트 시에는 node-server를 실행해야 한다.
