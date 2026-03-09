# 지식 인덱스 — Client Onboarding Portal

## 도메인 모델링

### 타입 구조

온보딩 흐름의 핵심 타입들:

- `OnboardingStep = "workspace" | "invites" | "review"` — URL query parameter로 사용되는 step 식별자
- `Session = { userId, name, email }` — 로그인 상태를 나타내는 최소 세션 정보
- `SignInCredentials = { email, password }` — 로그인 입력
- `WorkspaceProfile = { workspaceName, industry, region, teamSize, complianceEmail }` — workspace 설정 5개 필드
- `Invite = { id, email, role, status }` — role은 `"Admin" | "Billing" | "Collaborator"`, status는 항상 `"pending"`
- `InviteInput = { email, role }` — invite 생성 입력 (id와 status는 서버가 할당)
- `ChecklistItem = { id: "profile" | "invite" | "review", label, completed }` — 제출 전 완료 조건
- `OnboardingDraft = { profile, invites }` — 로컬 draft 상태
- `SubmitResult = { submittedAt, workspaceName, inviteCount }` — 제출 성공 응답
- `OnboardingMeta = { failNextSubmit, submittedAt }` — 데모 제어용 메타데이터

## 폼 검증

### Zod 4 스키마

세 가지 스키마가 검증을 담당한다:

- `signInSchema` — `z.email()` + `z.string().min(8)`
- `workspaceProfileSchema` — 5개 필드 모두 `min(2)` 이상, complianceEmail은 `z.email()`
- `inviteInputSchema` — `z.email()` + `z.enum(["Admin", "Billing", "Collaborator"])`

각 스키마에 커스텀 에러 메시지를 설정: `"Enter a valid work email."`, `"Password must be at least 8 characters."` 등.

### zodResolver 연결

React Hook Form에서 `useForm({ resolver: zodResolver(schema) })`로 연결한다. 폼 submit 시 스키마가 자동으로 검증되고, 실패하면 `formState.errors`에 필드별 에러 메시지가 채워진다.

## 상태 관리

### React Query 쿼리 구조

```
["session"]            → getSession()
["workspace-profile"]  → getWorkspaceProfile()   (session 의존)
["invites"]            → listInvites()            (session 의존)
["checklist"]          → listChecklistItems()     (session 의존)
```

`enabled: Boolean(sessionQuery.data)`로 세션이 없으면 나머지 쿼리가 비활성화된다.

### mutation 구조

5개 mutation이 각각 하나의 사용자 액션에 대응:

| mutation | 호출하는 API | 부수 효과 |
|----------|-------------|-----------|
| saveProfileMutation | saveWorkspaceProfile + completeChecklistItem("profile") | saveMessage 표시 |
| addInviteMutation | createInvite + completeChecklistItem("invite") | inviteForm 리셋 |
| completeReviewMutation | completeChecklistItem("review") | — |
| submitMutation | submitOnboarding | submitResult/submitError 설정 |
| signOutMutation | signOut | — |

모든 mutation의 onSuccess에서 `refreshPortalData()` 호출 → 4개 쿼리 invalidate.

### 로컬 상태

- `saveMessage` — 프로필 저장 성공 메시지
- `submitResult` — 제출 성공 결과
- `submitError` — 제출 실패 에러 메시지
- `shouldFailNextSubmit` — "다음 submit 실패" 토글

## 데이터 계층

### storage.ts 구조

localStorage 기반 mock persistence. 5개 storage key:
- session, profile, invites, checklist, meta

`canUseStorage()` 가드로 SSR 안전, `readJson`/`writeJson` 제네릭 헬퍼로 추상화. 세션 삭제 시 `removeItem` 호출.

`resetPortalState()`로 모든 상태를 기본값으로 초기화 가능.

### service.ts 구조

모든 API 함수에 80ms 지연 시뮬레이션(`wait(80)`). submit은 120ms.

`submitOnboarding`의 실패 시뮬레이션:
1. `failNextSubmit` 플래그가 true이면 → 플래그를 false로 리셋 → `createRetryableError` 발생
2. `canSubmitOnboarding` 가드 실패 시 → 일반 Error 발생
3. 통과하면 → `submittedAt` 기록 후 `SubmitResult` 반환

## 라우팅

### App Router 구조

```
app/
├── page.tsx          → SignInPanel (홈/로그인)
├── onboarding/
│   └── page.tsx      → OnboardingRoute (wizard)
├── case-study/
│   └── page.tsx      → 면접용 narrative
├── layout.tsx        → QueryProvider 래핑
└── globals.css       → Tailwind 4 @import
```

### step 관리

`OnboardingRoute`에서 `useSearchParams().get("step")`을 읽고 `coerceStep`으로 보정. step 전환은 `router.replace`로 히스토리를 쌓지 않음.

### route guard

컴포넌트 레벨 guard: `sessionQuery.data`가 없으면 "Sign in before opening" 메시지를 렌더링. 서버 middleware 대신 클라이언트 쿼리 결과로 판단.

## guards 함수

- `coerceStep(value)` — 유효한 step이면 그대로, 아니면 `"workspace"` 반환
- `isWorkspaceReady(profile)` — 5개 필드 모두 `trim()` 후 비어 있지 않은지 확인
- `isChecklistComplete(checklist, id)` — 특정 체크리스트 항목이 완료되었는지 확인
- `canSubmitOnboarding(profile, invites, checklist)` — 프로필 준비 + 초대 1개 이상 + 체크리스트 3개 완료

## UI 아키텍처

### 컴포넌트 구조

```
components/
├── portal/
│   ├── sign-in-panel.tsx            — 로그인/세션 분기
│   ├── onboarding-route.tsx         — URL → step 변환
│   └── client-onboarding-portal.tsx — 메인 wizard (560줄)
└── providers/
    └── query-provider.tsx           — QueryClient 생성
```

내부 유틸 컴포넌트:
- `Field` — label + input + error 래퍼
- `SummaryCard` — title + lines 표시

### step별 UI

- **workspace**: 2×2 그리드(workspaceName, industry, region, teamSize) + 단독 행(complianceEmail) + Save draft 버튼
- **invites**: 3열 그리드(email, role, Add invite) + pending invites 목록
- **review**: workspace/invite SummaryCard 2개 + submit failure 토글 + Mark review complete + Submit onboarding

### 사이드바

Progress 영역: 3개 step 버튼 (현재 step 강조)  
Checklist 영역: profile/invite/review 완료 상태 표시 (✓ 또는 •)

## 테스트 전략

### 단위 테스트 (Vitest)

- `guards.test.ts` — coerceStep 보정, canSubmitOnboarding 조건 조합
- `schemas.test.ts` — signIn/workspaceProfile 유효 입력 통과, 잘못된 이메일 거부
- `storage.test.ts` — draft 저장 후 읽기 일치 확인

### 통합 테스트 (Vitest + Testing Library)

- route guard 표시 (세션 없을 때)
- 전체 흐름: workspace 입력 → save → invite 추가 → review → submit 실패 → retry 성공

### E2E 테스트 (Playwright)

- 직접 URL 접근 시 guard → sign-in 복귀
- 전체 journey: sign-in → validation 에러 → 수정 → save → 새로고침 draft restore → invite → review → submit 실패 → retry 성공

## 디자인 시스템

- 색상: stone 팔레트 (950 primary, 600 body, 500 label, 200 border)
- 카드: rounded-[2rem] / rounded-[1.8rem], 깊은 그림자
- 라벨: font-mono text-xs uppercase tracking-[0.28em]
- 버튼: rounded-full, primary(bg-stone-950) / secondary(border border-stone-300)
- 폰트: Manrope(본문), IBM Plex Mono(라벨/코드), @fontsource 셀프호스팅
