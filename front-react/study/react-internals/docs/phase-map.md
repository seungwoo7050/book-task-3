# Phase Breakdown Map

`react-internals`는 원래 더 세분화된 7단계 흐름으로 설계되었지만, 주니어 끝자락 기준의 핵심 경로에서는 4단계로 압축했다. 이 문서는 그 매핑 근거를 보존한다.

## Mapping

| 이전 세분화 | 새 핵심 단계 | 이유 |
| --- | --- | --- |
| `01-vdom-foundations` | `01-vdom-foundations` | 시작점 자체는 가장 작은 핵심 단위라 그대로 유지한다 |
| `02-tree-reconciliation` | `02-render-pipeline` | diff/patch만으로는 갱신 파이프라인을 충분히 설명하기 어렵다 |
| `03-fiber-scheduler` | `02-render-pipeline` | render/commit split과 work unit reasoning을 같은 축에서 다루는 편이 더 명확하다 |
| `04-hooks-runtime` | `03-hooks-and-events` | state/effect는 이벤트 및 런타임 통합과 함께 봐야 제품형 mental model이 된다 |
| `05-event-delegation` | `03-hooks-and-events` | delegated event는 통합 런타임에서 의미가 더 선명해진다 |
| `06-mini-react-runtime` | `03-hooks-and-events` | hooks와 events를 묶은 뒤에 runtime integration을 같은 단계에서 설명한다 |
| `07-capstone-demo-app` | `04-runtime-demo-app` | 공유 런타임을 소비하는 작은 demo app과 limitation note로 단순화한다 |

## Why This Is Still Honest

- 세부 단계를 숨기지 않고 문서로 남긴다.
- 구현 경로는 짧게 유지하지만, 학습 논리는 부록에서 그대로 읽을 수 있다.
- 이후 구현이 확장되어도 core path는 4단계로 유지한다.
