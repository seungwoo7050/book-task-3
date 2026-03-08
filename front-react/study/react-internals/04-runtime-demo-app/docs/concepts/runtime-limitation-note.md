# Runtime Limitation Note

이 프로젝트는 shared runtime이 실제 UI 흐름 하나를 감당할 수 있음을 보여 주지만, 곧바로 제품 코드에 쓰기엔 제한이 많다.

## 현재 한계

- `useState`, 얇은 `useEffect`, delegated event만 지원한다.
- profiler API가 없어 metrics panel은 app state로 만든 관찰값이다.
- attribute 처리 범위가 좁아 `data-*` 같은 속성은 제품 수준으로 다루지 않는다.
- true infinite scroll, async data fetching, persistence는 없다.

## 왜 문서화하는가

이 capstone은 "우리 runtime도 React를 대체할 수 있다"를 주장하는 프로젝트가 아니다. 어디까지는 설명 가능하고 어디서부터는 portfolio나 실제 프레임워크로 넘어가야 하는지를 보여 주는 마감 단계다.
