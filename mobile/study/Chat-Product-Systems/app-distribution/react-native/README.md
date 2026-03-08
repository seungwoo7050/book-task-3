# React Native Implementation

Status: verified

이 구현은 `realtime-chat`의 verified snapshot을 release candidate로 복사한 뒤,
배포 리허설 자산을 덧붙인 앱이다. 제품 기능은 `realtime-chat`과 같고, 이 과제의 핵심은
Fastlane, workflow, env separation, rehearsal summary를 검증하는 데 있다.

## Commands

```bash
npm install
npm run typecheck
npm test
npm run release:validate
npm run release:rehearsal
```

## Release Assets

- `fastlane/Fastfile`
- `.github/workflows/mobile-release.yml`
- `.env.development.example`
- `.env.staging.example`
- `.env.production.example`
- `release/rehearsal-summary.json`

## Known Scope

- signed artifact 생성은 dry-run summary로 대체한다
- 실제 store upload lane은 문서로만 남긴다
- 비밀값은 모두 placeholder 예시로만 제공한다
