# 01 Bridge Vs JSI

이 프로젝트의 출발점은 “JSI가 더 빠르다”는 익숙한 문장을 반복하는 데 있지 않았다. 지금 저장소의 기준 버전이 RN `0.84.1`이라면, 더 의미 있는 질문은 legacy/new runtime 토글이 아니라 async serialized surface와 sync direct-call surface를 같은 workload로 비교하는 일이었다.

## 이번 글에서 따라갈 구현 순서

- `benchmark.ts`에서 같은 payload를 쓰는 두 surface를 정의한다.
- `BridgeVsJsiStudyApp.tsx`에서 결과를 카드형 대시보드로 보여 준다.
- `export-results.mjs`와 테스트로 결과를 JSON artifact로 남긴다.

## 새로 이해한 것: architecture 비교도 현재 버전에 맞는 질문으로 다시 써야 한다

이 앱이 바꾼 것은 구현보다 질문이다. old/new runtime 토글을 고집하는 대신, `Promise + serialized payload`와 `sync direct-call`이라는 실제 surface 차이를 같은 payload size로 비교하게 만들었다. 덕분에 architecture 이야기가 현재 코드와 더 직접 연결된다.

## Phase 1
### runtime toggle 대신 workload 비교로 질문을 다시 잡는다

- 당시 목표: legacy/new runtime 전환이 아니라 async vs sync surface의 비용 차이를 같은 payload로 비교한다.
- 변경 단위: `react-native/src/benchmark.ts`
- 처음 가설: RN `0.84.1` 기준에서는 runtime 토글 실험보다 JS surface 차이를 같은 workload에 태우는 편이 더 실용적이다.
- 실제 진행: `RUNS`에 `async serialized`, `sync direct-call` 두 benchmark를 정의하고, 둘 다 `payloadSize: 1000`과 `5`개 sample을 갖게 했다. `computeStats()`는 mean과 stddev 계산만 맡게 했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/01-bridge-vs-jsi/react-native
npm run typecheck
```

검증 신호:

- 두 run은 모두 `payloadSize: 1000`을 공유한다.
- `computeStats()`가 sample 평균과 표준편차를 결정적으로 계산한다.

핵심 코드:

```ts
export const RUNS: BenchmarkRun[] = [
  { label: 'async serialized', payloadSize: 1000, samples: [42, 45, 44, 47, 43] },
  { label: 'sync direct-call', payloadSize: 1000, samples: [11, 10, 12, 10, 11] },
];
```

왜 이 코드가 중요했는가:

architecture 비교를 “지금 버전에서 재현 가능한 workload”로 바꾸는 출발점이기 때문이다.

새로 배운 것:

- architecture 논의도 버전에 맞는 질문으로 다시 써야 의미가 유지된다.

다음:

- benchmark 결과를 문서 설명이 아니라 앱 화면에서 읽히게 만든다.

## Phase 2
### benchmark 결과를 대시보드처럼 읽히게 만든다

- 당시 목표: 수치 비교를 RN 화면 안에서 바로 읽을 수 있게 만든다.
- 변경 단위: `react-native/src/BridgeVsJsiStudyApp.tsx`
- 처음 가설: architecture 과제라도 결과 surface가 있으면 추상론보다 훨씬 덜 미끄럽다.
- 실제 진행: `RUNS.map(computeStats)`를 카드 두 장으로 렌더링해 label, payload, mean, stddev를 바로 보여 줬다. 앱은 비교기 자체가 아니라 결과를 요약하는 dashboard 역할을 맡았다.

CLI:

```bash
npm test
```

검증 신호:

- 현재 테스트는 `computeStats()`의 산출 형식과 `buildExport()`의 shape를 함께 확인한다.
- 화면은 `async serialized`, `sync direct-call`, `mean`, `stddev`를 카드 단위로 노출한다.

핵심 코드:

```ts
{stats.map(stat => (
  <View key={stat.label} style={styles.card}>
    <Text style={styles.cardTitle}>{stat.label}</Text>
    <Text style={styles.cardBody}>mean: {stat.mean}ms</Text>
    <Text style={styles.cardBody}>stddev: {stat.stddev}ms</Text>
  </View>
))}
```

왜 이 코드가 중요했는가:

runtime 설명이 추상 문장 대신 실제 비교 결과 카드로 내려오는 지점이기 때문이다.

새로 배운 것:

- architecture 글도 결과 surface가 있어야 독자가 지금 무엇을 비교 중인지 놓치지 않는다.

다음:

- export file을 추가해 benchmark를 화면 밖에서도 재생 가능하게 만든다.

## Phase 3
### export 결과를 artifact로 남긴다

- 당시 목표: benchmark 결과를 JSON export까지 포함한 공개 artifact로 닫는다.
- 변경 단위: `react-native/scripts/export-results.mjs`, `react-native/tests/bridge-vs-jsi.test.tsx`
- 처음 가설: 숫자 비교는 앱 화면만으로는 부족하고, 다른 문서와 연결할 수 있는 file artifact가 필요하다.
- 실제 진행: `export-results.mjs`가 `exports/benchmark-results.json`을 다시 쓰게 하고, 테스트는 `buildExport()`가 `RUNS.map(computeStats)`와 정확히 일치하는지 확인했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS tests/bridge-vs-jsi.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 2 passed`
- `benchmark results written to exports/benchmark-results.json`
- export 결과는 `async serialized mean 44.2ms`, `sync direct-call mean 10.8ms`

핵심 코드:

```js
fs.writeFileSync(
  path.join(outputDir, 'benchmark-results.json'),
  JSON.stringify({ generatedAt: '2026-03-08', results: [...] }, null, 2),
);
```

왜 이 코드가 중요했는가:

architecture 비교가 문장 설명이 아니라 저장 가능한 artifact로 남는 지점이기 때문이다.

새로 배운 것:

- benchmark의 설명력은 평균값 자체보다 export 가능한 결과물 여부에서 커진다.

다음:

- 다음 프로젝트에서는 cost 비교 대신 JS/native boundary를 typed spec과 codegen summary로 설명한다.

## 여기까지 정리

- 이 프로젝트가 남긴 핵심은 JSI를 칭찬한 것이 아니라, 현재 버전의 RN에서 의미 있는 비교 질문을 다시 정했다는 점이다.
- 다음 단계의 질문: runtime surface 대신 module boundary는 어떤 계약과 artifact로 설명해야 할까?
