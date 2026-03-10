# Development Timeline — App Distribution

이 문서는 프로젝트의 전체 개발 과정을 시간순으로 기록한다.
소스코드만으로는 알 수 없는 CLI 명령, 설치 과정, 설정 변경, 의사결정 맥락을 포함한다.

---

## Phase 1: 앱 스냅샷 복사

### realtime-chat에서 프로젝트 복사

```bash
cp -r study/Chat-Product-Systems/realtime-chat/react-native study/Chat-Product-Systems/app-distribution/react-native
```

복사 후 `package.json`의 `name`을 `AppDistributionStudy`로 변경하고, 배포 전용 scripts를 추가했다:
- `release:validate` — `node ./scripts/validate-release.mjs`
- `release:rehearsal` — `node ./scripts/release-rehearsal.mjs`

### 의존성 재설치

```bash
cd study/Chat-Product-Systems/app-distribution/react-native
rm -rf node_modules package-lock.json
npm install
```

기존 realtime-chat의 lock file이 아닌 독립적인 의존성 트리를 확보했다.

### iOS Pod 재설치

```bash
cd ios && bundle install && bundle exec pod install && cd ..
```

---

## Phase 2: 환경 분리 설정

### env example 파일 생성

세 환경의 `.env.*.example` 파일을 수동으로 생성했다:

```bash
touch .env.development.example .env.staging.example .env.production.example
```

각 파일에 동일한 네 가지 키를 넣되 값만 환경에 맞게 설정:
- `API_BASE_URL` — development는 localhost, staging/production은 도메인
- `WS_BASE_URL` — WebSocket 엔드포인트
- `RELEASE_CHANNEL` — 환경 이름
- `SENTRY_DSN` — placeholder 값

### env 검증 스크립트 작성

`scripts/releaseConfig.mjs` 작성:
1. `.env.*.example` 파일을 파싱하는 `parseEnvFile` 함수
2. 세 env 파일의 키 집합이 동일한지 비교하는 `buildValidationSummary` 함수
3. Fastfile과 GitHub Actions workflow 파일 존재 여부 확인

`scripts/validate-release.mjs` 작성:
- `buildValidationSummary`를 호출하고, 키 불일치/파일 누락 시 `process.exit(1)`

```bash
node scripts/validate-release.mjs
# 성공 시 JSON summary 출력, 실패 시 에러 메시지와 exit code 1
```

---

## Phase 3: Fastlane 설정

### Fastlane 초기화

```bash
mkdir -p fastlane
```

`Gemfile`은 realtime-chat에서 이미 복사되어 있었다. Fastlane gem이 포함되어 있으므로 별도 설치 없이 진행했다.

### Fastfile 작성

`fastlane/Appfile`과 `fastlane/Fastfile`을 작성했다.

Fastfile 구조:
- iOS platform: `validate_env`, `rehearsal_staging`, `rehearsal_production`
- Android platform: 동일한 세 lane

모든 rehearsal lane은 `validate_env`를 먼저 호출한 뒤 dry-run echo를 출력한다. 실제 빌드 명령은 의도적으로 생략했다.

```bash
bundle exec fastlane ios validate_env
bundle exec fastlane android validate_env
```

---

## Phase 4: CI 파이프라인 설정

### GitHub Actions 워크플로우 작성

```bash
mkdir -p .github/workflows
```

`mobile-release.yml` 작성:
- 트리거: `workflow_dispatch` + `pull_request` (app-distribution 경로 한정)
- 환경: `ubuntu-latest`, Node 22
- 스텝: checkout → setup-node → npm install → typecheck → test → release:validate

이 워크플로우는 빌드나 배포를 하지 않는다. 순수하게 "릴리스 자격 검증"만 수행한다.

---

## Phase 5: 릴리스 계획 코드화

### releasePlan.ts 작성

세 채널의 release target을 TypeScript 타입으로 정의:
- `ReleaseChannel` 유니언: `'development' | 'staging' | 'production'`
- `ReleaseTarget` 인터페이스: channel, iosLane, androidLane, artifact 경로
- `summarizeReleaseTargets()` — 각 타겟을 한 줄 문자열로 요약

### release-plan.test.ts 작성

두 가지 테스트:
1. 세 채널이 올바른 순서로 정의되어 있는지
2. summary 문자열이 해당 채널의 lane과 artifact 경로를 포함하는지

```bash
npm test -- --verbose
```

---

## Phase 6: 리허설 실행

### release-rehearsal.mjs 작성

```bash
node scripts/release-rehearsal.mjs
```

이 스크립트는:
1. `releaseConfig.mjs`의 `buildValidationSummary()`를 호출해 검증 결과를 얻는다
2. Fastlane/workflow 리허설 메타데이터를 추가한다
3. 검증이 실패하면 에러를 출력하고 종료한다
4. 성공하면 `release/rehearsal-summary.json`에 결과를 기록한다

### Make 기반 리허설

```bash
cd problem
make release-rehearsal
# → npm install + node scripts/release-rehearsal.mjs
```

---

## Phase 7: 빌드 검증

```bash
npm run typecheck        # TypeScript 타입 체크
npm test                 # Jest 실행
npm run release:validate # env/fastlane/workflow 검증
npm run release:rehearsal # 리허설 요약 생성
npm run verify           # typecheck + test

# Make 기반
make test               # verify_task.sh
make app-build          # npm install + typecheck
make app-test           # npm install + jest
make release-rehearsal  # 리허설 실행
```

---

## 사용한 CLI 명령 전체 요약

| 단계 | 명령 | 목적 |
|------|------|------|
| 복사 | `cp -r ...realtime-chat/react-native ...app-distribution/react-native` | 앱 스냅샷 복사 |
| 의존성 | `npm install` | 독립 의존성 확보 |
| iOS | `cd ios && bundle install && bundle exec pod install` | 네이티브 의존성 |
| Fastlane | `bundle exec fastlane ios validate_env` | lane 실행 테스트 |
| 검증 | `node scripts/validate-release.mjs` | 릴리스 자격 검증 |
| 리허설 | `node scripts/release-rehearsal.mjs` | 요약 artifact 생성 |
| 테스트 | `npm test` | Jest 실행 |
| CI | GitHub Actions `mobile-release.yml` | 자동 검증 |
| Make | `make release-rehearsal` | 통합 리허설 |
