# 접근 기록 — Ops Triage Console 구현 과정

## 도메인 모델링부터 시작

코드를 짜기 전에 types.ts를 먼저 정의했다. 이 프로젝트는 도메인 타입이 다양하므로, 타입이 곧 설계 문서 역할을 한다.

**핵심 타입들:**
- `Issue`: 18개 필드 — id, title, summary, customer, source, status, priority, slaRisk, labels, routeTeam, owner, accountTier, affectedUsers, createdAt/updatedAt/lastSeenAt, operatorNote, activity
- `IssueQuery`: search, status[], priority[], source[], slaRisk[], label[], sort, page, pageSize — 멱등한 filter/sort 명세
- `IssuePatch` / `BulkIssuePatch`: 단건/다건 수정 명세
- `SavedView`: 저장된 filter 조합 (id, name, description, query)
- `DashboardSummary`: 대시보드에 표시할 집계값
- `DemoRuntimeConfig`: 실패 시뮬레이션 설정 (mode, failureRate, latencyMs, failNextRequest)

리터럴 유니온 타입을 적극 활용했다. IssueStatus는 5개, IssuePriority는 4개, IssueSource는 4개, SlaRisk는 3개 — 이 타입들이 UI의 badge, filter 선택지, 정렬 로직에 모두 반영된다.

## 데이터 계층: mock 서비스 아키텍처

실제 API 없이 제품형 동작을 구현하기 위해 세 계층을 설계했다.

**1. storage.ts — persistence layer**
localStorage와 메모리 캐시를 병행한다. SSR에서는 localStorage가 없으므로 `canUseStorage()`로 분기한다. readIssues/writeIssues로 CRUD하며, resetIssues로 시드 데이터를 복원한다.

**2. service.ts — API simulation layer**
모든 함수가 async다. `simulateRequest(kind)`를 호출해 latency와 failure를 시뮬레이션한다. listIssues, getIssue, updateIssue, bulkUpdateIssues — REST API처럼 생긴 함수들이지만 내부는 storage를 읽고 쓴다.

**3. simulate.ts — chaos engineering**
DemoRuntimeConfig에 따라 요청을 지연시키거나 실패시킨다. `shouldSimulateFailure`는 mode(stable/chaos)와 failureRate, failNextRequest 플래그로 결정한다. `createRetryableError`는 code와 retryable 속성이 있는 에러를 만든다.

이 계층 분리 덕분에, React Query hook 쪽에서는 실제 API를 호출하든 mock을 호출하든 인터페이스가 같다.

## query.ts — 필터/정렬/페이지네이션 로직

`applyIssueQuery`는 순수 함수다. Issue 배열과 IssueQuery를 받아 IssueListResult를 반환한다.

필터링은 6개 조건의 AND 조합이다:
- search: title + summary + customer + routeTeam + labels를 합쳐 소문자 includes
- status, priority, source, slaRisk: 선택된 값 배열에 포함 여부 (빈 배열이면 전체 통과)
- label: 선택된 라벨이 모두 포함되는지 (every)

정렬은 4가지 기준: updated_desc, priority_desc, sla_desc, created_desc. priority와 sla는 weight 맵으로 숫자화한다.

`createDashboardSummary`는 Issue 배열로부터 집계값을 계산한다. totalIssues, atRiskCount, untriagedCount, escalatedCount, priorityCounts, sourceCounts, recentChanges.

## optimistic.ts — 낙관적 업데이트

`applyIssuePatch`는 Issue와 IssuePatch를 받아 새 Issue를 반환한다. 변경된 필드마다 activity 항목을 추가한다. 이 함수가 두 곳에서 쓰인다:
1. service.ts의 updateIssue — 서버 측 적용
2. use-ops-triage.ts의 onMutate — 클라이언트 측 낙관적 업데이트

같은 함수를 서버와 클라이언트에서 공유하므로, 낙관적 결과와 실제 결과가 일치한다.

## schemas.ts — Zod 검증

issuePatchSchema와 bulkIssuePatchSchema로 service 함수 진입 직전에 데이터를 검증한다. noteSchema는 최대 180자 제한을 걸어 "타임라인에서 스캔할 수 있을 정도로 짧게"라는 UX 제약을 코드로 표현한다.

## React Query hooks — 서버 상태 관리

use-ops-triage.ts에 모든 query/mutation hook을 모았다.

**Query hooks:**
- `useIssueList(query)`: IssueQuery를 key에 포함, 필터가 바뀌면 자동 refetch
- `useIssueDetail(issueId)`: enabled 조건으로 선택된 이슈가 있을 때만 fetch
- `useDashboardSummary()`: 전체 이슈 집계
- `useSavedViews()`: 저장된 뷰 목록

**Mutation hooks:**
- `useIssueMutation(setToast)`: 단건 수정. onMutate에서 캐시를 낙관적으로 교체하고, onError에서 snapshot으로 복원하며 Retry toast를 띄운다. onSuccess에서 invalidate + Undo toast를 띄운다.
- `useBulkIssueMutation`: 다건 수정. 같은 optimistic/rollback 패턴.
- `useResetDemoMutation`: 시드 데이터 복원.

Undo 흐름은 onSuccess 안에서 구현된다. `restoreIssuesSnapshot([result.previousIssue])`를 호출해 이전 상태를 storage에 쓰고, 다시 invalidate한다.

## OpsTriageConsole — 메인 UI 컴포넌트

하나의 큰 컴포넌트가 콘솔 전체를 담는다. 상태 7개:
- query (IssueQuery), selectedIssueId, toast, rowSelection, activeViewId, bulkDraft, runtime

TanStack React Table로 column 정의. 8개 컬럼: select(checkbox), title, source, status, priority, slaRisk, route, updatedAt, actions.

`useDeferredValue`로 검색어를 지연시킨다. React 19의 concurrent feature를 활용해, 타이핑 중에 queue 재렌더를 지연시킨다.

## UI 컴포넌트 계층

Radix UI primitives를 감싼 ui/ 컴포넌트 11개: Badge, Button, Card, Checkbox, Dialog, Input, Popover, Select, Textarea, Toast, Tooltip. 각각이 Tailwind CSS로 스타일링되어 있다.

console/ 컴포넌트 3개:
- ops-triage-console.tsx: 대시보드 + 큐 + 필터 + 벌크 액션
- issue-detail-dialog.tsx: 이슈 상세 + 편집 폼 (Radix Dialog)
- runtime-controls.tsx: 실패 시뮬레이션 UI

## Case Study 라우트

`/case-study` 라우트가 별도로 있다. 제품 요약, UX 판단 근거, 테스트/성능 요약을 면접 자리에서 보여 주기 위한 페이지다.
