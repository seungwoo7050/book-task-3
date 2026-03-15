# Building The Triage Surface

이 프로젝트를 다시 읽으면서 가장 먼저 눈에 들어온 건 기능 수가 아니라 화면 밀도였다. support, QA, feedback, monitoring에서 올라온 이슈를 한 명의 운영자가 빠르게 훑으려면, 예쁜 카드보다도 "한 화면에서 얼마나 많은 판단을 잃지 않고 처리할 수 있는가"가 더 중요하다. 그래서 이 콘솔의 첫 번째 성과는 state management보다 surface 설계에 있다.

## dashboard와 queue를 따로 만들지 않고 같은 흐름으로 붙였다

핵심 화면은 [`next/src/components/console/ops-triage-console.tsx`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console/next/src/components/console/ops-triage-console.tsx)에 모여 있다. 여기서 눈에 띄는 점은 summary, filters, table, detail dialog, runtime controls가 분리된 앱이 아니라 하나의 triage 흐름으로 이어진다는 것이다.

테이블은 `@tanstack/react-table`로 dense queue를 만들고, 왼쪽에서는 row selection과 saved view, 위에서는 summary와 current filter state, 오른쪽에서는 detail dialog가 열리는 식이다. 중요한 건 운영자가 화면을 이동하는 대신, 같은 화면에서 `scan -> select -> inspect -> update`를 끝낼 수 있게 설계했다는 점이다.

`useDeferredValue(query.search)`를 search에 쓴 것도 내부도구 맥락에 맞다. search input은 즉시 반응해야 하지만, 실제 query 적용은 약간 늦춰 dense queue를 덜 흔들게 만든다. 즉 이 콘솔은 "빠른 검색"보다 "흐름이 깨지지 않는 검색"을 택한다.

## saved view와 facet은 단순 편의가 아니라 triage 압축 장치다

[`next/src/lib/query.ts`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console/next/src/lib/query.ts)의 `mergeSavedView()`는 saved view를 불러오되 페이지를 1로 되돌린다.

```ts
return {
  ...defaultIssueQuery,
  ...query,
  ...view.query,
  page: 1,
};
```

이 한 줄이 중요한 이유는, saved view가 단순 프리셋이 아니라 "운영자의 다음 sweep 시작점"으로 쓰이기 때문이다. 기존 page를 유지하면 view 전환 직후 빈 화면이나 엉뚱한 pagination 상태에 빠질 수 있는데, 여기서는 그 가능성을 먼저 잘라 낸다.

동시에 이 saved view가 무엇이 아닌지도 적어 두는 편이 정확하다. 현재 `defaultSavedViews`는 코드에 박힌 shipped preset이고, 사용자가 새로 만들거나 편집해 persistence 되는 객체는 아니다. 즉 이 프로젝트가 보여 주는 건 "saved view CRUD"가 아니라 triage preset merge semantics다.

query helper 테스트도 이 부분을 정확히 잠근다. saved view merge 후 page가 1로 돌아가고, search 같은 현재 맥락은 유지되는지 본다. 즉 filter surface는 UX 장식이 아니라, 운영자의 사고 흐름을 잇는 상태 규칙이다. 반대로 view 생성/수정/삭제 같은 기능은 현재 테스트 범위에도 없다.

## surface는 keyboard와 dense data를 같이 감당하도록 설계됐다

이 콘솔이 좋은 이유는 내부도구라고 해서 keyboard를 포기하지 않았다는 점이다. Playwright 마지막 시나리오는 keyboard-only triage path를 끝까지 재생한다.

- issue search input focus
- 검색
- issue open
- operator note 입력
- apply triage

즉 dense table과 detail action이 모두 mouse-first 경험으로 잠기지 않는다. 이건 내부도구 품질에서 꽤 중요하다. 실제 운영자 도구는 반복 작업이 많기 때문에 keyboard path가 살아 있어야 피로가 덜 쌓인다.

그래서 이 프로젝트의 첫 편에서 남겨야 할 핵심은 화려한 UI보다는 "이 많은 판단 요소를 한 화면에 올리되, triage 흐름이 끊기지 않게 만들었다"는 사실이다.
