# Knowledge Index — App Distribution

## 연결된 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| `realtime-chat` | 선행 과제. 이 프로젝트의 앱 코드는 realtime-chat의 verified 스냅샷이다. |
| `offline-sync-foundations` | 간접 연결. realtime-chat의 sync 모델이 이 앱에 포함되어 있다. |
| `virtualized-list` | 패턴 유사. benchmark-summary.json과 rehearsal-summary.json은 같은 "검증 결과 artifact" 패턴이다. |
| `incident-ops-mobile-client` | 최종 캡스톤 앱의 배포 시 이 프로젝트의 Fastlane/CI 파이프라인을 참고. |

## 재사용 가능한 패턴

### Env Consistency Validation 패턴
여러 환경의 env 파일이 동일한 키 집합을 유지하는지 스크립트로 검증하는 패턴.
모든 멀티 환경 프로젝트에 적용 가능하다.

### Rehearsal Artifact 패턴
검증 결과를 JSON 파일로 남겨서, "이 검증을 언제 마지막으로 통과했는가"를 추적하는 패턴.
benchmark, release, migration 등 다양한 검증에 재사용 가능하다.

### Validate-then-Act Lane 구조
Fastlane lane을 validate → act 순서로 구성하면, 실제 빌드/배포 전에 전제 조건을 검증할 수 있다.

## 핵심 파일 참조

| 파일 | 역할 |
|------|------|
| `react-native/src/releasePlan.ts` | 세 채널의 릴리스 타겟 정의 |
| `react-native/scripts/releaseConfig.mjs` | env 파싱, 검증 summary 빌드 |
| `react-native/scripts/validate-release.mjs` | env/workflow/fastlane 검증 실행 |
| `react-native/scripts/release-rehearsal.mjs` | 리허설 요약 JSON 생성 |
| `react-native/fastlane/Fastfile` | iOS/Android rehearsal lane 정의 |
| `react-native/.github/workflows/mobile-release.yml` | CI 파이프라인 정의 |
| `react-native/.env.*.example` | 환경별 설정 예시 |
| `react-native/release/rehearsal-summary.json` | 리허설 검증 결과 artifact |

## 이 프로젝트에서 사용한 도구와 버전

- React Native 0.84.1
- Fastlane (Ruby gem, Gemfile 관리)
- GitHub Actions (Node 22 환경)
- Node.js ESM scripts (`import.meta.url` 기반)
- WatermelonDB ^0.28.0 (realtime-chat 스냅샷에서 상속)
- FlashList ^2.2.0 (상동)
- TypeScript ^5.8.3
- Jest ^29.6.3
