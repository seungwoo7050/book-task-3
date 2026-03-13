# Evidence Ledger: 03 App Distribution

## 독립 프로젝트 판정

- 판정: 처리
- 근거: release plan, env validation, Fastlane/workflow, rehearsal artifact를 자기 폴더 안에 독립적으로 갖춘 배포 리허설 프로젝트다.
- 소스 경로: `mobile/study/product-systems/03-app-distribution`

## 사용한 근거

- `mobile/study/product-systems/03-app-distribution/README.md`
- `mobile/study/product-systems/03-app-distribution/problem/README.md`
- `mobile/study/product-systems/03-app-distribution/react-native/README.md`
- `mobile/study/product-systems/03-app-distribution/docs/concepts/release-rehearsal.md`
- `mobile/study/product-systems/03-app-distribution/docs/concepts/env-separation.md`
- `mobile/study/product-systems/03-app-distribution/react-native/src/chatModel.ts`
- `mobile/study/product-systems/03-app-distribution/react-native/src/releasePlan.ts`
- `mobile/study/product-systems/03-app-distribution/react-native/scripts/releaseConfig.mjs`
- `mobile/study/product-systems/03-app-distribution/react-native/scripts/validate-release.mjs`
- `mobile/study/product-systems/03-app-distribution/react-native/scripts/release-rehearsal.mjs`
- `mobile/study/product-systems/03-app-distribution/react-native/tests/release-plan.test.ts`
- `mobile/study/product-systems/03-app-distribution/react-native/tests/realtime-chat.test.ts`
- `mobile/study/product-systems/03-app-distribution/react-native/release/rehearsal-summary.json`
- `mobile/study/product-systems/03-app-distribution/react-native/.github/workflows/mobile-release.yml`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/03-app-distribution/react-native
npm install --no-audit --no-fund
npm run verify
npm run release:rehearsal
```

## Chronology Ledger

### Phase 1 | verified chat snapshot을 release candidate로 고정한다

- 당시 목표: 제품 기능 자체는 `realtime-chat`과 같게 두고, 배포 문제만 따로 다룬다.
- 변경 단위: `react-native/src/chatModel.ts`, `react-native/src/releasePlan.ts`
- 처음 가설: 앱 기능과 release discipline을 한 번에 바꾸면 무엇을 검증하는지 흐려진다.
- 실제 조치: `chatModel.ts`는 realtime-chat의 lifecycle 규칙을 유지하고, `releasePlan.ts`에서 `development`, `staging`, `production` 세 채널과 lane/artifact 이름을 따로 정의했다.
- CLI:
```bash
npm test
```
- 검증 신호:
- `releaseTargets`는 세 채널을 모두 가진다.
- release plan 테스트는 `rehearsal_staging`, `production-summary.json` 문자열을 확인한다.
- 핵심 코드 앵커:
```ts
export const releaseTargets: ReleaseTarget[] = [
  { channel: 'development', iosLane: 'ios validate_env', ... },
  { channel: 'staging', iosLane: 'ios rehearsal_staging', ... },
  { channel: 'production', iosLane: 'ios rehearsal_production', ... },
];
```
- 새로 배운 것: 배포 리허설은 제품 기능을 늘리는 일이 아니라 release channel vocabulary를 먼저 고정하는 일이다.
- 다음: env 예시와 workflow를 검증하는 스크립트를 붙인다.

### Phase 2 | env와 workflow를 자동으로 검증한다

- 당시 목표: 비밀값 없이도 release 준비 상태를 스크립트로 점검한다.
- 변경 단위: `react-native/scripts/releaseConfig.mjs`, `react-native/scripts/validate-release.mjs`, `.github/workflows/mobile-release.yml`
- 처음 가설: 공개 저장소에서는 signed build보다 env key alignment와 workflow 존재 자체가 더 중요한 evidence다.
- 실제 조치: `.env.*.example` 파일을 읽어 key 집합 일치 여부를 검사하고, workflow/Fastlane 존재 여부를 validation summary에 넣었다.
- CLI:
```bash
npm run release:validate
```
- 검증 신호:
- `consistentKeys`, `workflowPresent`, `fastlanePresent`가 모두 `true`
- workflow는 `typecheck`, `test`, `release:validate`를 실행한다.
- 핵심 코드 앵커:
```js
return {
  checkedAt: '2026-03-08',
  envChecks,
  consistentKeys: envChecks.every(...),
  workflowPresent: fs.existsSync(...'mobile-release.yml'),
  fastlanePresent: fs.existsSync(...'Fastfile'),
};
```
- 새로 배운 것: release discipline의 첫 증거는 비밀값이 아니라 key alignment와 automation wiring이다.
- 다음: rehearsal summary를 artifact로 남긴다.

### Phase 3 | rehearsal summary를 배포 artifact로 남긴다

- 당시 목표: local rehearsal command가 release 준비 상태를 JSON으로 남기게 만든다.
- 변경 단위: `react-native/scripts/release-rehearsal.mjs`, `react-native/release/rehearsal-summary.json`
- 처음 가설: “배포 준비가 됐다”는 말보다 rehearsal summary file이 훨씬 재현 가능하다.
- 실제 조치: `release-rehearsal.mjs`가 validation summary 위에 android/ios/workflow rehearsal 설명을 덧붙여 `release/rehearsal-summary.json`을 다시 쓴다.
- CLI:
```bash
npm run verify
npm run release:rehearsal
```
- 검증 신호:
- current replay에서 `PASS tests/realtime-chat.test.ts`, `PASS tests/release-plan.test.ts`
- `Test Suites: 2 passed`, `Tests: 5 passed`
- `release rehearsal summary written to .../release/rehearsal-summary.json`
- summary에는 세 env example의 동일 key 집합과 rehearsal 설명이 들어간다.
- 핵심 코드 앵커:
```js
const summary = {
  ...buildValidationSummary(),
  rehearsal: {
    android: 'signed build rehearsal configured via Fastlane lane and placeholder keystore env keys',
    ios: 'archive dry-run configured via Fastlane lane and placeholder export options',
  },
};
```
- 새로 배운 것: 배포 문제는 signed binary가 없어도 rehearsal artifact로 충분히 학습할 수 있다.
- 다음: 다음 단계에서는 동일 incident domain을 계약 harness와 hiring-facing client 두 프로젝트로 나눠 다룬다.
