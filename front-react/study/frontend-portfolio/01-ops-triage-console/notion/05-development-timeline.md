# 개발 타임라인 — Ops Triage Console

## Phase 0: 프로젝트 초기화

```bash
# Next.js 16 프로젝트 생성
npx create-next-app@latest 01-ops-triage-console \
  --typescript --tailwind --eslint --app --src-dir \
  --import-alias "@/*"

cd 01-ops-triage-console
```

### Tailwind CSS 4 설정

Next.js의 기본 Tailwind 설정 위에 Tailwind CSS 4를 적용했다. `postcss.config.mjs`에서 `@tailwindcss/postcss` 플러그인을 사용하고, `globals.css`에서 `@import "tailwindcss"` 구문으로 변경했다.

### 핵심 의존성 설치

```bash
# TanStack (서버 상태 + 테이블)
npm install @tanstack/react-query@^5.90.21
npm install @tanstack/react-table@^8.21.3

# Radix UI primitives
npm install @radix-ui/react-checkbox
npm install @radix-ui/react-dialog
npm install @radix-ui/react-popover
npm install @radix-ui/react-select
npm install @radix-ui/react-tooltip

# 유틸리티
npm install zod@^4.0.0
npm install clsx tailwind-merge
```

### 테스트 도구 설치

```bash
# 단위 + 통합 테스트
npm install -D vitest@^4.0.18
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D @vitejs/plugin-react
npm install -D jsdom

# E2E 테스트
npm install -D @playwright/test@^1.58.2
npx playwright install chromium
```

### TypeScript, ESLint 설정

`tsconfig.json`에서 `"strict": true`, `"noUncheckedIndexedAccess": true`를 활성화했다. Next.js의 기본 ESLint 설정을 유지하면서 `next lint`로 검증한다.

---

## Phase 1: 도메인 모델과 데이터 계층

### types.ts 작성

Issue, IssueQuery, IssuePatch, BulkIssuePatch, SavedView, DashboardSummary, DemoRuntimeConfig, IssueActivity 타입을 정의했다. 리터럴 유니온 타입 6개로 도메인 어휘를 잡았다.

### constants.ts 작성

초기 이슈 데이터 30건, saved view 프리셋, 기본 query, 기본 runtime config를 하드코딩했다. 데이터를 코드에 포함시켜 외부 의존성 없이 동작하도록 했다.

### storage.ts 작성

```bash
# SSR 환경에서 테스트
npm run build && npm start
# → window is not defined 에러 → canUseStorage() 가드 추가
```

localStorage와 memory 듀얼 스토리지를 구현했다. `readIssues()`, `writeIssues()`, `resetIssues()`가 핵심 함수다.

### service.ts / simulate.ts 작성

mock API 함수와 카오스 엔지니어링 유틸리티를 분리했다. `simulateRequest`가 모든 API 호출을 감싸서 지연과 실패를 주입한다.

### query.ts 작성

순수 함수 `applyIssueQuery`와 `createDashboardSummary`를 작성했다. 이 시점에서 첫 번째 단위 테스트를 작성했다.

```bash
npx vitest run src/lib/__tests__/query.test.ts
# 6개 필터 조합 × 4개 정렬 → 전체 통과
```

### optimistic.ts 작성

`applyIssuePatch`와 `applyBulkPatch`를 순수 함수로 구현하고 테스트했다.

```bash
npx vitest run src/lib/__tests__/optimistic.test.ts
# 원본 불변성, activity 추가, 다중 필드 변경 → 전체 통과
```

### schemas.ts 작성

Zod 4로 issuePatchSchema, bulkIssuePatchSchema, noteSchema를 정의했다.

---

## Phase 2: React Query 훅

### use-ops-triage.ts 작성

`useIssueList`, `useIssueDetail`, `useDashboardSummary`, `useSavedViews` 쿼리 훅과 `useIssueMutation`, `useBulkIssueMutation`, `useResetDemoMutation` 뮤테이션 훅을 작성했다.

```bash
# QueryClientProvider 설정 후 개발 서버 확인
npm run dev
# → localhost:3000에서 query 훅 동작 확인
```

낙관적 업데이트의 onMutate/onError/onSuccess 패턴을 단건/다건에 일관되게 적용했다.

---

## Phase 3: UI 컴포넌트

### Radix 래퍼 컴포넌트 (11개)

```
src/components/ui/
├── badge.tsx
├── button.tsx
├── card.tsx
├── checkbox.tsx
├── dialog.tsx
├── input.tsx
├── popover.tsx
├── select.tsx
├── textarea.tsx
├── toast.tsx
└── tooltip.tsx
```

각 래퍼에서 `clsx`와 `tailwind-merge`로 className을 병합한다. `React.forwardRef`와 `ComponentPropsWithoutRef`로 타입 안전한 ref 전달을 설정했다.

### OpsTriageConsole 메인 컴포넌트

7개 useState, TanStack Table with 8 columns, useDeferredValue 적용. 약 250줄의 "use client" 컴포넌트다.

### IssueDetailDialog

이슈 상세 표시 + 인라인 수정. Dialog open 시 `useIssueDetail(selectedIssueId)`로 데이터를 가져온다.

### RuntimeControls

카오스 엔지니어링 설정 패널. Popover 안에 sliders와 select를 배치했다.

---

## Phase 4: 통합 테스트

```bash
# 통합 테스트 작성 후 실행
npx vitest run tests/integration/ops-triage-console.test.tsx

# QueryClientProvider + renderHook 조합으로 React Query 상태 흐름 검증
# 4개 테스트: query 변경, mutation 동기화, bulk mutation, rollback+retry
```

Testing Library의 `screen.getByRole`, `userEvent.click`, `waitFor`를 활용했다. React Query의 `queryClient`를 테스트마다 새로 생성해 캐시 격리를 보장했다.

---

## Phase 5: E2E 테스트

```bash
# Playwright 설정
npx playwright install chromium

# playwright.config.ts 설정
# → webServer: npm run dev, baseURL: localhost:3000
```

```bash
npx playwright test tests/e2e/ops-triage.spec.ts
```

4개 시나리오:
1. 이슈 상세 열기 → status 변경 → Undo 클릭 → 원래 status 확인
2. saved view 적용 → 다수 선택 → bulk update → 결과 확인
3. failure rate 100% 설정 → mutation → 에러 toast → Retry 클릭
4. Tab/Enter/Escape만으로 이슈 열기 → 수정 → 닫기

---

## Phase 6: 문서화

### docs/ 구조

```
docs/
├── concepts/
│   ├── positioning.md      # 왜 이 프로젝트인가
│   └── ux-and-state-flow.md # UX 흐름과 상태 전이 다이어그램
├── references/
│   └── quality-bar.md       # 테스트 커버리지 목표, 성능 기준
└── presentation.md          # 8개 섹션 면접 프레젠테이션 가이드
```

### README.md 작성

프로젝트 개요, 기술 스택, 로컬 실행 방법, 테스트 실행 방법, 아키텍처 다이어그램을 포함했다.

---

## 주요 도구 버전

| 도구 | 버전 |
|------|------|
| Node.js | 22.x (LTS) |
| Next.js | 16 |
| React | 19 |
| TypeScript | 5.x |
| TanStack React Query | ^5.90.21 |
| TanStack React Table | ^8.21.3 |
| Radix UI | 각 패키지 최신 |
| Zod | 4.x |
| Tailwind CSS | 4.x |
| Vitest | ^4.0.18 |
| Playwright | ^1.58.2 |
| Testing Library | 최신 |

## 개발 명령어 요약

```bash
npm run dev          # Next.js 개발 서버 (localhost:3000)
npm run build        # 프로덕션 빌드
npm run start        # 프로덕션 서버
npm run lint         # ESLint
npx vitest run       # 단위 + 통합 테스트
npx playwright test  # E2E 테스트
```
