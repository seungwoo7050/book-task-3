# Quality Bar

## 테스트

- unit: query/filter/sort, saved view serialization, optimistic helper, failure simulation
- integration: filter -> queue 갱신, detail mutation 동기화, bulk update, rollback + retry
- E2E: dashboard -> queue -> detail -> undo, saved view + bulk update, simulated failure + retry, keyboard flow

## 접근성

- 모든 주요 액션은 keyboard로 접근 가능해야 한다
- table selection, detail action, toast action은 명확한 label을 가져야 한다
- 색상만으로 상태를 전달하지 않는다

## 성능

- queue 연산은 memoized helper와 React Query 캐시를 사용한다
- summary와 detail은 필요한 단위로만 refetch한다
- dense UI라도 interaction latency가 낮게 유지되어야 한다

## 배포

- 기본 배포 타깃은 Vercel
- mock API와 local persistence만으로도 데모가 완결되어야 한다

