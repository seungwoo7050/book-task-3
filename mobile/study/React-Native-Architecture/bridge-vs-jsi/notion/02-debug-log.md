# 02 — Debug Log: Bridge vs JSI 디버깅 기록

## Issue 1: toFixed()가 문자열을 반환하는 타입 문제

### 증상

`computeStats()`에서 `mean.toFixed(2)`를 반환했더니 TypeScript가 `string` 타입이라고 에러를 냈다.
`BenchmarkStats.mean`은 `number` 타입으로 선언되어 있었다.

### 원인

JavaScript의 `toFixed()` 메서드는 숫자가 아닌 **문자열**을 반환한다.
이것은 JavaScript의 오래된 설계 결함 중 하나다.

### 해결

`Number(value.toFixed(2))`로 감싸서 다시 숫자 타입으로 변환했다:

```typescript
mean: Number(mean.toFixed(2)),
stddev: Number(Math.sqrt(variance).toFixed(2)),
```

### 교훈

`toFixed()`는 반올림+포매팅이 아니라 "문자열 포매팅"이다.
숫자 연산에 다시 사용하려면 항상 `Number()`나 `parseFloat()`로 감싸야 한다.

---

## Issue 2: Export 스크립트와 TypeScript 소스의 데이터 동기화

### 증상

`benchmark.ts`의 `RUNS` 데이터를 수정했는데 `export-results.mjs`의 결과값은 이전 그대로였다.
CI에서 생성된 JSON 파일이 앱에 표시되는 수치와 달랐다.

### 원인

`export-results.mjs`는 `benchmark.ts`를 import하지 않고 같은 값을 수동으로 하드코딩한다.
Node.js 스크립트에서 TypeScript 소스를 직접 import할 수 없기 때문이다.

### 해결

두 가지 방법을 고려했다:

1. **ts-node 사용**: `npx ts-node scripts/export-results.ts`로 TypeScript를 직접 실행. 의존성이 추가되는 단점.
2. **값 수동 동기화**: 현재 방식을 유지하되, `RUNS` 값을 바꿀 때 mjs도 함께 수정.

이 프로젝트에서는 2번(수동 동기화)을 선택했다.
CI 실행은 JS 소스에서 실행되고, 테스트가 `buildExport()`를 검증하므로
TS 쪽의 정확성은 보장된다. mjs는 외부 공유용 부가 산출물이다.

### 교훈

TS와 mjs 사이의 데이터 동기화 문제는 반복되는 패턴이다.
JSON 파일을 공유 데이터 소스로 두고 양쪽이 읽는 방법도 있지만,
프로젝트 규모에 따라 수동 동기화가 더 간결할 수 있다.

---

## Issue 3: 표준편차가 0이 되는 경우의 처리

### 증상

테스트 중 모든 sample이 동일한 값([10, 10, 10, 10, 10])인 run을 만들었더니 stddev가 0이 나왔다.
`mean > stddev` assertion이 `10 > 0`으로 통과하지만, 의미상 "표준편차 0"이 허용될지 고민이 생겼다.

### 분석

stddev가 0인 것은 수학적으로 정확하다. 모든 측정값이 동일하면 편차가 없다.
하지만 실제 벤치마크에서 5회 측정이 정확히 같은 값을 가지는 것은 비현실적이다.
이는 테스트용 인위적 데이터에서만 발생하는 경계 조건이다.

### 결정

stddev = 0을 유효한 결과로 허용했다.
통계 함수는 입력에 대해 수학적으로 정확한 결과를 반환하면 되고,
"현실적인 측정값인가?"를 판단하는 것은 통계 함수의 책임이 아니다.

### 교훈

순수 함수는 입력의 "타당성"을 판단하지 않는다. 주어진 입력에 대해 정확한 출력만 보장한다.
입력 검증은 함수를 호출하는 쪽의 책임이다.

---

## Issue 4: generatedAt 날짜의 결정성

### 증상

처음에 `new Date().toISOString().split('T')[0]`을 사용했더니 테스트에서 `toEqual`이 실패했다.
어제 실행하면 통과하고 오늘 실행하면 실패하는 flaky test가 되었다.

### 해결

`generatedAt`을 `'2026-03-08'` 고정 문자열로 변경했다.
결정적(deterministic) 출력을 보장해야 `toEqual`로 정확한 비교가 가능하다.

```typescript
export function buildExport() {
  return {
    generatedAt: '2026-03-08',
    results: RUNS.map(computeStats),
  };
}
```

### 교훈

"현재 시간"을 포함하는 함수는 결정적이지 않다.
테스트에서 결정성이 필요하면 시간을 외부에서 주입받거나 고정값을 사용해야 한다.
