# 회고 — Ops Triage Console을 만들며 배운 것

## 프로젝트 개요

Next.js 16과 React 19를 기반으로 B2B SaaS 운영 콘솔을 구현했다. 실시간 이슈 트리아지 대시보드라는 도메인 위에, mock 서비스 + 낙관적 업데이트 + 롤백/언두 + 카오스 엔지니어링이라는 주제를 쌓았다. 완성 후 돌아보면, 이 프로젝트에서 가장 많이 배운 지점은 "상태가 여러 곳에 동시에 존재할 때 어떻게 일관성을 유지하는가"였다.

## 잘한 점

### mock 서비스 아키텍처의 분리

storage → service → simulate 순서로 계층을 나눈 것이 좋았다. storage.ts는 localStorage/memory 듀얼 스토리지, service.ts는 비동기 mock API, simulate.ts는 지연/실패 주입을 담당한다. 이 분리 덕분에:

- 테스트에서 storage만 리셋하면 깨끗한 상태가 보장된다.
- simulate.ts의 failure 모드를 바꾸면 에러 시나리오를 즉시 재현할 수 있다.
- service.ts는 실제 API로 교체할 때 인터페이스만 유지하면 된다.

### 낙관적 업데이트의 패턴화

단건 mutation과 bulk mutation 모두 동일한 패턴을 따르도록 만들었다: onMutate에서 snapshot 저장 + 캐시 교체, onError에서 snapshot 복원 + Retry toast, onSuccess에서 invalidate + Undo toast. 이 패턴을 두 mutation에 일관되게 적용한 결과, 새로운 mutation을 추가할 때도 같은 뼈대를 재사용할 수 있었다.

### Zod 4와 schema-first 접근

Zod 4의 schema에서 타입을 추출하는 방식(`z.infer<typeof schema>`)을 사용하지 않고, 별도의 TypeScript 타입을 정의한 뒤 schema는 런타임 검증용으로만 사용했다. 이 선택은 의도적이었다. `IssuePatch`의 타입이 `Partial<Pick<Issue, ...>>` 같은 복잡한 유틸리티 타입 조합인 경우, Zod로 표현하면 가독성이 크게 떨어지기 때문이다. 타입은 TypeScript가 담당하고, schema는 런타임 가드로 역할을 분리했다.

### 테스트 3계층 전략

단위 테스트(optimistic, query, simulate)로 순수 로직을 검증하고, 통합 테스트(React Query + TanStack Table이 연동된 실제 컴포넌트)로 상태 흐름을 검증하고, E2E(Playwright)로 사용자 시나리오를 검증했다. 각 계층이 검증하는 대상이 명확했기 때문에, 버그가 생기면 어느 계층에서 잡혀야 하는지 판단하기 쉬웠다.

## 부족했던 점

### query key 구조의 후발적 설계

초기에 query key를 `["issues"]`, `["issue", id]` 같은 단순 key로 시작했다가, invalidation 범위가 넓어지면서 `issueKeys` 팩토리 패턴으로 리팩터링했다. 처음부터 key factory를 설계했다면 중간에 key를 교체하는 작업이 줄었을 것이다.

```typescript
const issueKeys = {
  all: () => ["issues"] as const,
  lists: () => [...issueKeys.all(), "list"] as const,
  list: (query: IssueQuery) => [...issueKeys.lists(), query] as const,
  detail: (id: string) => [...issueKeys.all(), "detail", id] as const,
  summary: () => [...issueKeys.all(), "summary"] as const,
};
```

### saved view와 query 동기화의 복잡도

savedView를 적용하면 query가 바뀌고, query가 바뀌면 UI가 갱신되고, UI에서 필터를 바꾸면 activeViewId가 해제되어야 한다. 이 3방향 동기화를 useState 3개로 관리하면서 edge case가 많았다. useReducer나 상태 머신으로 명시적으로 전환을 관리했으면 더 깔끔했을 것이다.

### Radix UI 컴포넌트의 래핑 비용

Radix의 `@radix-ui/react-select`, `@radix-ui/react-dialog` 등을 Tailwind와 결합하기 위해 11개 래퍼 컴포넌트를 만들었다. 래퍼 자체는 간단하지만, 각각의 props 인터페이스를 정의하고 forwardRef를 설정하는 보일러플레이트가 상당했다. shadcn/ui 같은 코드 생성 도구를 사용했으면 이 시간을 줄일 수 있었을 것이다.

## 기술적 인사이트

### React Query의 캐시는 "또 하나의 상태 저장소"이다

React Query를 "서버 상태 관리 도구"로만 생각하면, onMutate에서 캐시를 직접 조작하는 코드가 이상하게 느껴진다. 하지만 낙관적 업데이트를 구현하면, 캐시가 곧 사용자가 보는 UI의 source of truth라는 것을 깨닫는다. list, detail, summary 세 곳의 캐시가 모두 동일한 데이터를 다른 형태로 가지고 있고, mutation이 발생하면 세 곳을 모두 일관되게 변경해야 한다.

### "Undo" 기능의 핵심은 snapshot이다

Undo는 "변경을 되돌리기"가 아니라 "이전 스냅샷으로 교체하기"로 구현해야 한다. 변경을 역으로 적용하면 중간에 다른 변경이 끼어들었을 때 충돌이 생긴다. mutation 응답에 `previousIssue`를 포함시키고, Undo 시 이 스냅샷을 storage에 직접 쓰는 방식이 안전하다.

### mock service에 "카오스"를 넣으면 에러 처리가 자연스러워진다

simulate.ts 없이 만들었다면, 에러 처리 코드를 "일단 있어야 하니까" 넣게 된다. 하지만 runtime-controls에서 failure rate를 50%로 올리면, 에러 처리가 실제로 동작하는 것을 눈으로 확인하면서 자연스럽게 Toast, Retry, Rollback 흐름을 다듬게 된다.

### TanStack Table의 column definition은 선언형으로 충분하다

`columnHelper.accessor`와 `columnHelper.display`로 8개 컬럼을 정의할 때, 각 컬럼의 `cell` 렌더러에 Radix 컴포넌트를 직접 넣었다. JSX를 반환하는 함수일 뿐이므로, 별도의 CellRenderer 컴포넌트로 분리할 필요가 없었다. 컬럼 정의 자체가 "이 데이터를 어떤 UI로 보여줄까"라는 선언이 된다.

## 다음에 다르게 하고 싶은 것

1. **query state machine** — 필터/정렬/페이지/saved view의 전환을 useReducer + discriminated union으로 모델링
2. **mutation 추상화** — 단건/bulk mutation의 공통 패턴을 `createOptimisticMutation` 팩토리로 추출
3. **server component 활용** — 현재 모든 것이 "use client"인데, 초기 데이터 로딩을 server component로 분리하면 hydration이 빨라질 것
4. **접근성 향상** — 키보드 전용 E2E 테스트를 작성했지만, 실제 스크린 리더로 검증하지는 못했다
