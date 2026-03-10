# 05 — Development Timeline: 개발 환경·도구 기록

이 문서는 소스 코드만으로는 알 수 없는 CLI 명령, 환경 설정, export 스크립트 실행 과정을 기록한다.

---

## Step 1: 프로젝트 초기화

```bash
cd study/React-Native-Architecture/bridge-vs-jsi/react-native
npm install
```

이 프로젝트는 RN 코어 외에 서드파티 의존성이 없다.
`npm install`만으로 환경 준비가 완료된다.

## Step 2: 타입 체크 및 테스트

```bash
# TypeScript 타입 체크
npm run typecheck

# Jest 테스트 실행
npm test

# 전체 검증 (typecheck + test + export)
npm run verify
```

테스트는 두 개만 존재한다:
1. `computeStats()` 결과의 mean이 stddev보다 큰지 확인
2. `buildExport()` 결과가 결정적인 JSON shape과 정확히 일치하는지 확인

## Step 3: Export 스크립트 실행

```bash
# 벤치마크 결과를 JSON으로 내보내기
npm run export-results
```

실행 결과:
```
benchmark results written to exports/benchmark-results.json
```

파일 확인:
```bash
cat exports/benchmark-results.json
```

## Step 4: 시뮬레이터 실행

```bash
# iOS
npm run ios

# Android
npm run android
```

앱은 단일 화면으로, 두 개의 카드에 async serialized와 sync direct-call의 통계를 보여준다.
interactive 요소가 없으므로 화면이 표시되면 확인 완료다.

## Step 5: 검증 파이프라인

```bash
# problem 디렉터리에서 전체 검증
cd ../problem
make test

# 개별 단계
make app-build     # typecheck
make app-test      # jest
```

## 실제 벤치마크 측정 방법 (참고)

이 프로젝트의 합성 데이터 대신 실제 측정을 하고 싶다면:

### TurboModule 활용
```bash
# RN 0.84에서 TurboModule spec 생성
npx react-native codegen

# iOS 빌드
cd ios && bundle exec pod install && cd ..
npm run ios
```

### performance.now() 측정 예시
```typescript
const start = performance.now();
await nativeModule.asyncMethod(payload);
const elapsed = performance.now() - start;
```

### Hermes Profiler
```bash
# Hermes sampling profiler로 JS 실행 프로파일링
# Dev Menu → Settings → Hermes Profile 활성화
# 프로파일 데이터를 chrome://tracing에서 분석
```

## 사용된 도구 정리

| 도구 | 버전/용도 |
|------|-----------|
| Node.js | >= 22.11.0 (package.json engines에는 미지정, 저장소 공통 기준) |
| npm | 패키지 관리 |
| TypeScript 5.8+ | 타입 체크 (--noEmit) |
| Jest 29.6+ | 테스트 러너 |
| Node.js mjs | export-results.mjs 스크립트 실행 |
| Metro Bundler | JS 번들링 |

## 트러블슈팅 체크리스트

- [ ] `toFixed()` 반환값이 string → `Number()`로 감싸기
- [ ] Export JSON이 앱 수치와 다름 → `export-results.mjs`의 하드코딩 값 확인
- [ ] 테스트에서 `toEqual` 실패 → `generatedAt` 고정 문자열 여부 확인
- [ ] Metro 캐시 → `npm start -- --reset-cache`
