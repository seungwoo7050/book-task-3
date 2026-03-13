# 03 App Distribution

동작하는 앱이 있다고 해서 곧바로 배포 준비가 끝나는 것은 아니다. 이 프로젝트는 그 사실을 분명히 하기 위해 `realtime-chat`의 verified snapshot을 release candidate로 가져오고, 제품 기능은 그대로 둔 채 env separation, workflow, rehearsal artifact만 따로 다룬다.

## 이번 글에서 따라갈 구현 순서

- verified chat snapshot 위에 release channel vocabulary를 얹는다.
- env example과 workflow를 자동으로 검증한다.
- rehearsal summary를 JSON artifact로 남긴다.

## 새로 이해한 것: 배포 준비 상태는 signed build보다 summary artifact로 더 명확하다

공개 저장소에서는 실제 credential을 담을 수 없다. 그래서 이 프로젝트는 “store 업로드를 안 했으니 배포를 못 증명한다”는 식으로 가지 않고, 대신 어떤 채널이 있고, env key가 맞고, workflow가 연결돼 있고, rehearsal summary가 재생되는지를 artifact로 남긴다.

## Phase 1
### verified snapshot 위에 release channel vocabulary를 얹는다

- 당시 목표: 제품 기능과 release discipline을 분리해 설명한다.
- 변경 단위: `react-native/src/chatModel.ts`, `react-native/src/releasePlan.ts`
- 처음 가설: 앱 동작과 release workflow를 한 번에 바꾸면 무엇을 검증하는지 흐려진다.
- 실제 진행: `chatModel.ts`는 realtime-chat의 lifecycle 규칙을 유지하고, `releasePlan.ts`가 `development`, `staging`, `production` 세 채널과 각 lane/artifact 이름을 정의하게 했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/03-app-distribution/react-native
npm test
```

검증 신호:

- release plan 테스트는 세 채널 모두가 존재함을 확인한다.
- `rehearsal_staging`, `production-summary.json` 같은 문자열이 stable summary로 고정된다.

핵심 코드:

```ts
export const releaseTargets: ReleaseTarget[] = [
  { channel: 'development', iosLane: 'ios validate_env', ... },
  { channel: 'staging', iosLane: 'ios rehearsal_staging', ... },
  { channel: 'production', iosLane: 'ios rehearsal_production', ... },
];
```

왜 이 코드가 중요했는가:

배포 프로젝트의 vocabulary가 feature 목록이 아니라 release channel 목록으로 바뀌는 지점이기 때문이다.

새로 배운 것:

- 배포 리허설은 앱을 더 만들기보다 채널과 산출물을 먼저 닫는 일이다.

다음:

- env example과 workflow를 자동 검증으로 묶는다.

## Phase 2
### env와 workflow를 자동으로 검증한다

- 당시 목표: 비밀값 없이도 release 준비 상태를 스크립트로 판단한다.
- 변경 단위: `react-native/scripts/releaseConfig.mjs`, `react-native/scripts/validate-release.mjs`, `.github/workflows/mobile-release.yml`
- 처음 가설: 공개 저장소에서 가장 강한 배포 근거는 secret이 아니라 key alignment와 automation wiring이다.
- 실제 진행: `.env.development.example`, `.env.staging.example`, `.env.production.example`의 key 집합을 읽어 비교하고, workflow/Fastlane 존재 여부를 validation summary에 넣었다. GitHub Actions는 `typecheck`, `test`, `release:validate`를 실행하게 했다.

CLI:

```bash
npm run release:validate
```

검증 신호:

- `consistentKeys`, `workflowPresent`, `fastlanePresent`가 모두 `true`
- workflow는 `npm install`, `npm run typecheck`, `npm test`, `npm run release:validate`를 순서대로 실행한다

핵심 코드:

```js
consistentKeys: envChecks.every(
  check => JSON.stringify(check.keys) === JSON.stringify(baselineKeys),
),
workflowPresent: fs.existsSync(path.join(projectRoot, '.github', 'workflows', 'mobile-release.yml')),
```

왜 이 코드가 중요했는가:

배포 준비 상태를 “문서로는 설명하지만 실제로는 모른다”가 아니라 스크립트가 바로 판정하게 만들기 때문이다.

새로 배운 것:

- release discipline의 첫 증거는 secret 그 자체가 아니라 key alignment와 automation wiring이다.

다음:

- rehearsal summary를 JSON artifact로 남긴다.

## Phase 3
### rehearsal summary를 artifact로 남긴다

- 당시 목표: 로컬 리허설이 summary file을 남기게 만들어 배포 준비 상태를 재생한다.
- 변경 단위: `react-native/scripts/release-rehearsal.mjs`, `react-native/release/rehearsal-summary.json`
- 처음 가설: “배포 준비가 됐다”는 문장보다 `rehearsal-summary.json`이 더 재현 가능한 근거다.
- 실제 진행: validation summary 위에 android/ios/workflow rehearsal 설명을 덧붙여 `release/rehearsal-summary.json`을 다시 쓰게 했다.

CLI:

```bash
npm run verify
npm run release:rehearsal
```

검증 신호:

- current replay에서 `PASS tests/realtime-chat.test.ts`, `PASS tests/release-plan.test.ts`
- `Test Suites: 2 passed`
- `Tests: 5 passed`
- `release rehearsal summary written to .../release/rehearsal-summary.json`
- artifact에는 세 env example의 동일 key 집합과 rehearsal 설명이 함께 남는다

핵심 코드:

```js
const summary = {
  ...buildValidationSummary(),
  rehearsal: {
    android: 'signed build rehearsal configured via Fastlane lane and placeholder keystore env keys',
    ios: 'archive dry-run configured via Fastlane lane and placeholder export options',
    workflow: 'mobile-release.yml runs typecheck, test, release:validate',
  },
};
```

왜 이 코드가 중요했는가:

배포 문제를 signed artifact 유무가 아니라 rehearsal artifact 재생 여부로 옮겨 놓기 때문이다.

새로 배운 것:

- 공개 저장소에서도 release discipline은 충분히 학습 가능하고, 그 핵심 출력물은 summary artifact다.

다음:

- 다음 단계에서는 같은 incident domain을 contract harness와 hiring-facing client라는 두 프로젝트로 분리해 다룬다.

## 여기까지 정리

- 이 프로젝트가 실제로 남긴 것은 기능 추가가 아니라, release vocabulary와 automation wiring, rehearsal artifact를 하나의 독립 문제로 분리한 감각이다.
- 다음 단계의 질문: 같은 도메인을 contract 증명과 product UX로 나누면 무엇이 더 선명해질까?
