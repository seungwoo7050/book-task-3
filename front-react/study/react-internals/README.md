# React Internals Track

이 트랙은 React 런타임을 모두 따라 만드는 것이 아니라, 주니어 끝자락 기준으로 꼭 필요한 mental model을 4개 핵심 단계로 압축해 학습하는 코스다.

## 프로젝트 목록

| 순서 | 프로젝트 | 상태 | 설명 |
| --- | --- | --- | --- |
| 01 | [01-vdom-foundations](01-vdom-foundations/README.md) | verified | VNode, `createElement`, DOM 생성과 동기 재귀 렌더 |
| 02 | [02-render-pipeline](02-render-pipeline/README.md) | verified | diff/patch, render/commit 분리, work unit의 필요성 |
| 03 | [03-hooks-and-events](03-hooks-and-events/README.md) | verified | function component state/effect, delegated events, runtime integration |
| 04 | [04-runtime-demo-app](04-runtime-demo-app/README.md) | verified | 공유 런타임 위의 demo app, 성능과 한계 문서화 |

## 왜 4단계로 압축했는가

기존 레거시와 초기 재설계는 7단계로 더 세분화되어 있었다. 하지만 주니어 끝자락 기준에서는 너무 길고, 학습자의 핵심 질문보다 단계 수가 많아지는 문제가 있었다.

압축 원칙은 아래와 같다.

- `01-vdom-foundations`는 그대로 유지한다.
- `reconciliation`과 `fiber`는 `02-render-pipeline`으로 묶는다.
- `hooks`, `event delegation`, `mini-react integration`은 `03-hooks-and-events`로 묶는다.
- capstone은 `04-runtime-demo-app`으로 단순화한다.

세부 pedagogical reasoning은 [docs/phase-map.md](docs/phase-map.md)에 부록으로 보존한다.

## 검증 원칙

현재 실제 workspace package와 검증이 연결된 것은 아래 네 단계다.

```bash
cd study
npm run verify:internals
```

- `01-vdom-foundations`
- `02-render-pipeline`
- `03-hooks-and-events`
- `04-runtime-demo-app`

후속 단계는 같은 방식으로 구현과 검증이 끝나면 순서대로 `verified`로 올린다.
