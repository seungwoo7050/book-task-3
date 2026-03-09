# 지식 인덱스 — Ops Triage Console

## 도메인 모델링

### Issue 타입 설계

18개 필드를 가진 `Issue` 인터페이스가 프로젝트의 중심이다. 리터럴 유니온 타입으로 `IssueStatus`(5종), `IssuePriority`(4종), `IssueSource`(4종), `SlaRisk`(3종), `IssueLabel`(6종), `TeamRoute`(5종)을 정의했다. 각 유니온은 string 서브타입이므로 자동 완성이 되고, 타입 가드 없이 switch/case로 분기할 수 있다.

### IssueQuery — 필터/정렬/페이지의 단일 객체화

여섯 개의 필터 조건(status, priority, source, team, risk, search)과 정렬, 페이지를 하나의 `IssueQuery` 객체로 묶었다. 이 객체가 React Query의 queryKey에 들어가므로, 필터가 바뀌면 새로운 캐시 엔트리가 생긴다. 검색어를 타이핑할 때마다 새 key가 만들어지는 문제는 `useDeferredValue`로 해결했다.

### IssuePatch / BulkIssuePatch

`Partial<Pick<Issue, "status" | "priority" | "team" | "labels" | "note">>`로 변경 가능한 필드만 노출한다. Bulk은 `{ issueIds: string[], patch: IssuePatch }` 형태다. patch가 단건/다건에서 동일하므로 `applyIssuePatch` 함수를 공유할 수 있다.

### IssueActivity

`{ timestamp, action, detail }` 구조의 타임라인 엔트리. `applyIssuePatch`에서 변경 사항을 자동으로 activity에 push한다.

## 상태 관리

### React Query 캐시 구조

세 가지 캐시 그룹을 사용한다:
- `issueKeys.list(query)` — 필터/정렬/페이지 조합별 이슈 목록
- `issueKeys.detail(id)` — 개별 이슈 상세
- `issueKeys.summary()` — 대시보드 요약 (status별 count, health 점수 등)

key factory 패턴으로 `issueKeys.all()`을 기준으로 prefix invalidation이 가능하다.

### 낙관적 업데이트 흐름

```
사용자 액션
  → onMutate: snapshot 저장 + list/detail 캐시 교체
  → 서버(mock) 요청
    성공 → onSuccess: invalidate all + Undo toast (previousIssue 포함)
    실패 → onError: snapshot 복원 + Retry toast
사용자가 Undo 클릭
  → restoreIssuesSnapshot([previousIssue])
  → invalidate all
```

### 로컬 상태 7개

OpsTriageConsole 컴포넌트에는 7개의 useState가 있다:
1. `query` — 현재 필터/정렬/페이지 상태
2. `selectedIssueId` — detail dialog에 표시할 이슈 ID
3. `toast` — 알림 메시지 (success | error | undo | retry)
4. `rowSelection` — TanStack Table의 체크박스 선택 상태
5. `activeViewId` — 현재 활성화된 saved view ID
6. `bulkDraft` — bulk 액션용 임시 patch 데이터
7. `runtime` — DemoRuntimeConfig (latency, failure rate 등)

## 데이터 계층

### storage.ts — 듀얼 스토리지

`canUseStorage()` 가드로 SSR 안전성을 확보한다. 클라이언트에서는 localStorage에 JSON.stringify/parse로 읽고 쓴다. SSR이나 localStorage 불가 환경에서는 모듈 레벨 변수(memory)에 저장한다.

### service.ts — mock API

`simulateRequest`로 모든 API 호출을 감싼다. 내부에서 `waitForLatency` → `shouldSimulateFailure` 순서로 실행하며, 실패 시 `createRetryableError`로 재시도 가능한 에러를 생성한다. 성공 시 변경 전 상태를 반환하므로 Undo에 사용할 수 있다.

### simulate.ts — 카오스 엔지니어링

세 가지 기능을 제공한다:
- `waitForLatency(config)` — 0~max 사이 랜덤 지연
- `shouldSimulateFailure(config)` — mode(random/burst/sequential)에 따른 실패 판정
- `createRetryableError(message)` — Error 서브클래스에 `retryable: true` 플래그 부착

### query.ts — 순수 필터/정렬 함수

`applyIssueQuery`는 순수 함수로, Issue[]와 IssueQuery를 받아 필터 → 정렬 → 페이지네이션 순서로 처리한다. 6개 필터 조건은 AND로 결합된다. `createDashboardSummary`는 전체 이슈 배열로부터 status별 count, 평균 priority, SLA health 등을 계산한다.

## 검증

### Zod 4 스키마

- `issuePatchSchema` — 변경 가능한 5개 필드의 runtime 검증
- `bulkIssuePatchSchema` — issueIds(1개 이상) + patch
- `noteSchema` — 최대 180자 제한, 커스텀 에러 메시지

TypeScript 타입과 Zod 스키마를 분리한 이유: 타입은 utility type 조합이 복잡하고 Zod로 표현하면 가독성이 떨어진다. 타입은 컴파일 타임, 스키마는 런타임으로 역할을 구분했다.

## UI 아키텍처

### TanStack React Table

`createColumnHelper<Issue>()`로 8개 컬럼을 정의한다:
- select (체크박스)
- id
- title (truncate)
- status (Badge)
- priority (색상 코딩)
- team
- slaRisk (아이콘)
- actions (dropdown)

`useReactTable`에 `getCoreRowModel`, `onRowSelectionChange`를 전달하고, table.getRowModel().rows를 순회해 `<tr>`을 렌더링한다.

### Radix UI 컴포넌트 래퍼

11개의 Radix primitive를 Tailwind CSS 4 클래스와 결합해 래퍼 컴포넌트로 만들었다: Badge, Button, Card, Checkbox, Dialog, Input, Popover, Select, Textarea, Toast, Tooltip. 각 래퍼는 `className`을 받아 `clsx`와 `tailwind-merge`로 병합한다.

### issue-detail-dialog

Dialog 안에서 이슈의 전체 필드를 표시하고, status/priority/team/labels를 직접 변경할 수 있다. 변경 시 `useIssueMutation`이 호출되며, 낙관적 업데이트가 적용된다.

### runtime-controls

카오스 엔지니어링 설정 UI. failure rate 슬라이더, latency 범위, failure mode 선택, "Fail Next Request" 버튼을 제공한다.

## 테스트 전략

### 단위 테스트 (Vitest)

- `optimistic.test.ts` — applyIssuePatch가 원본을 변경하지 않음, 여러 필드 동시 변경, activity 추가
- `query.test.ts` — 6개 필터 조합, 4개 정렬 전략, 페이지네이션 경계, 빈 결과
- `simulate.test.ts` — latency 범위 검증, failure mode별 동작, retryable error 구조

### 통합 테스트 (Vitest + Testing Library)

- query 변경 → list 갱신
- mutation → 캐시 동기화
- bulk mutation → 모든 선택 row 반영
- rollback → snapshot 복원 + retry toast

### E2E 테스트 (Playwright)

- 이슈 상세 열기 → 수정 → Undo
- saved view 적용 → bulk 액션
- 에러 발생 → retry
- 키보드만으로 전체 워크플로 수행

## SavedView 패턴

`SavedView = { id, name, query: Partial<IssueQuery> }`로 프리셋 필터를 저장한다. 적용 시 `mergeSavedView`가 현재 query에 view.query를 merge하고 page를 1로 리셋한다. query를 수동 변경하면 `activeViewId`가 null로 풀린다.

## Next.js 라우팅

App Router를 사용한다. `app/layout.tsx`에서 QueryClientProvider를 설정하고, `app/page.tsx`에서 `<OpsTriageConsole />`을 렌더링한다. `app/case-study/page.tsx`에서 프로젝트 소개와 아키텍처 설명을 포함한 정적 페이지를 제공한다.
