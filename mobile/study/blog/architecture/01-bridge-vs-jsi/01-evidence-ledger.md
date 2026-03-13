# Evidence Ledger: 01 Bridge Vs JSI

## 독립 프로젝트 판정

- 판정: 처리
- 근거: benchmark 문제 정의, RN 구현, export script, 테스트, generated artifact path를 한 폴더 안에 갖춘 독립 benchmark 앱이다.
- 소스 경로: `mobile/study/architecture/01-bridge-vs-jsi`

## 사용한 근거

- `mobile/study/architecture/01-bridge-vs-jsi/README.md`
- `mobile/study/architecture/01-bridge-vs-jsi/problem/README.md`
- `mobile/study/architecture/01-bridge-vs-jsi/react-native/README.md`
- `mobile/study/architecture/01-bridge-vs-jsi/docs/concepts/modernized-runtime-benchmark.md`
- `mobile/study/architecture/01-bridge-vs-jsi/react-native/src/benchmark.ts`
- `mobile/study/architecture/01-bridge-vs-jsi/react-native/src/BridgeVsJsiStudyApp.tsx`
- `mobile/study/architecture/01-bridge-vs-jsi/react-native/scripts/export-results.mjs`
- `mobile/study/architecture/01-bridge-vs-jsi/react-native/tests/bridge-vs-jsi.test.tsx`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/01-bridge-vs-jsi/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | runtime toggle 대신 workload 비교로 질문을 다시 잡는다

- 당시 목표: legacy/new runtime 전환이 아니라 async vs sync surface의 비용 차이를 같은 payload로 비교한다.
- 변경 단위: `react-native/src/benchmark.ts`
- 처음 가설: RN 0.84에서는 runtime 토글보다 JS surface 차이를 같은 workload에 태우는 편이 더 실용적이다.
- 실제 조치: `RUNS`를 `async serialized`와 `sync direct-call` 두 표면으로 정의하고, 둘 다 `payloadSize: 1000`과 `5`개 sample을 갖게 했다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- 두 run 모두 같은 payload size를 쓴다.
- sample 기반 mean/stddev 계산이 `computeStats()`에 모인다.
- 핵심 코드 앵커:
```ts
export const RUNS: BenchmarkRun[] = [
  { label: 'async serialized', payloadSize: 1000, samples: [42, 45, 44, 47, 43] },
  { label: 'sync direct-call', payloadSize: 1000, samples: [11, 10, 12, 10, 11] },
];
```
- 새로 배운 것: architecture 비교도 현재 버전에 맞게 질문을 현대화해야 증거가 살아 남는다.
- 다음: benchmark를 카드형 대시보드로 드러낸다.

### Phase 2 | benchmark를 화면에서 읽히게 만든다

- 당시 목표: 숫자를 README 설명 대신 앱 화면에서 바로 읽을 수 있게 만든다.
- 변경 단위: `react-native/src/BridgeVsJsiStudyApp.tsx`
- 처음 가설: architecture 과제라도 결과가 UI surface를 가지면 나중에 문서와 연결하기가 쉽다.
- 실제 조치: `RUNS.map(computeStats)` 결과를 카드 두 장으로 렌더링해 label, payload, mean, stddev를 바로 보여 줬다.
- CLI:
```bash
npm test
```
- 검증 신호:
- 카드에는 `async serialized`, `sync direct-call`, `mean`, `stddev`가 모두 드러난다.
- 테스트가 `computeStats()`와 `buildExport()`의 결정적 shape를 확인한다.
- 핵심 코드 앵커:
```ts
{stats.map(stat => (
  <View key={stat.label} style={styles.card}>
    <Text style={styles.cardTitle}>{stat.label}</Text>
    <Text style={styles.cardBody}>mean: {stat.mean}ms</Text>
    <Text style={styles.cardBody}>stddev: {stat.stddev}ms</Text>
  </View>
))}
```
- 새로 배운 것: architecture 설명도 결과 surface가 있어야 추상론에서 덜 미끄러진다.
- 다음: benchmark를 export file까지 포함한 공개 artifact로 닫는다.

### Phase 3 | export 결과를 공개 artifact로 남긴다

- 당시 목표: benchmark 결과를 앱 화면뿐 아니라 JSON export로도 재생한다.
- 변경 단위: `react-native/scripts/export-results.mjs`, `react-native/tests/bridge-vs-jsi.test.tsx`
- 처음 가설: 수치 비교는 화면보다 export artifact가 있어야 다른 문서나 검증 흐름과 연결하기 쉽다.
- 실제 조치: `export-results.mjs`가 `exports/benchmark-results.json`을 만들고, 테스트가 `buildExport()` 결과를 잠그게 했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS tests/bridge-vs-jsi.test.tsx`
- `Test Suites: 1 passed`, `Tests: 2 passed`
- `benchmark results written to exports/benchmark-results.json`
- export 값은 `44.2ms / 1.72` vs `10.8ms / 0.75`
- 핵심 코드 앵커:
```js
console.log('benchmark results written to exports/benchmark-results.json');
```
- 새로 배운 것: benchmark의 설명력은 평균값 자체보다 export 가능한 결과물 여부에서 커진다.
- 다음: 다음 프로젝트에서는 benchmark 대신 JS/native boundary를 spec과 codegen으로 설명한다.
