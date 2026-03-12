# 01 — Approach Log: Bridge vs JSI 구현 과정

## Phase 1: 벤치마크 데이터 모델 — benchmark.ts

가장 먼저 정의한 것은 벤치마크 데이터의 shape이다.

`BenchmarkRun`은 세 필드를 가진다:
- `label`: 호출 surface 이름 ("async serialized" 또는 "sync direct-call")
- `payloadSize`: 전송하는 데이터 크기 (양쪽 동일하게 1000)
- `samples`: 5회 측정값 배열 (밀리초 단위)

`RUNS` 배열에 두 개의 run을 하드코딩했다:

```typescript
const RUNS: BenchmarkRun[] = [
  { label: 'async serialized', payloadSize: 1000, samples: [42, 45, 44, 47, 43] },
  { label: 'sync direct-call', payloadSize: 1000, samples: [11, 10, 12, 10, 11] },
];
```

왜 하드코딩인가?
이 저장소의 CI 게이트는 JS/type/test 기반이다.
실제 native module 호출로 측정하려면 디바이스가 필요하고, CI에서 재현이 불가능하다.
대신 대표적인 측정값을 고정해 "통계 계산 로직의 정확성"을 검증하는 데 집중한다.

## Phase 2: 통계 함수 — computeStats

`computeStats(run)` 함수는 평균과 표준편차를 계산한다.

평균은 `samples.reduce(...) / length`로 구하고,
분산은 `samples.reduce((sum, v) => sum + (v - mean)², 0) / length`로 계산한 뒤
제곱근을 씌워 표준편차를 얻는다.

결과를 `toFixed(2)`로 소수점 둘째 자리까지 반올림해 `Number()`로 다시 숫자 타입으로 변환한다.
이 단계가 없으면 문자열이 반환되어 타입 에러가 발생한다.

계산 결과:

| Surface | Mean | Stddev |
|---------|------|--------|
| async serialized | 44.2ms | 1.72ms |
| sync direct-call | 10.8ms | 0.75ms |

sync direct-call이 async보다 약 4배 빠르다.
표준편차도 낮아 측정 결과가 더 안정적이다.

## Phase 3: Export 함수 — buildExport

`buildExport()` 함수는 모든 run에 대해 `computeStats()`를 적용하고,
`generatedAt` 날짜와 함께 객체를 반환한다:

```typescript
{
  generatedAt: '2026-03-08',
  results: [
    { label: 'async serialized', payloadSize: 1000, mean: 44.2, stddev: 1.72 },
    { label: 'sync direct-call', payloadSize: 1000, mean: 10.8, stddev: 0.75 },
  ]
}
```

`generatedAt`이 고정 문자열인 이유는 테스트에서 `toEqual`로 정확한 비교를 하기 위해서다.
`new Date().toISOString()`을 사용하면 실행 시점마다 값이 달라져 snapshot이 필요해진다.

## Phase 4: UI 대시보드 — BridgeVsJsiStudyApp.tsx

앱은 단일 화면으로 구성된다.
`RUNS.map(computeStats)`로 각 surface의 통계를 계산하고,
카드 형태로 label, payloadSize, mean, stddev를 나란히 보여준다.

UI가 의도적으로 간결한 이유는 이 프로젝트의 핵심이 "시각적 앱 구현"이 아니라 "벤치마크 로직과 결과 해석"이기 때문이다.
두 카드를 나란히 놓으면 async vs sync의 차이가 직관적으로 보인다.

## Phase 5: Export 스크립트 — export-results.mjs

`scripts/export-results.mjs`는 Node.js 스크립트로 `exports/benchmark-results.json`을 생성한다.
`npm run export-results`나 CI에서 실행할 수 있다.

스크립트의 결과값은 `benchmark.ts`의 `buildExport()`와 동일한 데이터를 담는다.
TypeScript 소스를 직접 import할 수 없으므로 같은 값을 스크립트에 다시 작성했다.

## 테스트 구조

`bridge-vs-jsi.test.tsx`는 두 개의 테스트를 가진다:

1. **통계 계산 검증**: `computeStats(RUNS[0])`의 mean이 stddev보다 큰지 확인. 이것은 "측정값이 노이즈보다 유의미하게 큰가?"를 검증하는 sanity check다.

2. **Export 결정성 검증**: `buildExport()`의 결과가 `RUNS.map(computeStats)`를 포함하는 정확한 객체인지 `toEqual`로 비교. generatedAt 날짜까지 포함해서 완전한 일치를 확인한다.
