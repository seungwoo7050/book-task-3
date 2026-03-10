# 04 — Knowledge Index: Bridge vs JSI 빠른 참조

## 소스 파일 맵

| 파일 | 역할 |
|------|------|
| `react-native/App.tsx` | 진입점. BridgeVsJsiStudyApp 렌더링 |
| `src/benchmark.ts` | `BenchmarkRun`, `BenchmarkStats`, `RUNS`, `computeStats()`, `buildExport()` |
| `src/BridgeVsJsiStudyApp.tsx` | 대시보드 UI. RUNS의 통계를 카드로 표시 |
| `scripts/export-results.mjs` | exports/benchmark-results.json 생성 Node.js 스크립트 |
| `tests/bridge-vs-jsi.test.tsx` | 2개 테스트 (통계 계산, export 결정성) |

## 벤치마크 데이터

### Raw Samples

| Surface | payloadSize | samples (ms) |
|---------|-------------|-------------|
| async serialized | 1000 | [42, 45, 44, 47, 43] |
| sync direct-call | 1000 | [11, 10, 12, 10, 11] |

### Computed Stats

| Surface | Mean | Stddev |
|---------|------|--------|
| async serialized | 44.2ms | 1.72ms |
| sync direct-call | 10.8ms | 0.75ms |

### 성능 비율

- sync direct-call은 async serialized보다 약 **4.1배** 빠르다
- 표준편차도 약 **2.3배** 낮아 측정 안정성이 더 높다

## 타입 정의

```typescript
interface BenchmarkRun {
  label: string;
  payloadSize: number;
  samples: number[];
}

interface BenchmarkStats {
  label: string;
  payloadSize: number;
  mean: number;
  stddev: number;
}
```

## 의존성 목록

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `react` | 19.2.3 | UI 프레임워크 |
| `react-native` | 0.84.1 | 모바일 프레임워크 |
| `@testing-library/react-native` | ^13.3.3 | 컴포넌트 테스트 |
| `typescript` | ^5.8.3 | 타입 체크 |
| `jest` | ^29.6.3 | 테스트 러너 |

> 이 프로젝트는 RN 코어 외에 서드파티 의존성이 없다.
> 벤치마크 로직이 순수 TypeScript로 구현되어 있다.

## Makefile 타겟

| 타겟 | 동작 |
|------|------|
| `make test` / `make verify` | `script/verify_task.sh` |
| `make app-install` | `npm install` |
| `make app-build` | `npm run typecheck` |
| `make app-test` | `npm test` |
| `make clean` | node_modules, ios/build, android/build, exports 삭제 |

## npm 스크립트

| 스크립트 | 동작 |
|---------|------|
| `npm test` | Jest 실행 |
| `npm run typecheck` | tsc --noEmit |
| `npm run export-results` | export-results.mjs 실행 → exports/benchmark-results.json |
| `npm run verify` | typecheck + test + export-results |

## Export 결과 형태

```json
{
  "generatedAt": "2026-03-08",
  "results": [
    { "label": "async serialized", "payloadSize": 1000, "mean": 44.2, "stddev": 1.72 },
    { "label": "sync direct-call", "payloadSize": 1000, "mean": 10.8, "stddev": 0.75 }
  ]
}
```

## 핵심 개념 문서

| 파일 | 내용 |
|------|------|
| `docs/concepts/modernized-runtime-benchmark.md` | RN 0.84에서 runtime toggle 대신 surface 비교를 하는 이유 |

## 연관 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| native-modules | 같은 그룹의 후행 과제. JSI 성능 이점을 실제 네이티브 모듈 spec으로 적용 |
| virtualized-list | 벤치마크 패턴 공유. mean/stddev 통계 비교 방법론 |
| incident-ops-mobile-client | 캔스톤 앱에서 JSI 기반 아키텍처를 활용 |
