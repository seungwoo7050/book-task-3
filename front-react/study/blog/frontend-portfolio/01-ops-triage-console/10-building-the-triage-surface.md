# Building The Triage Surface

포트폴리오용 internal tool을 만들 때 가장 쉽게 빠지는 함정은 화면을 화려하게 만드는 데 집중하는 것이다. 하지만 운영자가 실제로 오래 머무는 도구는 보기 좋은 대시보드보다 "지금 어떤 이슈를 보고 있고, 다음에 무엇을 눌러야 하는지"가 더 빨리 보여야 한다. Ops Triage Console의 시작점도 바로 그 감각이었다.

이 프로젝트는 support, QA, customer feedback, monitoring에서 쏟아지는 이슈를 한 화면 안에서 triage할 수 있도록 설계됐다. 그래서 정보 밀도를 피하지 않는다. summary, filters, saved views, triage queue, detail dialog entry, bulk action이 모두 한 화면에서 이어진다. 중요한 건 복잡성을 감추는 것이 아니라, 운영자가 잃지 않도록 문맥을 잡아 주는 것이다.

코드를 보면 이 앱의 첫 번째 난제는 스타일이 아니라 surface composition이라는 사실이 분명하다. 어떤 상태는 query여야 하고, 어떤 상태는 operator가 잠깐 들고 있는 draft여야 한다. 이 경계가 서야 화면도 안정된다.

## 구현 순서를 먼저 짚으면

- 메인 콘솔에서 query, selection, saved view, bulk draft를 모두 한 작업 surface로 모았다.
- 테이블 row와 detail dialog를 분리하지 않고 같은 흐름 안에서 오가게 만들었다.
- typecheck와 테스트를 먼저 통과시켜 surface 설계가 이후 mutation 단계의 전제가 되게 했다.

## 좋은 internal tool은 먼저 머무를 수 있는 surface를 만들어야 했다

`OpsTriageConsole()`의 첫 몇 줄을 보면 이 프로젝트가 어디서부터 시작됐는지 드러난다. search query, selected issue, row selection, active view, bulk draft, runtime config가 모두 메인 surface 안에서 함께 움직인다.

```tsx
const [query, setQuery] = useState<IssueQuery>(defaultIssueQuery);
const [selectedIssueId, setSelectedIssueId] = useState<string | null>(null);
const [rowSelection, setRowSelection] = useState<RowSelectionState>({});
const [activeViewId, setActiveViewId] = useState("all");
const [bulkDraft, setBulkDraft] = useState<BulkIssuePatch>({});
const deferredSearch = useDeferredValue(query.search);
const effectiveQuery = { ...query, search: deferredSearch };
```

이 조각이 중요한 이유는 명확하다. 운영자의 문맥은 단일 상태로 설명되지 않는다. 검색어는 서버 query에 가깝고, row selection과 bulk draft는 지금 이 화면에서만 의미가 있다. 이걸 한 surface 안에서 같이 보이게 만들지 않으면, internal tool은 금방 모달과 세부 페이지 사이를 왕복하는 UI가 된다.

`docs/concepts/ux-and-state-flow.md`가 split view와 saved view를 특별히 강조하는 것도 같은 맥락이다. 운영자는 목록과 상세를 자주 왕복하고, 반복되는 triage 작업을 saved view로 줄여야 한다.

## dense queue는 목록이 아니라 작업 진입점이어야 했다

테이블 column 정의를 보면 이 앱이 데이터를 "보여 주는 것"보다 "작업을 시작하는 것"에 더 가깝다는 사실이 드러난다. 특히 title cell은 단순 텍스트가 아니라 detail dialog를 여는 버튼으로 설계돼 있다.

```tsx
{
  accessorKey: "title",
  header: "Issue",
  cell: ({ row }) => {
    const issue = row.original;
    return (
      <button type="button" className="text-left" onClick={() => setSelectedIssueId(issue.id)}>
        <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-slate-500">
          {issue.id}
        </p>
        <p className="mt-1 text-sm font-semibold text-slate-950">{issue.title}</p>
      </button>
    );
  },
}
```

즉 queue는 read-only 표가 아니라 작업 surface의 왼쪽 절반이다. 행을 클릭하면 곧바로 detail dialog로 이어지고, 그곳에서 status와 route, note를 바꾸고 다시 queue로 돌아온다. 화면 구조가 이 흐름을 끊지 않도록 설계돼 있기 때문에, 이후의 optimistic mutation과 retry도 같은 표면 위에서 자연스럽게 읽힌다.

이 시점에서 배운 건 internal tool의 좋은 밀도란 정보가 많다는 뜻이 아니라, operator가 다음 행동을 찾는 시간이 짧다는 뜻이라는 점이었다.

## 이 surface가 먼저 고정됐기 때문에 뒤의 mutation도 의미를 얻었다

이 단계에서는 아직 rollback과 retry를 깊게 다루지 않아도, 이미 검증은 surface의 안정성을 확인하고 있다.

```bash
cd study
npm run typecheck --workspace @front-react/ops-triage-console
npm run test --workspace @front-react/ops-triage-console
```

2026-03-13 replay 기준으로 typecheck가 통과했고, `vitest`는 unit과 integration을 합쳐 16개 테스트를 통과했다. 이 수치가 말해 주는 건 UI가 화려하다는 사실이 아니라, query, detail, summary, selection이 같은 화면 문맥 안에서 일관되게 움직인다는 사실이다.

다음 글로 넘어가면 질문이 조금 바뀐다. 이렇게 잘 정돈된 surface가 있다고 해서 곧바로 좋은 운영 도구가 되는 것은 아니다. 실제로 이슈를 바꾸는 순간, 빠르게 반응하면서도 되돌릴 수 있어야 하기 때문이다.
