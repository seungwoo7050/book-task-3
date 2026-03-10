# 04 — 지식 인덱스: 대시보드 핵심 개념 정리

## MPC Dashboard 컴포넌트 구조

### v1 섹션

| 섹션 | 위치 | API 의존 |
|------|------|----------|
| Hero | 최상단 | 없음 (정적 텍스트) |
| 추천 실험 | 좌측 상단 | POST `/api/recommendations`, POST `/api/recommendations/candidate` |
| Usage Totals | 우측 상단 | GET `/api/usage-events` |
| Compare Snapshot | 우측 중단 | GET `/api/compare/latest`, POST `/api/compare/run` |
| Feedback Loop | 우측 하단 | POST `/api/feedback` |
| Experiment Console | 좌측 하단 | GET/POST/PUT/DELETE `/api/experiments` |
| Catalog CRUD | 우측 하단 | GET/POST/PUT/DELETE `/api/catalog` |

### v2 추가 섹션

| 섹션 | API 의존 |
|------|----------|
| Release Candidate CRUD | GET/POST/PUT/DELETE `/api/release-candidates` |
| Compatibility | GET `/api/compatibility/latest`, POST `/api/compatibility/run` |
| Release Gate | GET `/api/release-gate/latest`, POST `/api/release-gate/run` |
| Artifact Preview | GET `/api/submission/latest`, POST `/api/submission/export` |

## 핵심 타입

### EvalSummary

```typescript
type EvalSummary = {
  id: string;
  metrics: {
    top3Recall: number;           // golden set에서 top-3 안에 정답이 들어간 비율
    explanationCompleteness: number;  // 설명 완성도
    forbiddenHitRate: number;     // 금지된 도구가 추천에 포함된 비율 (낮을수록 좋음)
  };
};
```

### CompareSummary

```typescript
type CompareSummary = {
  id: string;
  metrics: {
    baselineNdcg3: number;        // baseline 전략의 nDCG@3
    candidateNdcg3: number;       // candidate 전략의 nDCG@3
    uplift: number;               // candidate - baseline 개선폭
    baselineTop1HitRate: number;  // baseline top-1 정답률
    candidateTop1HitRate: number; // candidate top-1 정답률
  };
};
```

### UsageSummary

```typescript
type UsageSummary = {
  items: Array<{ catalogId: string; action: string }>;
  totals: { impression: number; click: number; accept: number; dismiss: number };
};
```

## buildSampleCatalogEntry 패턴

seed 데이터를 복제해서 새 엔트리를 만드는 팩토리 함수:

```typescript
function buildSampleCatalogEntry(seed: CatalogEntry, id: string): CatalogEntry {
  return {
    ...seed,
    id,
    slug: id,
    name: `Signal ${seed.name}`,
    version: "1.0.0",
    summaryKo: `${seed.summaryKo} signal-rerank 실험용 변형 엔트리`,
    // ... exposure 등 한국어 필드 수정
  };
}
```

- `id`와 `slug`를 새로 지정
- `summaryKo`, `descriptionKo`에 실험 목적 태그를 추가
- 나머지 필드(capabilities, compatibility, exposure 등)는 seed에서 상속

## loadAll() 호출 시점

| 동작 | loadAll 호출 |
|------|-------------|
| 페이지 마운트 (`useEffect`) | ✅ |
| Catalog 저장/추가/삭제 | ✅ |
| Experiment 생성/토글/삭제 | ✅ |
| Feedback 저장 | ✅ |
| Usage event 기록 (채택 로그) | ✅ |
| Release Candidate 생성/수정/삭제 (v2) | ✅ |
| Compatibility/Release Gate 실행 (v2) | ✅ |
| 추천 실행 (baseline/candidate) | ❌ (결과만 로컬 상태에 저장) |

추천 실행은 `loadAll()`을 호출하지 않는다.  
추천 결과는 서버에 저장되는 것이 아니라 응답으로 돌아오는 것이므로 로컬 상태에만 넣으면 된다.

## e2e 테스트 접근법

### Playwright 테스트 구조

```
test("runs candidate recommendation and release gate flow")
  1. page.goto("/") — 대시보드 접근
  2. heading 확인 — "MCP 제출 운영 콘솔" (v2 기준)
  3. Candidate 실행 → 결과 텍스트 확인
  4. Release Gate 실행 → "Release Quality" heading 확인
  5. "Submission Artifact Preview" heading 확인
```

### 왜 getByRole을 쓰는가

- `data-testid`보다 semantic한 접근: 실제 접근성 트리 기반
- 한글 heading 텍스트가 바뀌면 테스트도 자동으로 실패 → 의도적인 coupling

## CSS Grid 레이아웃 클래스

| 클래스 | 역할 |
|--------|------|
| `.shell` | 전체 래퍼 (max-width, padding) |
| `.hero` | 상단 소개 영역 |
| `.hero-card` | 소개 카드 (pill 태그 포함) |
| `.grid` | 2열 그리드 컨테이너 |
| `.card` | 개별 섹션 카드 |
| `.form` | 폼 요소 그룹 |
| `.actions` | 버튼 그룹 (flex) |
| `.stats` | 지표 표시 그리드 |
| `.stat` | 개별 지표 카드 |
| `.catalog-list` | 목록 컨테이너 |
| `.catalog-row` | 목록 행 |
| `.pill` | 태그/배지 |
| `.muted` | 보조 텍스트 |
