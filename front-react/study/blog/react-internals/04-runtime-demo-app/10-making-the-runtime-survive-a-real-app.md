# Making The Runtime Survive A Real App

이 프로젝트를 다시 읽으면서 가장 중요하게 보였던 건 앱 UI보다 소비 관계였다. 앞 단계까지는 runtime 자체를 만들고 검증했다. 여기서는 그 runtime이 정말 consumer app 위에서도 설명 가능한 동작을 하는지 본다. 그래서 포인트는 search box나 카드 UI가 아니라, `@front-react/hooks-and-events`를 실제 dependency로 소비하면서 debounce, pagination, metrics를 한 화면에서 돌려 보는 데 있다.

## 먼저 runtime을 복사하지 않고 가져다 썼다는 점이 중요하다

[`package.json`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app/package.json)을 보면 이 앱은 runtime 소스를 복붙하지 않는다.

```json
"dependencies": {
  "@front-react/hooks-and-events": "*"
}
```

그리고 [`ts/src/app.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app/ts/src/app.ts) 첫 줄에서 실제로 shared runtime API를 import한다.

```ts
import {
  createElement,
  render,
  resetRuntime,
  useEffect,
  useState,
  type SetStateAction,
} from "@front-react/hooks-and-events";
```

이 점이 중요한 이유는, internals 트랙이 여기서 비로소 "학습용 구현"에서 "소비 가능한 패키지"로 넘어가기 때문이다. runtime이 진짜로 재사용된다면, 그 장점뿐 아니라 한계도 consumer app 맥락에서 더 분명하게 보이게 된다.

다만 이 package boundary도 정확히 적어 둘 필요가 있다. 여기서 `"@front-react/hooks-and-events": "*"`는 published npm package를 새로 설치해 검증한다기보다, 같은 workspace 안의 패키지를 consumer app이 import하는 monorepo boundary에 가깝다. 즉 이 프로젝트는 "패키지로 소비되는가"는 보여 주지만, registry publish/install까지 증명하지는 않는다.

## debounce와 pagination은 같은 상태 축 위에서 서로 간섭한다

이 앱의 중심은 `useDebouncedValue`, `visibleCount`, 그리고 metrics effect 세 가지다.

```ts
const [query, setQuery] = useState("");
const debouncedQuery = useDebouncedValue(query, DEBOUNCE_MS);
const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
```

`useDebouncedValue()`는 effect cleanup을 이용해 오래된 timer를 지운다.

```ts
useEffect(() => {
  const timeoutId = window.setTimeout(() => {
    setDebounced(value);
  }, delayMs);

  return () => {
    window.clearTimeout(timeoutId);
  };
}, [value, delayMs]);
```

그리고 debounced query가 바뀌면 visible window를 다시 첫 페이지로 돌린다.

```ts
useEffect(() => {
  setVisibleCount(PAGE_SIZE);
}, [normalizedQuery]);
```

즉 이 앱은 검색과 페이지네이션을 따로 노는 기능으로 두지 않는다. query가 바뀌면 load-more 상태도 다시 계산해야 한다는 점을 effect로 명시해 둔다. 그래서 테스트 첫 시나리오가 debounce window 전후를 나눠 확인하고, load-more 테스트가 visible metrics까지 같이 보는 것이다.

## metrics panel은 성능 도구가 아니라 runtime 관찰 창이다

이 앱을 읽을 때 가장 조심해야 하는 부분은 metrics다. 이름만 보면 profiler처럼 보일 수 있지만, 실제로는 runtime이 어떤 상호작용 뒤 얼마나 자주 다시 그렸는지 보여 주는 학습용 패널에 가깝다.

`updateMetrics()`는 commit 시간을 대략적으로 기록하고 render count를 올린다.

```ts
setMetrics((previous) => ({
  renderCount: previous.renderCount + 1,
  lastCommitMs: elapsed,
  visibleCount,
  matchCount,
  activeQuery,
}));
```

여기서 중요한 건 절대 정확도가 아니라, 검색/페이지네이션/리렌더가 metrics panel에도 같이 드러난다는 점이다. docs가 "production profiler처럼 주장하지 않는다"고 못 박는 이유도 바로 이 때문이다.

게다가 `renderCount`라는 이름도 문자 그대로 읽으면 과해질 수 있다. 이 값은 `updateMetrics()`를 호출하는 effect가 돌 때만 증가하고, 그 effect dependency는 `normalizedQuery`, `visibleItems.length`, `filteredItems.length`다. 즉 이 panel은 모든 commit을 전역적으로 세는 profiler라기보다, 검색어와 visible window가 바뀔 때 runtime이 남긴 대표 샘플을 보여 주는 쪽에 더 가깝다.

## dataset과 UI는 runtime의 한계를 보여 주는 쪽으로 설계됐다

[`ts/src/data.ts`](/Users/woopinbell/work/book-task-3/front-react/study/react-internals/04-runtime-demo-app/ts/src/data.ts)에는 metrics, interaction, effects, limitations 같은 카테고리의 10개 item이 들어 있다. 이건 그냥 예시 데이터가 아니라, runtime이 무엇을 잘 설명하고 무엇은 아직 못 하는지 주제별로 보여 주기 위한 dataset이다.

UI도 같은 철학을 따른다.

- 기본 `PAGE_SIZE = 4`
- `DEBOUNCE_MS = 250`
- load more는 단순 button
- no match면 empty state
- metrics panel은 항상 side panel로 유지

즉 소비자 앱도 과하게 복잡하게 만들지 않고, runtime이 가진 현재 능력을 선명하게 보여 주는 쪽으로 절제돼 있다.

## 이번 검증은 "앱이 된다"보다 "runtime 특성이 앱에서도 드러난다"를 확인했다

이번 Todo에서 다시 돌린 검증은 아래 한 줄이었다.

```bash
npm run verify --workspace @front-react/runtime-demo-app
```

재실행 결과는 다음을 확인해 줬다.

- `demo.test.ts` 3개 테스트 통과
- typecheck 통과

테스트가 고정하는 핵심은 세 가지다.

1. debounce window 전에는 결과가 그대로 있고, 260ms 뒤에야 query가 반영되는가
2. load more가 visible item 수와 metrics panel을 함께 갱신하는가
3. 여러 상호작용 뒤에도 render metrics panel이 계속 남아 있는가

즉 이 앱의 검증 포인트는 UX polish보다 runtime 특성 노출에 가깝다. debounce cleanup, query/window 변화에 따라 갱신되는 metrics 샘플, visible window 변화가 consumer app 맥락에서 계속 관찰 가능해야 한다. 반대로 no-match empty state의 세부 문구나 CSS layout fidelity까지를 자동 테스트가 잠그는 것은 아니다.

## 그래서 이 프로젝트는 제품 데모라기보다 runtime 졸업 시험에 가깝다

여기에는 실제 네트워크도 없고 persistence도 없고 production profiling도 없다. 하지만 앞에서 만든 runtime이 "작은 앱 하나 정도는 설명 가능한 수준"인지 확인하는 데는 충분하다.

이 프로젝트의 성과는 runtime을 실제 소비자가 쓸 수 있는 패키지로 한 단계 끌어올렸다는 데 있다. 동시에 한계도 숨기지 않는다. metrics는 관찰값일 뿐이고, infinite scroll이나 real data layer는 없다. 그래서 이 앱은 완성된 제품이 아니라, internals 구현이 어디까지 현실 UI를 버틸 수 있는지 보여 주는 마감 단계로 읽는 편이 정확하다.
