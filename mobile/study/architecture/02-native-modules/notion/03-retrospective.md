# 03 — Retrospective: 네이티브 모듈 Spec 회고

## 무엇을 만들었나

Battery, Haptics, Sensor 세 가지 네이티브 모듈의 TypeScript spec을 정의하고,
codegen summary를 JSON으로 내보내고, consumer app에서 spec 데이터를 시각화하는 앱을 구현했다.
전체 verify 파이프라인(codegen → typecheck → test)을 구성했다.

## 잘된 점

### 1. as const로 spec의 불변성 보장

`MODULE_SPECS`에 `as const`를 적용해 모든 값을 리터럴 타입으로 고정한 것은 핵심적인 결정이었다.
spec 데이터는 런타임에 변경될 이유가 없으므로 `readonly`가 자연스럽다.
실수로 spec을 수정하려 하면 TypeScript가 컴파일 타임에 막아준다.

### 2. buildGeneratedSummary()가 spec에서 자동 파생

summary를 수동으로 작성하지 않고 `MODULE_SPECS.map()`으로 파생하는 것은
"spec과 summary가 항상 일치한다"는 보장을 제공한다.
모듈을 추가하거나 메서드를 바꿀 때 summary가 자동으로 따라온다.

### 3. 검증 순서의 명시성

`codegen → typecheck → test` 순서를 package.json의 verify 스크립트에 명시한 것은
"어떤 순서로 검증해야 하는가"를 코드로 문서화한 것이다.
새 팀원이 와도 `npm run verify`만 실행하면 된다.

## 아쉬운 점

### 1. 실제 native 코드가 없다

이 프로젝트는 spec의 "JS side"만 정의한다.
실제 TurboModule은 iOS(Objective-C++로 spec 구현)와 Android(Java/Kotlin으로 spec 구현)에
native 코드가 있어야 동작한다.
spec-first의 장점을 더 보여주려면 최소한 하나의 모듈에 대한 native 구현 예시가 있었으면 좋았다.

### 2. 메서드의 시그니처가 없다

현재 spec은 메서드 `이름`만 정의하고, `매개변수 타입`과 `반환 타입`은 정의하지 않는다.
실제 TurboModule spec은 `getBatteryLevel(): Promise<number>` 같은 전체 시그니처가 필요하다.
메서드 이름 목록만으로는 contract clarity가 부분적이다.

### 3. subscribe 패턴의 구조 미정의

BatteryModule의 `subscribe`는 이벤트 구독 패턴이다.
EventEmitter를 반환하는지, cleanup 함수를 반환하는지, 콜백을 받는지의 차이는
API의 사용성에 큰 영향을 미치는데 spec에 반영되어 있지 않다.

## 설계 판단 기록

### 왜 세 모듈인가?

세 모듈은 네이티브 모듈의 세 가지 대표적인 패턴을 보여주기 위해 선택했다:

1. **BatteryModule** — 조회(query) + 구독(subscription) 패턴
2. **HapticsModule** — fire-and-forget 명령(command) 패턴
3. **SensorModule** — 리소스 관리(start/stop) 패턴

이 세 패턴이 실무에서 만나는 대부분의 네이티브 모듈 유형을 커버한다.

### 왜 full native build가 아닌 summary export인가?

이 저장소의 CI 게이트는 JS/type/test 기반이다.
full native build는 Xcode와 Android SDK가 필요하고 CI 환경에서 무겁다.
JS 레벨의 codegen summary는 "spec이 올바른 구조인지"를 빠르게 검증하는 최소 게이트 역할을 한다.

### 왜 consumer app이 실제 native 호출을 하지 않는가?

consumer app의 목적은 "spec 데이터가 어떤 모습인지 시각적으로 확인"하는 것이다.
실제 native 호출은 네이티브 코드 구현이 선행되어야 하고,
그 구현은 이 프로젝트의 학습 범위("spec 정의와 codegen 파이프라인")을 벗어난다.

## TurboModule과의 관계

이 프로젝트의 spec은 TurboModule의 **설계 단계**에 해당한다.
실제 TurboModule 구현 파이프라인은 다음과 같다:

```
1. TypeScript spec 정의 (이 프로젝트가 여기)
2. npx react-native codegen 실행
3. iOS: generated protocol을 Objective-C++로 구현
4. Android: generated interface를 Java/Kotlin으로 구현
5. JS에서 TurboModuleRegistry.getEnforcing()으로 사용
```

## 다음 단계에서 시도할 것

1. **메서드 시그니처 추가**: `getBatteryLevel(): Promise<number>` 같은 전체 타입 정의
2. **실제 codegen 실행**: `npx react-native codegen`으로 native interface 생성 확인
3. **하나의 모듈 native 구현**: BatteryModule의 iOS/Android native 코드 작성
4. **EventEmitter 통합**: subscribe 패턴의 구체적 구현 (RCTEventEmitter 활용)
