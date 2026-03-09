# 05 — 개발 타임라인: 대시보드 구축 순서

## Phase 1: v1 대시보드 뼈대 (Experiment Console + Catalog CRUD)

### 1-1. React 프로젝트 구성

```bash
# Next.js App Router 앱 안에서 작업 (v0에서 이미 생성된 구조)
cd 08-capstone-submission/v1-ranking-hardening

# shared 패키지 타입 확인
pnpm exec tsc --noEmit -p shared/tsconfig.json

# react 폴더 구조 확인
ls react/components/
```

### 1-2. MpcDashboard 컴포넌트 생성

```bash
# 컴포넌트 파일 생성
touch react/components/mcp-dashboard.tsx

# "use client" 지시어와 import 작성
# CatalogEntry, ExperimentConfig, RecommendationResult를 @study1-v0/shared에서 import
```

작성 순서:
1. `apiFetch<T>()` 유틸 — 모든 API 호출의 기반
2. `buildSampleCatalogEntry()` — catalog 샘플 생성 팩토리
3. 상태 선언 — `useState` 14개
4. `loadAll()` — `Promise.all`로 5개 API 병렬 호출
5. `useEffect` — 마운트 시 `loadAll()` 실행

### 1-3. 추천 실험 섹션 구현

```bash
# API 서버 기동 (별도 터미널)
cd api && pnpm dev

# 브라우저에서 대시보드 확인
cd web && pnpm dev
# http://localhost:3000 접속
```

구현 순서:
1. `runRecommendation("baseline" | "candidate")` 함수
2. query textarea + desiredCapabilities 체크박스 UI
3. Baseline / Candidate 결과 카드 (2열 그리드)
4. 각 candidate 카드에 "채택 로그 남기기" 버튼 → `trackAccept()`

### 1-4. Usage & Compare 섹션

```bash
# usage event가 쌓이는지 확인
curl http://127.0.0.1:3101/api/usage-events | jq '.totals'
# { "impression": 3, "click": 1, "accept": 1, "dismiss": 0 }
```

구현 순서:
1. Usage Totals — impression / click / accept 숫자 카드
2. Compare Snapshot — baselineNdcg3 / candidateNdcg3 / uplift
3. "Compare 갱신" 버튼 → `runEvalAndCompare()`

### 1-5. Feedback Loop 섹션

```bash
# feedback API 확인
curl -X POST http://127.0.0.1:3101/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"id":"test-1","recommendationRunId":"manual","catalogId":"release-check-bot","scoreDelta":2,"noteKo":"테스트","reviewer":"cli","createdAt":"2024-01-01T00:00:00Z"}'
```

구현:
- Catalog select + Score Delta input + Note textarea
- "피드백 저장" 버튼 → `submitFeedback()` → `loadAll()`

### 1-6. Experiment Console 섹션

구현:
1. 실험 생성 폼: name, hypothesis 입력 → `saveExperiment()`
2. 실험 목록: experiments map → name, hypothesis 표시
3. 상태 토글 버튼 → `toggleExperiment()` (running ↔ completed)
4. 삭제 버튼 → `removeExperiment()`

### 1-7. Catalog CRUD 섹션

구현:
1. Selected Catalog select
2. Summary textarea + Freshness input → `saveCatalog()`
3. "샘플 MCP 추가" 버튼 → `createCatalog()`
4. "삭제" 버튼 → `removeCatalog()`

## Phase 2: v2 Release Console 확장

### 2-1. shared 패키지에 v2 타입 추가

```bash
cd 08-capstone-submission/v2-submission-polish

# shared/src/contracts.ts에 새 타입 확인
# ReleaseCandidate, CompatibilityReport, ReleaseGateReport, ArtifactExport
pnpm exec tsc --noEmit -p shared/tsconfig.json
```

### 2-2. 대시보드에 Release Candidate 상태 추가

v1의 `mcp-dashboard.tsx`를 복사해서 v2 버전으로 확장:

```bash
cp ../v1-ranking-hardening/react/components/mcp-dashboard.tsx \
   react/components/mcp-dashboard.tsx
```

추가 상태:
- `releaseCandidates`, `selectedReleaseCandidateId`
- `releaseVersionDraft`, `releaseOwnerDraft`, `releaseNotesDraft`
- `latestCompatibility`, `latestGate`, `latestArtifact`

### 2-3. loadAll() 확장

5개 → 9개 API 병렬 호출로 확장:

```
+ /api/release-candidates
+ /api/compatibility/latest
+ /api/release-gate/latest
+ /api/submission/latest
```

### 2-4. Release Candidate CRUD UI

```bash
# RC 생성 API 확인
curl -X POST http://127.0.0.1:3102/api/release-candidates \
  -H "Content-Type: application/json" \
  -d '{"id":"rc-test","name":"test rc","manifestId":"release-check-bot","previousVersion":"1.0.0","releaseVersion":"1.1.0","targetClientVersion":"1.2.0","releaseNotesKo":"테스트","requiredDocs":[],"requiredArtifacts":[],"deprecatedFieldsUsed":[],"owner":"cli","status":"candidate","createdAt":"2024-01-01T00:00:00Z","updatedAt":"2024-01-01T00:00:00Z"}'
```

구현:
1. `buildSampleReleaseCandidate()` 팩토리 함수
2. RC 목록 select + version/owner/notes 폼
3. 생성/수정/삭제 버튼

### 2-5. Compatibility & Release Gate 버튼

```bash
# compatibility 확인
curl -X POST http://127.0.0.1:3102/api/compatibility/run \
  -H "Content-Type: application/json" \
  -d '{"releaseCandidateId":"rc-release-check-bot-1-5-0"}'

# release gate 확인
curl -X POST http://127.0.0.1:3102/api/release-gate/run \
  -H "Content-Type: application/json" \
  -d '{"releaseCandidateId":"rc-release-check-bot-1-5-0"}'
```

### 2-6. Artifact Export Preview

```bash
# artifact export 확인
curl http://127.0.0.1:3102/api/submission/latest | jq '.latest.format'
# "json"
```

대시보드에서 artifact JSON을 `<pre>` 태그로 표시.

## Phase 3: e2e 테스트

### 3-1. Playwright 설치 및 설정

```bash
cd 08-capstone-submission/v2-submission-polish

# Playwright 설치 (pnpm workspace에서)
pnpm add -D @playwright/test
npx playwright install --with-deps chromium

# playwright.config.ts 확인
cat playwright.config.ts
```

### 3-2. 테스트 작성

```bash
mkdir -p tests/e2e
touch tests/e2e/recommendation.spec.ts
```

테스트 흐름:
1. `page.goto("/")` — 대시보드 접근
2. "MCP 제출 운영 콘솔" heading 확인
3. "Candidate 실행" 클릭 → 한글 설명 텍스트 노출 확인
4. "Release Gate 실행" 클릭 → "Release Quality" heading 확인
5. "Submission Artifact Preview" heading 확인

### 3-3. 테스트 실행

```bash
# API + Web 서버 기동 상태에서
pnpm exec playwright test tests/e2e/recommendation.spec.ts

# headed 모드로 디버깅
pnpm exec playwright test --headed tests/e2e/recommendation.spec.ts

# 실패 시 trace 확인
pnpm exec playwright show-trace test-results/*/trace.zip
```

## Phase 4: 스타일링

```bash
# CSS 파일 확인/수정
ls react/styles/
# globals.css 또는 대시보드 전용 CSS

# CSS 클래스 체계
# .shell → .hero → .grid → .card → .form → .actions
# .stats → .stat (지표 카드)
# .catalog-list → .catalog-row
# .pill (태그), .muted (보조 텍스트)
```

CSS Grid 레이아웃 결정:
- 2열 그리드 (`grid-template-columns: 1fr 1fr`)
- 모바일 대응은 하지 않음 (운영 콘솔은 데스크톱 전용)
- 다크 모드도 미구현 (필요시 CSS 변수로 전환 가능)
