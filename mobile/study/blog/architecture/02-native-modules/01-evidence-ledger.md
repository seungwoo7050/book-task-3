# Evidence Ledger: 02 Native Modules

## 독립 프로젝트 판정

- 판정: 처리
- 근거: typed spec, codegen summary script, generated artifact, consumer app, tests가 모두 한 폴더 안에 있다.
- 소스 경로: `mobile/study/architecture/02-native-modules`

## 사용한 근거

- `mobile/study/architecture/02-native-modules/README.md`
- `mobile/study/architecture/02-native-modules/problem/README.md`
- `mobile/study/architecture/02-native-modules/react-native/README.md`
- `mobile/study/architecture/02-native-modules/docs/concepts/spec-and-codegen.md`
- `mobile/study/architecture/02-native-modules/react-native/src/specs.ts`
- `mobile/study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`
- `mobile/study/architecture/02-native-modules/react-native/scripts/codegen-summary.mjs`
- `mobile/study/architecture/02-native-modules/react-native/tests/native-modules.test.tsx`
- `mobile/study/architecture/02-native-modules/react-native/generated/modules.json`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/02-native-modules/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | public spec를 먼저 고정한다

- 당시 목표: Battery, Haptics, Sensor를 기능 설명보다 public contract로 먼저 정의한다.
- 변경 단위: `react-native/src/specs.ts`
- 처음 가설: 네이티브 연동은 플랫폼 구현 예제보다 spec이 먼저 보여야 경계가 선명해진다.
- 실제 조치: `MODULE_SPECS` 배열에 module name과 method 목록을 고정하고, `buildGeneratedSummary()`가 method count만 뽑도록 했다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- 세 모듈 모두 이름과 method 목록이 명시적으로 드러난다.
- summary는 module/methodCount shape로 축약된다.
- 핵심 코드 앵커:
```ts
export const MODULE_SPECS = [
  { name: 'BatteryModule', methods: ['getBatteryLevel', 'getChargingStatus', 'subscribe'] },
  ...
];
```
- 새로 배운 것: JS/native boundary는 기능 데모보다 public spec가 먼저여야 설명 가능하다.
- 다음: spec를 consumer surface에 연결한다.

### Phase 2 | consumer 앱이 spec를 읽게 만든다

- 당시 목표: codegen 이전에도 spec가 화면에서 바로 읽히게 만든다.
- 변경 단위: `react-native/src/NativeModulesStudyApp.tsx`
- 처음 가설: spec와 consumer가 따로 놀면 codegen summary도 독자가 연결하기 어렵다.
- 실제 조치: 앱이 `MODULE_SPECS.map(...)` 결과를 카드로 그리며 module name과 method 목록을 보여 주게 했다.
- CLI:
```bash
npm test
```
- 검증 신호:
- 소비 화면은 Battery, Haptics, Sensor 세 모듈과 method 이름을 그대로 노출한다.
- 테스트는 `MODULE_SPECS` 길이와 method 존재를 확인한다.
- 핵심 코드 앵커:
```ts
{MODULE_SPECS.map(spec => (
  <View key={spec.name} style={styles.card}>
    <Text style={styles.cardTitle}>{spec.name}</Text>
    <Text style={styles.cardBody}>{spec.methods.join(' · ')}</Text>
  </View>
))}
```
- 새로 배운 것: boundary 문서는 spec, consumer, generated summary가 같은 vocabulary를 공유해야 한다.
- 다음: codegen summary를 artifact로 재생한다.

### Phase 3 | codegen summary를 공개 artifact로 남긴다

- 당시 목표: full native build 대신 reproducible generated summary를 공식 산출물로 둔다.
- 변경 단위: `react-native/scripts/codegen-summary.mjs`, `react-native/tests/native-modules.test.tsx`, `react-native/generated/modules.json`
- 처음 가설: 이 저장소의 게이트는 native binary가 아니라 contract clarity와 reproducible summary에 있다.
- 실제 조치: script가 `generated/modules.json`을 다시 쓰고, 테스트는 `buildGeneratedSummary()`의 결과를 고정했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `generated summary written to generated/modules.json`
- `PASS tests/native-modules.test.tsx`
- `Test Suites: 1 passed`, `Tests: 2 passed`
- artifact는 `Battery 3`, `Haptics 3`, `Sensor 4` method count를 남긴다.
- 핵심 코드 앵커:
```js
console.log('generated summary written to generated/modules.json');
```
- 새로 배운 것: native boundary의 canonical evidence는 build log보다 spec/codegen/consumer alignment다.
- 다음: 다음 단계에서는 product-systems 트랙으로 넘어가 queue/retry 규칙을 standalone 문제로 다룬다.
