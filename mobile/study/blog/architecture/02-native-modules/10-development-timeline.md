# 02 Native Modules

native module 학습은 쉽게 플랫폼별 예제 모음으로 흘러간다. 이 프로젝트가 택한 방향은 반대였다. Battery, Haptics, Sensor를 각각 구현 디테일보다 public contract로 먼저 보고, 그 spec를 consumer 화면과 generated summary가 같이 읽게 만드는 것이 핵심이었다.

## 이번 글에서 따라갈 구현 순서

- `specs.ts`에서 세 모듈의 public contract를 먼저 정의한다.
- `NativeModulesStudyApp.tsx`에서 consumer surface가 같은 vocabulary를 쓰게 한다.
- `codegen-summary.mjs`와 `generated/modules.json`으로 reproducible artifact를 남긴다.

## 새로 이해한 것: native boundary의 핵심은 build보다 contract alignment다

이 프로젝트는 full native build보다 `spec -> consumer -> generated summary` 세 층이 같은 이름과 method count를 공유하는지를 더 중요하게 본다. 덕분에 “무엇을 연동하는가”보다 “어떤 contract를 유지하는가”가 글의 중심으로 올라온다.

## Phase 1
### public spec를 먼저 고정한다

- 당시 목표: Battery, Haptics, Sensor를 기능 설명보다 public contract로 먼저 정의한다.
- 변경 단위: `react-native/src/specs.ts`
- 처음 가설: 네이티브 연동은 플랫폼 구현 예제보다 spec가 먼저 보여야 JS/native boundary가 선명해진다.
- 실제 진행: `MODULE_SPECS`에 module name과 method 목록을 넣고, `buildGeneratedSummary()`가 module/methodCount shape로 축약하게 했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/02-native-modules/react-native
npm run typecheck
```

검증 신호:

- 세 모듈의 이름과 method 목록이 코드에서 직접 드러난다.
- generated summary는 이 spec에서만 파생된다.

핵심 코드:

```ts
export const MODULE_SPECS = [
  { name: 'BatteryModule', methods: ['getBatteryLevel', 'getChargingStatus', 'subscribe'] },
  { name: 'HapticsModule', methods: ['vibrate', 'impactFeedback', 'notificationFeedback'] },
  { name: 'SensorModule', methods: ['startAccelerometer', 'stopAccelerometer', 'startGyroscope', 'stopGyroscope'] },
];
```

왜 이 코드가 중요했는가:

boundary 설명이 “네이티브로 뭘 했다”보다 “어떤 계약을 노출한다”로 바뀌는 지점이기 때문이다.

새로 배운 것:

- native module은 기능 구현보다 public contract 설계 문제로 보는 편이 훨씬 재현 가능하다.

다음:

- consumer 앱이 이 contract를 그대로 읽게 만든다.

## Phase 2
### consumer surface가 spec를 그대로 읽게 만든다

- 당시 목표: codegen 이전에도 spec가 화면에서 바로 읽히게 만든다.
- 변경 단위: `react-native/src/NativeModulesStudyApp.tsx`
- 처음 가설: spec와 consumer가 따로 놀면 generated summary가 나와도 boundary 설명은 여전히 추상적이다.
- 실제 진행: 앱이 `MODULE_SPECS.map(...)` 결과를 카드로 렌더링해 module name과 method 목록을 그대로 보여 주게 했다.

CLI:

```bash
npm test
```

검증 신호:

- current 테스트는 `MODULE_SPECS` 길이와 각 method 집합의 존재를 확인한다.
- 화면은 세 모듈의 이름과 method 목록을 그대로 읽는다.

핵심 코드:

```ts
{MODULE_SPECS.map(spec => (
  <View key={spec.name} style={styles.card}>
    <Text style={styles.cardTitle}>{spec.name}</Text>
    <Text style={styles.cardBody}>{spec.methods.join(' · ')}</Text>
  </View>
))}
```

왜 이 코드가 중요했는가:

contract와 consumer가 같은 vocabulary를 쓰는지 한눈에 드러나는 지점이기 때문이다.

새로 배운 것:

- boundary 문서는 spec, consumer, generated summary가 같은 언어를 공유할 때 비로소 설명력이 생긴다.

다음:

- generated summary를 artifact와 테스트로 잠근다.

## Phase 3
### codegen summary를 reproducible artifact로 남긴다

- 당시 목표: full native build 대신 reproducible generated summary를 공식 산출물로 둔다.
- 변경 단위: `react-native/scripts/codegen-summary.mjs`, `react-native/tests/native-modules.test.tsx`, `react-native/generated/modules.json`
- 처음 가설: 이 저장소의 공용 게이트는 build log보다 contract clarity와 reproducible summary에 있다.
- 실제 진행: script가 `generated/modules.json`을 다시 쓰고, 테스트는 `buildGeneratedSummary()`가 세 모듈의 method count를 정확히 반영하는지 확인했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `generated summary written to generated/modules.json`
- `PASS tests/native-modules.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 2 passed`
- artifact는 `Battery 3`, `Haptics 3`, `Sensor 4` method count를 남긴다

핵심 코드:

```js
fs.writeFileSync(
  path.join(outputDir, 'modules.json'),
  JSON.stringify([
    { module: 'BatteryModule', methodCount: 3 },
    { module: 'HapticsModule', methodCount: 3 },
    { module: 'SensorModule', methodCount: 4 },
  ], null, 2),
);
```

왜 이 코드가 중요했는가:

spec가 generated artifact로 내려와 consumer와 같은 이름을 공유하는 순간, boundary 설명이 문서 밖으로 나온다.

새로 배운 것:

- native boundary의 canonical evidence는 build 자체보다 spec/codegen/consumer alignment다.

다음:

- 다음 단계에서는 architecture boundary를 떠나 queue/retry/DLQ 같은 product-system 규칙을 standalone 문제로 다룬다.

## 여기까지 정리

- 이 프로젝트가 실제로 남긴 것은 세 모듈 자체보다, contract를 중심으로 boundary를 설명하는 방식이다.
- 다음 단계의 질문: 제품형 문제로 넘어가기 전에 sync 규칙은 어디까지 독립적으로 떼어 연습해야 할까?
