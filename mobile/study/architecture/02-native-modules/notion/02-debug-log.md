# 02 — Debug Log: 네이티브 모듈 디버깅 기록

## Issue 1: as const 없이 리터럴 타입이 사라지는 문제

### 증상

`MODULE_SPECS`를 `as const` 없이 선언했더니 `spec.name`의 타입이 `string`이었다.
특정 모듈 이름으로 분기하는 코드에서 string narrowing이 동작하지 않았다.

### 원인

TypeScript의 기본 타입 추론은 배열의 요소를 가장 넓은 타입으로 일반화한다.
`['getBatteryLevel', 'getChargingStatus']`는 `string[]`로 추론되고,
`name: 'BatteryModule'`은 `name: string`으로 추론된다.

### 해결

배열 끝에 `as const`를 추가했다:

```typescript
export const MODULE_SPECS = [
  { name: 'BatteryModule', methods: [...] },
  // ...
] as const;
```

이제 `MODULE_SPECS`는 `readonly` tuple이 되고 각 요소의 모든 값이 리터럴 타입이다.
`MODULE_SPECS[0].name`은 `'BatteryModule'` 타입이 된다.

### 교훈

상수 데이터를 타입 안전하게 사용하려면 `as const`가 필수다.
특히 codegen이나 코드 생성에 사용되는 spec 데이터는 리터럴 타입이 보장되어야
잘못된 문자열이 들어왔을 때 컴파일 타임에 잡을 수 있다.

---

## Issue 2: codegen-summary.mjs와 specs.ts의 데이터 동기화

### 증상

`specs.ts`에서 SensorModule에 `readMagnetometer` 메서드를 추가했는데,
`generated/modules.json`에는 methodCount가 여전히 4로 출력되었다.

### 원인

`codegen-summary.mjs`는 TypeScript 소스를 import하지 않고 같은 데이터를 수동으로 하드코딩한다.
Node.js mjs 스크립트에서 `.ts` 파일을 직접 import할 수 없기 때문이다.

### 해결

현재 구조에서는 수동 동기화를 유지하기로 했다.
대안으로 고려한 방법들:

1. **tsc로 specs.ts를 JS로 빌드 후 import** — 빌드 단계가 추가됨
2. **specs.json을 공유 데이터 소스로 사용** — TS에서 JSON import 후 타입 assertion 필요
3. **tsx (ts-node 대체) 사용** — devDependency 추가

이 프로젝트의 규모에서는 수동 동기화의 비용이 가장 낮다.
테스트에서 `buildGeneratedSummary()`를 검증하므로 TS 쪽의 정확성은 보장된다.

### 교훈

TS/JS 경계에서 데이터 동기화 문제는 bridge-vs-jsi 프로젝트에서도 동일하게 발생했다.
저장소 전체에서 반복되는 패턴이므로 공통 해결책(예: JSON 기반 공유 상수)을 고려할 만하다.

---

## Issue 3: 테스트에서 readonly 배열의 toEqual 비교

### 증상

`as const`로 선언된 `MODULE_SPECS`를 `toHaveLength(3)`으로 테스트하면 동작하지만,
`toEqual`로 정확한 값을 비교하려 하면 타입이 맞지 않는다는 에러가 발생했다.

### 원인

`as const`가 적용된 배열은 `readonly` 타입이다.
Jest의 `toEqual`은 `readonly`를 비교할 수 있지만,
기대값을 리터럴 객체로 쓰면 `readonly` vs 일반 배열의 타입 불일치가 발생할 수 있다.

### 해결

테스트에서는 `buildGeneratedSummary()`의 반환값을 비교하도록 변경했다.
`buildGeneratedSummary()`가 새 배열을 반환하므로 `readonly` 문제가 사라진다:

```typescript
expect(buildGeneratedSummary()).toEqual([
  { module: 'BatteryModule', methodCount: 3 },
  // ...
]);
```

### 교훈

`as const` 데이터를 직접 테스트하기보다 변환 함수의 출력을 테스트하는 것이 타입 호환성 문제를 피하는 방법이다.

---

## Issue 4: verify 순서에서 codegen이 먼저 실행되어야 하는 이유

### 증상

`npm run verify`의 순서를 `typecheck → test → codegen`으로 했더니,
`generated/modules.json`이 없는 상태에서도 typecheck와 test가 통과했다.
하지만 CI에서는 codegen 결과를 다른 단계의 입력으로 사용하는 경우가 있었다.

### 해결

verify 순서를 `codegen → typecheck → test`로 변경했다:

```json
"verify": "npm run codegen && npm run typecheck && npm test"
```

codegen이 먼저 실행되면:
1. `generated/modules.json`이 항상 최신 상태로 존재
2. typecheck가 codegen 결과를 참조하는 코드가 있어도 실패하지 않음
3. test가 codegen과 일치하는지 검증

### 교훈

빌드 파이프라인에서 "생성 → 검증 → 테스트" 순서는 기본 원칙이다.
생성 단계가 빠지면 이후 단계가 stale 데이터를 사용할 수 있다.
