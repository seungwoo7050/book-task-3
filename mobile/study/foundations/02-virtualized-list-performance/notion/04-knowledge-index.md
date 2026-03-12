# 04 — Knowledge Index: 리스트 가상화 빠른 참조

## 소스 파일 맵

| 파일 | 역할 |
|------|------|
| `react-native/App.tsx` | 진입점. VirtualizedListStudyApp 렌더링 |
| `src/listData.ts` | `StudyListItem` 타입, `createDeterministicItems()`, `itemHeightForType()` |
| `src/pagination.ts` | `PaginationState`, `createPaginationState()`, `loadNextPage()`, `isPaginationComplete()` |
| `src/benchmark.ts` | `BenchmarkMetric`, `SAMPLE_BENCHMARK`, `computeBenchmarkSummary()` |
| `src/VirtualizedListStudyApp.tsx` | FlatList/FlashList/Summary 3모드 전환 UI |
| `scripts/benchmark-summary.mjs` | benchmarks/summary.json 생성 Node.js 스크립트 |
| `tests/virtualized-list.test.tsx` | 4개 테스트 (렌더링, 결정적 데이터, pagination, benchmark delta) |

## 데이터 모델

```typescript
type ItemKind = 'text' | 'image' | 'card';

interface StudyListItem {
  id: string;          // `item-${seed}-${index}`
  type: ItemKind;      // index % 3으로 순환
  title: string;
  subtitle: string;    // seed와 sample 값 포함
  imageUrl?: string;   // image type만 존재
  tags: string[];      // group-N, bucket-N
  timestamp: number;
}
```

## Type별 높이

| Type | 높이 (px) |
|------|-----------|
| text | 92 |
| image | 232 |
| card | 156 |

## 벤치마크 지표

| 지표 | FlatList | FlashList | Delta |
|------|----------|-----------|-------|
| FPS | 47 | 58 | +11 |
| Initial render | 222ms | 141ms | -81ms |
| Blank area | 61ms | 18ms | -43ms |
| Peak memory | 188MB | 134MB | -54MB |
| Mount count | 1230 | 472 | -758 |

## 의존성 목록

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `@shopify/flash-list` | ^2.2.0 | FlashList v2 리스트 컴포넌트 |
| `@testing-library/react-native` | ^13.3.3 | 컴포넌트 테스트 |
| `react` | 19.2.3 | UI 프레임워크 |
| `react-native` | 0.84.1 | 모바일 프레임워크 |
| `typescript` | ^5.8.3 | 타입 체크 |
| `jest` | ^29.6.3 | 테스트 러너 |

## Pagination 상태 전이 예시

```
createPaginationState(10000, 50)
→ { cursor: 50, pageSize: 50, total: 10000 }

loadNextPage(...)
→ { cursor: 100, ... }

... (반복)

loadNextPage(...)
→ { cursor: 10000, ... }

isPaginationComplete(...)
→ true
```

## Makefile 타겟

| 타겟 | 동작 |
|------|------|
| `make test` / `make verify` | `script/verify_task.sh` |
| `make app-install` | `npm install` (node_modules 없을 때만) |
| `make app-build` | `npm run typecheck` |
| `make app-test` | `npm test` |
| `make benchmark` | `npm run benchmark` → benchmarks/summary.json |
| `make clean` | node_modules, ios/build, android/build, benchmarks 삭제 |

## npm 스크립트

| 스크립트 | 동작 |
|---------|------|
| `npm test` | Jest 실행 (runInBand) |
| `npm run typecheck` | tsc --noEmit |
| `npm run benchmark` | scripts/benchmark-summary.mjs 실행 |
| `npm run verify` | typecheck + test + benchmark |

## 핵심 개념 문서

| 파일 | 내용 |
|------|------|
| `docs/concepts/flashlist-v2-benchmarking.md` | FlashList v2 벤치마킹 방법론, 합성 지표 사용 이유 |

## 연관 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| navigation | 같은 그룹의 선행 과제. 리스트가 포함된 복잡한 네비게이션 구조 |
| bridge-vs-jsi | 성능 측정 패턴 유사. benchmark + stats 비교 방법론 공유 |
| incident-ops-mobile-client | 캔스톤 앱에서 FlatList + 커서 페이지네이션 패턴을 적용 |
