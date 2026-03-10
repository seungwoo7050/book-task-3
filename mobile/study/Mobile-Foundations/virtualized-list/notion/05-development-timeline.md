# 05 — Development Timeline: 개발 환경·도구 기록

이 문서는 소스 코드만으로는 알 수 없는 CLI 명령, 패키지 설치 순서, 벤치마크 실행 과정을 기록한다.

---

## Step 1: 프로젝트 초기화

```bash
cd study/Mobile-Foundations/virtualized-list/react-native
npm install
```

Node >= 22.11.0 필요.

## Step 2: FlashList 설치

```bash
npm install @shopify/flash-list
```

FlashList v2는 React Native 0.84와 호환된다.
v1에서 v2로의 주요 변경 사항:
- `estimatedItemSize`가 선택적 prop이 됨 (v1에서는 필수)
- cell recycling 알고리즘 개선
- type별 recycling pool 분리 정확도 향상

iOS에서는 pod install이 필요하다:
```bash
cd ios && bundle exec pod install && cd ..
```

## Step 3: 테스트 환경 확인

```bash
# TypeScript 타입 체크
npm run typecheck

# Jest 테스트 실행
npm test

# 둘 다 + 벤치마크까지
npm run verify
```

## Step 4: 벤치마크 스크립트 실행

```bash
# npm 스크립트로 실행
npm run benchmark

# 또는 Makefile 타겟
make benchmark
```

실행 결과:
```
benchmark summary written to benchmarks/summary.json
```

생성된 파일 확인:
```bash
cat benchmarks/summary.json
```

```json
{
  "datasetSize": 10000,
  "pageSize": 50,
  "flatList": { "fps": 47, "initialRenderMs": 222, "blankAreaMs": 61, "peakMemoryMb": 188, "mountCount": 1230 },
  "flashList": { "fps": 58, "initialRenderMs": 141, "blankAreaMs": 18, "peakMemoryMb": 134, "mountCount": 472 }
}
```

## Step 5: 시뮬레이터에서 실행

```bash
# iOS
npm run ios

# Android
npm run android
```

앱 UI에서 세 가지 모드를 전환하며 테스트:
1. **FlatList** 탭 → 스크롤 성능 확인, "다음 50개" 버튼으로 데이터 로딩
2. **FlashList v2** 탭 → 동일 데이터로 스크롤 비교
3. **Benchmark** 탭 → 개선 폭 확인

## Step 6: 디바이스 실측 (선택)

합성 지표 외에 실제 디바이스에서 FPS를 측정하는 방법:

### React Native Performance Monitor
```bash
# 앱 실행 중 시뮬레이터/디바이스에서
# Dev Menu → Performance Monitor 활성화
```

### Flipper (React Native Debugger)
```bash
# Flipper 설치 후 앱 연결
# React DevTools → Performance 탭에서 렌더링 프로파일링
```

### Systrace (Android)
```bash
npx react-native start --reset-cache
# 별도 터미널에서
adb shell perfetto -o /data/misc/perfetto-traces/trace.perfout -t 10s sched freq
```

## Step 7: 검증 파이프라인

```bash
# problem 디렉터리에서 전체 검증
cd ../problem
make test

# 또는 개별 단계
make app-build     # typecheck
make app-test      # jest
make benchmark     # summary.json 생성
```

## 사용된 도구 정리

| 도구 | 버전/용도 |
|------|-----------|
| Node.js | >= 22.11.0 |
| npm | 패키지 관리 |
| @shopify/flash-list | ^2.2.0 — FlashList v2 |
| CocoaPods | iOS native dependency (FlashList native 코드) |
| Metro Bundler | JS 번들링 |
| TypeScript 5.8+ | 타입 체크 (--noEmit) |
| Jest 29.6+ | 테스트 러너 |
| Node.js mjs | benchmark-summary.mjs 스크립트 실행 |

## 트러블슈팅 체크리스트

- [ ] FlashList `estimatedItemSize` 경고 → prop 추가하거나 `getItemType` 설정
- [ ] Cell 깜빡임/잔상 → `getItemType` 미설정 확인
- [ ] `make benchmark` 오류 → `benchmarks/` 디렉터리 쓰기 권한 확인
- [ ] 테스트 실패 → `npm run typecheck` 먼저 실행해 타입 에러 해결
- [ ] Metro 캐시 → `npm start -- --reset-cache`
