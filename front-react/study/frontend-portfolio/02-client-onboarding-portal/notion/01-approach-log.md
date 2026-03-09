# 접근 과정 — Client Onboarding Portal 구현 기록

## 도메인 모델: 온보딩에 필요한 타입들

types.ts에서 온보딩 흐름에 필요한 모든 타입을 정의했다. FP 01의 Issue처럼 필드가 많지는 않지만, 각 타입이 하나의 step이나 기능에 대응하는 구조다.

`OnboardingStep`은 `"workspace" | "invites" | "review"` 리터럴 유니온이다. URL의 `?step=` 파라미터와 1:1로 대응한다.

`Session`은 `{ userId, name, email }` 세 필드뿐이다. 실제 인증 토큰이나 만료 시간은 없다. mock이므로, 세션이 "있느냐 없느냐"만 중요하다.

`WorkspaceProfile`은 5개 필드: workspaceName, industry, region, teamSize, complianceEmail. 모두 string이다. 각 필드의 제약 조건은 Zod 스키마에서 정의한다.

`Invite`는 `{ id, email, role, status }` 구조다. role은 `"Admin" | "Billing" | "Collaborator"` 유니온, status는 항상 `"pending"`이다. 실제 초대 수락/거절 흐름은 범위 밖이므로 status가 변하지 않는다.

`ChecklistItem`은 `{ id, label, completed }` 구조다. id는 `"profile" | "invite" | "review"` 세 값 중 하나다. 각 step에서 핵심 동작을 수행하면 해당 체크리스트 항목이 완료된다.

`OnboardingDraft`는 `{ profile, invites }`를 묶은 타입이고, `SubmitResult`는 제출 성공 후 반환되는 `{ submittedAt, workspaceName, inviteCount }`다.

`OnboardingMeta`는 `{ failNextSubmit, submittedAt }` — 데모 제어용 플래그와 제출 기록이다.

## 스키마: Zod 4와 React Hook Form의 연결

schemas.ts에서 세 개의 Zod 스키마를 정의했다.

`signInSchema`는 이메일 형식(`z.email`)과 비밀번호 최소 8자를 검증한다. 커스텀 에러 메시지를 각 필드에 직접 넣었다.

`workspaceProfileSchema`는 5개 필드 모두에 `min(2)` 이상의 제약을 건다. complianceEmail은 `z.email()`로 형식까지 확인한다.

`inviteInputSchema`는 이메일 형식과 role enum을 검증한다.

세 스키마 모두에서 `z.infer<typeof schema>`로 타입을 추출했다. FP 01에서는 타입과 스키마를 분리했지만, 이 프로젝트에서는 타입이 단순하므로 Zod에서 추출하는 방식을 택했다.

React Hook Form에서는 `zodResolver(schema)`를 resolver로 전달한다. 사용자가 submit 버튼을 누르면, 먼저 Zod가 검증하고 실패하면 `formState.errors`에 에러 메시지가 채워진다. 통과하면 `handleSubmit`의 콜백이 호출된다.

## storage: localStorage 기반 mock persistence

storage.ts는 FP 01과 같은 패턴을 따른다. `canUseStorage()` 가드로 SSR 안전성을 확보하고, `readJson`/`writeJson` 헬퍼로 localStorage를 추상화했다.

5개의 storage key를 사용한다:
- `front-react:onboarding:session` — 현재 세션
- `front-react:onboarding:profile` — workspace 프로필 draft
- `front-react:onboarding:invites` — 초대 목록
- `front-react:onboarding:checklist` — 체크리스트 상태
- `front-react:onboarding:meta` — 데모 제어 메타데이터

각 key에 대해 read/write 함수 쌍을 제공하고, `resetPortalState()`로 모든 상태를 초기화할 수 있다.

특이한 점은 session을 null로 write하면 `removeItem`을 호출한다는 것이다. sign-out 시 세션 키 자체를 삭제해서, 다음 읽기에서 자연스럽게 null이 반환되게 했다.

## guards: step 보정과 제출 가드

guards.ts에는 세 가지 가드 함수가 있다.

`coerceStep`은 URL의 step 파라미터를 받아 유효한 `OnboardingStep`으로 보정한다. `"workspace"`, `"invites"`, `"review"` 외의 값이 들어오면 `"workspace"`로 떨어진다.

`isWorkspaceReady`는 프로필의 5개 필드가 모두 비어 있지 않은지 확인한다. `trim()`으로 공백만 넣은 경우도 걸러낸다.

`canSubmitOnboarding`은 세 가지 조건을 AND로 결합한다: 프로필이 준비되었고, 초대가 1개 이상 있고, 체크리스트 3개 항목이 모두 완료되었을 때만 true를 반환한다. 이 함수의 반환값이 submit 버튼의 disabled 상태를 결정한다.

## service: mock API 계층

service.ts는 FP 01의 service.ts와 구조가 비슷하지만, 카오스 엔지니어링 레이어(simulate.ts)가 없다. 대신 submit 전용으로 "다음 한 번 실패" 플래그(`failNextSubmit`)를 사용한다.

모든 API 함수는 `wait(80)` 으로 80ms 지연을 시뮬레이션한다. 이렇게 하면 React Query의 pending/success 상태 전환이 눈에 보인다.

`signIn`은 이메일에서 `@` 앞부분을 추출해 name을 만든다. 어떤 이메일이든 "성공"하므로 데모에서 자유롭게 이메일을 바꿔 볼 수 있다.

`saveWorkspaceProfile`은 현재 프로필에 patch를 merge한 뒤 `workspaceProfileSchema.parse`로 검증한다. 검증이 통과하면 storage에 저장하고 체크리스트의 "profile" 항목을 완료 처리한다.

`createInvite`는 `inviteInputSchema.parse`로 검증한 뒤 랜덤 ID를 생성해 invite를 추가한다. 동시에 체크리스트의 "invite" 항목을 완료 처리한다.

`submitOnboarding`은 지연을 120ms로 더 길게 준다. `failNextSubmit` 플래그가 true이면 플래그를 false로 리셋하고 `createRetryableError`를 던진다. 정상이면 `canSubmitOnboarding` 가드를 검사하고, 통과하면 `submittedAt` 타임스탬프를 기록한다.

## 라우팅: App Router와 query parameter

Next.js App Router의 구조:
- `app/page.tsx` → `<SignInPanel />`
- `app/onboarding/page.tsx` → `<OnboardingRoute />`
- `app/case-study/page.tsx` → 면접용 narrative 페이지
- `app/layout.tsx` → `<QueryProvider>` 래핑

`OnboardingRoute`는 `useSearchParams`로 `?step=` 값을 읽고, `coerceStep`으로 보정한 뒤 `<ClientOnboardingPortal>`에 전달한다. step 변경 시 `router.replace`로 URL을 갱신한다. `push`가 아닌 `replace`를 쓰는 이유는 step 전환마다 히스토리가 쌓이면 뒤로가기가 불편해지기 때문이다.

## SignInPanel: 세션에 따른 분기 렌더링

sign-in-panel.tsx는 두 가지 모드를 가진다:
- **세션이 없을 때**: 이메일/비밀번호 폼을 보여 준다. submit하면 `signIn` mutation이 호출되고, 성공 시 `/onboarding?step=workspace`로 이동한다.
- **세션이 있을 때**: 현재 세션 정보와 "Continue onboarding", "Sign out" 버튼을 보여 준다.

기본값으로 `owner@latticecloud.dev` / `launch-ready`가 미리 채워져 있어, 데모에서 바로 로그인할 수 있다.

## ClientOnboardingPortal: 핵심 wizard 컴포넌트

client-onboarding-portal.tsx는 약 560줄의 "use client" 컴포넌트다. props로 `step`과 `onStepChange`를 받아 controlled component 패턴을 따른다.

### 세션 가드

가장 먼저 `sessionQuery`를 확인한다. 로딩 중이면 "Loading session..."을, 세션이 없으면 route guard 메시지를 보여 준다. 세션이 있을 때만 onboarding 콘텐츠를 렌더링한다.

### React Query 쿼리 4개

```typescript
sessionQuery  → getSession()
profileQuery  → getWorkspaceProfile()  (session 있을 때만)
invitesQuery  → listInvites()          (session 있을 때만)
checklistQuery → listChecklistItems()  (session 있을 때만)
```

`enabled: Boolean(sessionQuery.data)`로 세션이 없으면 나머지 쿼리가 실행되지 않는다.

### React Hook Form 2개

`workspaceForm`은 workspace step에서 프로필 입력에 사용하고, `inviteForm`은 invite step에서 초대 추가에 사용한다. 각각 Zod resolver가 연결되어 있다.

### mutation 5개

1. `saveProfileMutation` — 프로필 저장 + checklist "profile" 완료
2. `addInviteMutation` — 초대 생성 + checklist "invite" 완료 + 폼 리셋
3. `completeReviewMutation` — checklist "review" 완료
4. `submitMutation` — 온보딩 제출 (실패 시 에러 메시지, 성공 시 결과 표시)
5. `signOutMutation` — 세션 삭제

모든 mutation의 onSuccess에서 `refreshPortalData()`를 호출해 4개 쿼리를 모두 invalidate한다.

### step 별 렌더링

조건부 렌더링으로 step에 따라 다른 섹션을 보여 준다:
- **workspace**: 5개 필드 폼 + Save draft 버튼
- **invites**: 초대 추가 폼 + pending invites 목록
- **review**: 요약 카드 2개(workspace/invite) + 체크리스트 + submit 버튼 + 실패 시뮬레이션 토글

### 좌측 sidebar

Progress 영역에 세 step 버튼이 있다. 현재 step은 `bg-stone-950 text-white`로 강조된다. 아래에 Checklist가 표시되어 완료 상태를 실시간으로 보여 준다.

## UI 디자인 특징

이 프로젝트는 FP 01과 달리 Radix UI 래퍼를 사용하지 않는다. 네이티브 HTML 요소(`<input>`, `<select>`, `<button>`)에 Tailwind 클래스를 직접 적용했다. 이유는 온보딩 폼이 복잡한 인터랙션(dropdown, tooltip, popover 등)을 필요로 하지 않기 때문이다.

디자인 시스템은 `stone` 팔레트 기반이다. rounded-2xl/rounded-[2rem] 카드, `font-mono text-xs uppercase tracking-[0.28em]` 라벨, `shadow-[0_30px_80px_-60px_...]` 깊은 그림자로 일관된 톤을 유지한다.

폰트는 Manrope(본문)와 IBM Plex Mono(라벨/코드)를 `@fontsource/`로 설치해 셀프호스팅한다.
