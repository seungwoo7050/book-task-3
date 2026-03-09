# 개발 타임라인 — Client Onboarding Portal

## Phase 0: 프로젝트 초기화

```bash
# Next.js 16 프로젝트 생성
npx create-next-app@latest 02-client-onboarding-portal \
  --typescript --tailwind --eslint --app --src-dir \
  --import-alias "@/*"

cd 02-client-onboarding-portal
```

### 폰트 설치

```bash
npm install @fontsource/manrope @fontsource/ibm-plex-mono
```

`app/layout.tsx`에서 각 weight별로 import:
```typescript
import "@fontsource/manrope/400.css";
import "@fontsource/manrope/500.css";
import "@fontsource/manrope/600.css";
import "@fontsource/manrope/700.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
```

### 핵심 의존성 설치

```bash
# 폼 관리
npm install react-hook-form@^7.66.0
npm install @hookform/resolvers@^5.2.2

# 서버 상태
npm install @tanstack/react-query@^5.90.21

# 검증
npm install zod@^4.3.6
```

### 테스트 도구 설치

```bash
# 단위 + 통합 테스트
npm install -D vitest@^4.0.18
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D @vitejs/plugin-react
npm install -D jsdom@^28.1.0

# E2E 테스트
npm install -D @playwright/test@^1.58.2
npx playwright install chromium
```

### Tailwind CSS 4 설정

```bash
npm install -D tailwindcss@^4.2.1 @tailwindcss/postcss@^4.2.1
```

`postcss.config.mjs`에서 `@tailwindcss/postcss` 플러그인 설정. `globals.css`에서 `@import "tailwindcss"` 구문.

---

## Phase 1: 도메인 모델과 데이터 계층

### types.ts 작성

OnboardingStep, Session, WorkspaceProfile, Invite, ChecklistItem 등 10개 타입 정의.

### storage.ts 작성

localStorage 기반 mock persistence. 5개 storage key, read/write 함수 쌍, `resetPortalState()`.

```bash
# SSR 환경에서 테스트
npm run build && npm start
# → canUseStorage() 가드 확인
```

### schemas.ts 작성

Zod 4로 signInSchema, workspaceProfileSchema, inviteInputSchema 정의.

### guards.ts 작성

`coerceStep`, `isWorkspaceReady`, `canSubmitOnboarding` 가드 함수.

### service.ts 작성

10개 mock API 함수. 80ms 지연 시뮬레이션. submit 전용 `failNextSubmit` 플래그.

---

## Phase 2: React Query + 폼 훅

### query-provider.tsx 작성

QueryClient를 useState로 생성해 SSR에서 매 렌더마다 새 클라이언트가 만들어지는 것을 방지.

```typescript
const [queryClient] = useState(() => new QueryClient({
  defaultOptions: { queries: { staleTime: 0, retry: false } },
}));
```

### 폼/쿼리 훅 설계

React Hook Form 2개(`workspaceForm`, `inviteForm`)와 React Query 쿼리 4개, mutation 5개를 `ClientOnboardingPortal` 안에서 직접 사용.

```bash
npm run dev
# localhost:3000에서 쿼리 훅 동작 확인
```

---

## Phase 3: UI 구현

### SignInPanel

sign-in-panel.tsx — 세션 유무에 따른 분기 렌더링. 기본값으로 데모 이메일/비밀번호 포함.

### OnboardingRoute

onboarding-route.tsx — `useSearchParams`로 step 읽기, `router.replace`로 step 전환.

### ClientOnboardingPortal

client-onboarding-portal.tsx — 메인 wizard 컴포넌트 약 560줄.
- 세션 가드 (loading → guard → content)
- 좌측 sidebar (progress + checklist)
- step별 content (workspace form / invite form + list / review summary + submit)

### 내부 컴포넌트

- `Field` — label + input + error 래퍼
- `SummaryCard` — review step의 workspace/invite 요약

---

## Phase 4: 단위 테스트

```bash
npx vitest run tests/unit/guards.test.ts
# coerceStep 보정, canSubmitOnboarding 조건 조합 → 통과

npx vitest run tests/unit/schemas.test.ts
# signIn/workspaceProfile 유효 입력 통과, 잘못된 이메일 거부 → 통과

npx vitest run tests/unit/storage.test.ts
# draft 저장 후 읽기 일치 → 통과
```

---

## Phase 5: 통합 테스트

```bash
npx vitest run tests/integration/client-onboarding-portal.test.tsx
```

2개 테스트:
1. 세션 없을 때 route guard 표시
2. 전체 onboarding 흐름: workspace 입력 → save → invite 추가 → review → submit 실패 → retry 성공

QueryClientProvider + useState wrapper를 테스트 헬퍼(`renderPortal`)로 추출. `signIn`을 직접 호출해 세션을 미리 설정한 뒤 테스트.

---

## Phase 6: E2E 테스트

```bash
# Playwright 설정
# playwright.config.ts → webServer: npm run dev, baseURL: localhost:3000

npx playwright test tests/e2e/client-onboarding.spec.ts
```

2개 시나리오:
1. 직접 `/onboarding?step=review` 접근 → guard 표시 → sign-in으로 복귀
2. 전체 journey: sign-in → validation 에러(잘못된 compliance email) → 수정 → save → reload draft restore → invite → review → submit 실패 → retry 성공

---

## Phase 7: 문서화

### docs/ 구조

```
docs/
├── concepts/
│   ├── information-architecture.md  — 2 route, 3 step 구조
│   └── validation-and-draft-flow.md — validation, draft save, submit retry 설계
├── references/
│   └── quality-bar.md               — 검증 범위와 목표
└── presentation.md                  — 6-8분 데모 흐름, 발표 포인트
```

### README.md 작성

프로젝트 개요, prerequisite, 구조, build/test 명령어, 검증 범위.

---

## 주요 도구 버전

| 도구 | 버전 |
|------|------|
| Node.js | 22.x (LTS) |
| Next.js | ^16.1.6 |
| React | ^19.2.4 |
| TypeScript | ^5.9.3 |
| React Hook Form | ^7.66.0 |
| @hookform/resolvers | ^5.2.2 |
| TanStack React Query | ^5.90.21 |
| Zod | ^4.3.6 |
| Tailwind CSS | ^4.2.1 |
| Manrope / IBM Plex Mono | @fontsource|
| Vitest | ^4.0.18 |
| Testing Library | 최신 |
| Playwright | ^1.58.2 |

## 개발 명령어 요약

```bash
npm run dev          # Next.js 개발 서버
npm run build        # 프로덕션 빌드
npm run start        # 프로덕션 서버
npm run typecheck    # tsc --noEmit
npm run test         # Vitest 단위/통합 테스트
npm run e2e          # Playwright E2E 테스트
npm run verify       # typecheck + test + e2e
```
