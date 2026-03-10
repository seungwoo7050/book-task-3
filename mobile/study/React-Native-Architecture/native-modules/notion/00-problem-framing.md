# 00 — Problem Framing: 네이티브 모듈 Spec 설계

## 문제의 출발점

React Native 앱이 배터리 잔량을 읽거나, 진동 피드백을 주거나, 센서 데이터를 수집하려면
JavaScript가 직접 할 수 없는 플랫폼 API에 접근해야 한다.
이 접근을 제공하는 것이 Native Module이다.

React Native 0.84의 New Architecture에서 Native Module은 TurboModule로 구현된다.
TurboModule의 핵심은 **TypeScript spec이 코드 생성(codegen)의 입력**이 된다는 것이다.
spec을 정의하면 iOS(Objective-C++)와 Android(Java/Kotlin) 쪽의 인터페이스 코드가 자동으로 생성된다.

이 프로젝트의 질문은:
**Battery, Haptics, Sensor 세 가지 네이티브 모듈의 public spec을 TypeScript로 고정하고, 
그 spec에서 codegen summary와 consumer app을 만들면 어떤 구조가 되는가?**

## 왜 spec-first가 중요한가

1. **Contract clarity** — spec이 먼저 정의되면 JS와 Native 양쪽 개발자가 같은 인터페이스를 보고 작업한다. "이 메서드가 무엇을 반환하는지" 논쟁이 없어진다.

2. **Codegen 가능성** — TurboModule codegen은 TypeScript spec에서 native 인터페이스를 생성한다. spec이 부정확하면 codegen 결과도 틀리다. spec의 정확성이 전체 시스템의 정확성을 결정한다.

3. **Platform parity** — 하나의 TypeScript spec에서 iOS와 Android 인터페이스가 모두 생성되므로, 양 플랫폼이 동일한 API surface를 가진다.

## 설계 방향

### 세 가지 모듈

| 모듈 | 메서드 | 역할 |
|------|--------|------|
| BatteryModule | getBatteryLevel, getChargingStatus, subscribe | 배터리 잔량 읽기, 충전 상태, 변화 구독 |
| HapticsModule | vibrate, impactFeedback, notificationFeedback | 진동 종류별 피드백 |
| SensorModule | startAccelerometer, stopAccelerometer, startGyroscope, stopGyroscope | 가속도/자이로스코프 센서 시작/중지 |

### Spec 구조

`MODULE_SPECS`는 `as const`로 선언된 배열이다.
각 요소는 `{ name: string, methods: string[] }` shape을 가지며,
`as const`가 리터럴 타입을 보존해 `MODULE_SPECS[0].name`이 `'BatteryModule'` 타입이 된다.

### Codegen Summary

`buildGeneratedSummary()` 함수가 각 모듈의 이름과 메서드 수를 요약한다.
`scripts/codegen-summary.mjs`가 이 요약을 `generated/modules.json`으로 저장한다.

이 접근이 의미 있는 이유:
실제 React Native codegen은 `npx react-native codegen`으로 실행하며 native 빌드 아티팩트를 생성한다.
하지만 CI에서 full native build 없이 "모듈 구조가 올바른지"를 빠르게 검증하려면
JS 레벨의 summary가 필요하다. 이것이 contract clarity를 위한 최소 게이트다.

## 학습 범위

| 영역 | 구체적 목표 |
|------|-------------|
| Spec 정의 | TypeScript로 모듈 이름과 메서드 목록 고정 |
| Codegen | summary export로 spec → artifact 파이프라인 이해 |
| Consumer | spec 데이터를 UI에 표시하는 consumer app |
| Platform | JS/Native 경계의 계약 구조 이해 |
