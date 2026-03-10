# 01 — Approach Log: 네이티브 모듈 구현 과정

## Phase 1: Module Spec 정의 — specs.ts

첫 번째로 만든 것은 세 모듈의 spec 상수다.

```typescript
export const MODULE_SPECS = [
  { name: 'BatteryModule', methods: ['getBatteryLevel', 'getChargingStatus', 'subscribe'] },
  { name: 'HapticsModule', methods: ['vibrate', 'impactFeedback', 'notificationFeedback'] },
  { name: 'SensorModule', methods: ['startAccelerometer', 'stopAccelerometer', 'startGyroscope', 'stopGyroscope'] },
] as const;
```

`as const`의 역할이 핵심이다.
이 assertion이 없으면 `MODULE_SPECS`는 `{ name: string; methods: string[] }[]` 타입이 되지만,
`as const`가 있으면 각 요소의 name과 methods가 리터럴 타입으로 고정된다.
`MODULE_SPECS[0].name`의 타입이 `string`이 아니라 `'BatteryModule'`이 된다.

이 차이가 실무에서 중요한 이유:
TurboModule codegen은 spec의 정확한 문자열을 기반으로 native 코드를 생성한다.
타입이 느슨하면 "존재하지 않는 모듈 이름"을 넣어도 컴파일 에러가 나지 않는다.

### 각 모듈의 메서드 설계 의도

**BatteryModule** — 세 가지 패턴을 보여준다:
- `getBatteryLevel`: 단발 조회 (Promise 반환 가능)
- `getChargingStatus`: 단발 조회 (동기 또는 비동기)
- `subscribe`: 이벤트 구독 (EventEmitter 패턴)

**HapticsModule** — fire-and-forget 패턴:
- `vibrate`, `impactFeedback`, `notificationFeedback`: 모두 반환값 없이 native 동작만 트리거

**SensorModule** — start/stop 페어 패턴:
- `startAccelerometer`/`stopAccelerometer`: 가속도 센서 제어
- `startGyroscope`/`stopGyroscope`: 자이로스코프 제어
- 리소스 관리가 필수이므로 반드시 stop을 호출해야 한다

## Phase 2: Codegen Summary 함수 — buildGeneratedSummary

`buildGeneratedSummary()` 함수는 각 모듈의 이름과 메서드 수를 요약한 배열을 반환한다:

```typescript
[
  { module: 'BatteryModule', methodCount: 3 },
  { module: 'HapticsModule', methodCount: 3 },
  { module: 'SensorModule', methodCount: 4 },
]
```

이 함수는 `MODULE_SPECS.map()`으로 구현되어 spec 상수에 모듈을 추가하면 summary도 자동으로 확장된다.
수동으로 summary를 관리하는 것과 달리 spec과 summary가 항상 동기화된다.

## Phase 3: Consumer App — NativeModulesStudyApp.tsx

앱은 단일 화면으로 `MODULE_SPECS`를 순회하며 카드를 렌더링한다.
각 카드에는 모듈 이름과 메서드 목록이 `·`로 구분되어 표시된다.

```
BatteryModule
getBatteryLevel · getChargingStatus · subscribe

HapticsModule
vibrate · impactFeedback · notificationFeedback

SensorModule
startAccelerometer · stopAccelerometer · startGyroscope · stopGyroscope
```

consumer app이 실제 native 호출을 하지 않는 것은 의도적이다.
이 프로젝트의 초점은 "모듈의 public surface가 올바른지"를 시각적으로 확인하는 것이다.
실제 native 구현은 iOS/Android 각각의 네이티브 코드 작업이 필요하며,
이 프로젝트의 scope 밖이다.

## Phase 4: Codegen Export 스크립트

`scripts/codegen-summary.mjs`는 Node.js 스크립트로 `generated/modules.json`을 생성한다:

```json
[
  { "module": "BatteryModule", "methodCount": 3 },
  { "module": "HapticsModule", "methodCount": 3 },
  { "module": "SensorModule", "methodCount": 4 }
]
```

`npm run codegen` 또는 `make codegen`으로 실행한다.
verify 파이프라인(`npm run verify`)에서는 codegen이 가장 먼저 실행된다:
`codegen → typecheck → test` 순서다.

## 테스트 구조

`native-modules.test.tsx`는 두 개의 테스트를 가진다:

1. **Spec 구조 검증**: `MODULE_SPECS`가 정확히 3개 모듈을 가지고, 첫 번째 모듈의 methods가 1개 이상인지 확인.

2. **Codegen summary 검증**: `buildGeneratedSummary()`가 모듈 이름과 정확한 methodCount를 반환하는지 `toEqual`로 확인. 이 테스트가 통과하면 "spec에서 summary를 정확하게 추출하는 로직"이 검증된 것이다.
