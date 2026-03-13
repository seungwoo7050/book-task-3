# React Internals

이 트랙은 React를 "어떻게 쓰는가"보다 "어떻게 움직이는가"에 가까운 기록이다. JSX를 어떤 데이터 구조로 바꾸는지, 그 구조를 언제 DOM에 반영하는지, state와 effect와 event가 왜 같은 런타임 문제인지, 마지막에는 그 런타임이 실제 앱을 얼마나 버티는지까지 한 단계씩 밟는다.

## 읽는 순서

1. [01 VDOM Foundations](01-vdom-foundations/00-series-map.md)
   - JSX shape를 VNode와 DOM 조작으로 처음 연결하는 단계
2. [02 Render Pipeline](02-render-pipeline/00-series-map.md)
   - diff, patch, render/commit 분리를 처음 도입하는 단계
3. [03 Hooks And Events](03-hooks-and-events/00-series-map.md)
   - hook slot, effect cleanup, delegated event를 하나의 runtime으로 묶는 단계
4. [04 Runtime Demo App](04-runtime-demo-app/00-series-map.md)
   - 직접 만든 runtime을 실제 consumer app 위에 올려 보는 단계

앞의 프로젝트가 뒤의 전제이기 때문에, 이 트랙은 순서대로 읽을수록 훨씬 선명하다.
